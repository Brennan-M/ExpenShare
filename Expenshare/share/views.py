from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from share.models import PayGroup, PaymentLog
from share.forms import UserForm

# Create your views here.
def index(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    paygroup_list = PayGroup.objects.order_by('name')
    context_dict = {'paygroups': paygroup_list}

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render_to_response('home.html', context_dict, context)

def home(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    context_dict = {}

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render_to_response('home.html', context_dict, context)

def history(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    context_dict = {}

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render_to_response('ExpenseLog.html', context_dict, context)

#View for registering new users
def register(request):
    context = RequestContext(request)

    #Boolean value saying whether registration was successful or not
    registered = False

    if(request.method=='POST'):
        #Attempt to get raw information
        userForm = UserForm(data=request.POST)

        #If getting the information was successful...
        if(userForm.is_valid()):
            #Save to database
            user = userForm.save()

            #This hashes the users password for safe storage
            user.set_password(user.password)
            user.save()

            registered = True

        else:
            print("There was an error with registering your account.")
    
    #Else it was not HTTP POST so have a blank form 
    else:
        userForm = UserForm()

    contextDict = {'userForm': userForm, 'registered': registered}

    return render_to_response('register.html', contextDict, context)





