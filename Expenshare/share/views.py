from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from share.models import PayUser, PayGroup, PaymentLog
from share.forms import UserForm, PayForm, MakeGroupForm
from share.forms import UserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    context_dict = {}

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render_to_response('login.html', context_dict, context)
@login_required
def home(request):
    # Request the context of the request.                                                            
    # The context contains information such as the client's machine details, for example.            
    context = RequestContext(request)

    # Construct a dictionary to pass to the template engine as its context.                          
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!                     
    paygroup_list = PayGroup.objects.order_by('name')
    payform = PayForm()
    groupform = MakeGroupForm()
    context_dict={'PayForm' : payform, 'paygroups' : paygroup_list, 'MakeGroupForm' : groupform}  

    # Return a rendered response to send to the client.                                              
    # We make use of the shortcut function to make our lives easier.                                     # Note that the first parameter is the template we wish to use.                                   
    return render_to_response('home.html', context_dict, context)

@login_required
def history(request):
    # Request the context of the request.                                                            
    # The context contains information such as the client's machine details, for example.            
    context = RequestContext(request)

    # Construct a dictionary to pass to the template engine as its context.                          
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!                     
    paylog_list = PaymentLog.objects.all()
    context_dict = {'paylog': paylog_list}

    # Return a rendered response to send to the client.                                              
    # We make use of the shortcut function to make our lives easier.                                     # Note that the first parameter is the template we wish to use.                                   
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
            #Make a new PayUser account
            payUser = PayUser(userKey=user)
            payUser.save()


            registered = True

        else:
            print("There was an error with registering your account.")
    
    #Else it was not HTTP POST so have a blank form 
    else:
        userForm = UserForm()

    contextDict = {'userForm': userForm, 'registered': registered}

    return render_to_response('register.html', contextDict, context)

@login_required
def add_groupform(request):
    context = RequestContext(request)

    if (request.method=='POST'):
        groupform = MakeGroupForm(request.POST)
        
        if (groupform.is_valid()):
            group = groupform.save()   
            group.save()

            return render_to_response('home.html')   #After submitting the form, redirects the user back to the homepage
        else:
            print ("Error making this Group")
    else:
        groupform = MakeGroupForm()

    paygroup_list = PayGroup.objects.order_by('name')
    payform = PayForm()
    context_dict={'PayForm' : payform, 'paygroups' : paygroup_list, 'MakeGroupForm' : groupform}  
    return render_to_response('home.html', context_dict, context)


# Alter this for add_payform
@login_required
def add_payform(request):
    context = RequestContext(request)

    if (request.method=='POST'):
        payform = PayForm(request.POST)
        
        if (payform.is_valid()):
            cost = payform.save(commit=False)   
            cost.user = request.user
            cost.save()

            return render_to_response('ExpenseLog.html')   #After submitting the form, redirects the user back to the homepage
        else:
            print ("Error Processing your Payment")
    else:
        payform = PayForm()

    paygroup_list = PayGroup.objects.order_by('name')
    groupform = MakeGroupForm()
    context_dict={'PayForm' : payform, 'paygroups' : paygroup_list, 'MakeGroupForm' : groupform}    
    return render_to_response('home.html', context_dict, context)

@login_required
def joingroup_form(request):
    context = RequestContext(request)
    print request.POST
    currPayUser = PayUser.objects.get(userKey=request.user)
    if (request.method == 'POST'):
        try:
            group = PayGroup.objects.get(name=request.POST['group'])
            passcode = request.POST['passcode']
            realcode = group.passcode
            if passcode==realcode:
                group.members.add(request.user)
                currPayUser.payGroups.add(group)
            else:
                print("Wrong Passcode")
        except:
            print ("Error joining Group.")


    paygroup_list = PayGroup.objects.order_by('name')
    groupform = MakeGroupForm()
    payform = PayForm()
    context_dict={'PayForm' : payform, 'paygroups' : paygroup_list, 'MakeGroupForm' : groupform}    
    return render_to_response('home.html', context_dict, context)



def userLogin(request):
	context = RequestContext(request)

	if(request.method == 'POST'):
		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(username=username, password=password)

		#Check to see if a user with the submitted credentials was found
		if(user):
			#Check to see if the user account is active
			if(user.is_active):
				login(request, user)
				return HttpResponseRedirect('/share/home')
			else:
				return HttpResponse("Sorry, this account has been disabled.")
		else:
			print("Nothing found with username: {0} and password: {1}".format(username, password))
			return HttpResponse('Either the username or password entered is incorrect')
	#Blank form
	else:
		return render_to_response('login.html', {}, context)

@login_required
def userLogout(request):
	logout(request)
	return HttpResponseRedirect('/share/')

