from django.contrib.auth import authenticate, login
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext

from persons.models import Person
from persons.forms import (AddPersonForm, RemovePersonForm,
                           UserForm, UserProfileForm)

def index(request):
    t = loader.get_template('index.html')
    return HttpResponse(t.render(RequestContext(request, {})))

def register(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the
    # registration was successful.
    # Set to False initially. Code changes value to True when
    # registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set
            # commit=False.
            # This delays saving the model until we're ready to avoid
            # integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in
            # the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print(user_form.errors, profile_form.errors)

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    #t = loader.get_template('register.html')
    #return HttpResponse(t.render(RequestContext(request, context)))
    return render_to_response(
            'register.html',
            {'user_form': user_form, 'profile_form': profile_form,
             'registered': registered},
            context)

def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value),
        # no user with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Persons account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('login.html', {}, context)


def list_persons(request):
    GET_SHORT_NAME = 'short'
    GET_FULL_NAME = 'full'
    GET_EMAIL = 'mail'

    get_params = { GET_SHORT_NAME : request.GET.get(GET_SHORT_NAME),
                    GET_FULL_NAME : request.GET.get(GET_FULL_NAME),
                    GET_EMAIL : request.GET.get(GET_EMAIL) }

    filter_strings = { GET_SHORT_NAME : 'short_name__icontains',
                        GET_FULL_NAME : 'full_name__icontains',
                        GET_EMAIL : 'email__icontains' }

    persons = Person.objects.all()

    for param in sorted(request.GET):
        print('GET: %s = %s' % (param, request.GET.get(param))) # for debug
        if get_params.get(param):
            filter_dict = { filter_strings[param] : get_params[param] }
            persons = persons.filter(**filter_dict)

    context_dict = {}
    context_dict['persons'] = persons
    context_dict['persons_count'] = len(persons)

    # make list font tiny:
    context_dict['tiny_font'] = request.GET.get('tiny')

    t = loader.get_template('persons.html')
    return HttpResponse(t.render(RequestContext(request, context_dict)))

def manage_persons(request):
    persons = Person.objects.all()
    form_data = request.POST if request.POST else None
    if form_data: # debug info
        print(form_data) # POST data (for debug)

    form_add = AddPersonForm(form_data)
    if form_add.is_valid():
        new_person = Person(
                        short_name=form_data.get('short_name'),
                        full_name=form_data.get('full_name'),
                        email=form_data.get('email')
                     )
        new_person.save() # write new row to DB
        return redirect('/persons/')

    form_rem = RemovePersonForm(form_data)
    if form_rem.is_valid():
        persons_to_be_removed = Person.objects.filter(
                    short_name__icontains=form_data.get('short_name_substr'))
        persons_to_be_removed.delete() # delete row from DB
        return redirect('/persons/')

    t = loader.get_template('manage.html')
    return HttpResponse(t.render(RequestContext(request,
                                       {'form_add' : form_add,
                                        'form_rem' : form_rem,
                                        'persons_count' : len(persons),}
                        )))

