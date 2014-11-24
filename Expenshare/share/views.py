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
    context = RequestContext(request)

    #Find the current PayUser
    currPayUser = PayUser.objects.get(userKey=request.user)
    paygroup_list = currPayUser.payGroups.all()
    payform = PayForm()
    groupform = MakeGroupForm()
    context_dict={'PayForm' : payform, 'paygroups' : paygroup_list, 'MakeGroupForm' : groupform}  
                                  
    return render_to_response('home.html', context_dict, context)

@login_required
def history(request):            
    context = RequestContext(request)

    print(request.POST['group'])
    currGroup = PayGroup.objects.get(name=request.POST['group'])
    paylog_list = currGroup.paymentLogs.order_by('-date')
    print(paylog_list)
    context_dict = {'paylog': paylog_list, 'group': currGroup}
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
            pass
        
    #Else it was not HTTP POST so have a blank form 
    else:
        userForm = UserForm()

    contextDict = {'userForm': userForm, 'registered': registered}

    return render_to_response('register.html', contextDict, context)

@login_required
def add_groupform(request):
    context = RequestContext(request)
    currPayUser = PayUser.objects.get(userKey=request.user)
    paygroup_list = currPayUser.payGroups.all()
    payform = PayForm()
    groupform = MakeGroupForm()
    context_dict={'PayForm' : payform, 'paygroups' : paygroup_list, 'MakeGroupForm' : groupform} 

    if (request.method=='POST'):
        groupform = MakeGroupForm(request.POST)
        
        if (groupform.is_valid()):
            group = groupform.save()   
            group.save()
            currPayUser = PayUser.objects.get(userKey=request.user)
            currPayUser.payGroups.add(group)
            group.members.add(request.user)

            return render_to_response('home.html', context_dict, context)  #After submitting the form, redirects the user back to the homepage
        else:
            print ("Error making this Group")

    context_dict={'PayForm' : payform, 'paygroups' : paygroup_list, 'MakeGroupForm' : groupform}  
    return render_to_response('home.html', context_dict, context)


# Alter this for add_payform
@login_required
def add_payform(request):
    context = RequestContext(request)
    print("Your Post was: ", request.POST)
    clickedGroup = PayGroup.objects.get(name=request.POST['group'])
    if (request.method=='POST'):
        payform = PayForm(request.POST)
        
        if (payform.is_valid()):
            cost = payform.save(commit=False)   
            cost.user = request.user
            cost.save()
            clickedGroup.paymentLogs.add(cost)
            print(clickedGroup)
            payLogs = clickedGroup.paymentLogs.order_by('date')

            return render_to_response('ExpenseLog.html', {'paylog' : payLogs, 'group' : clickedGroup})   #After submitting the form, redirects the user back to the homepage
        else:
            print ("Error Processing your Payment")
    else:
        payform = PayForm()

    currPayUser = PayUser.objects.get(userKey=request.user)
    paygroup_list = currPayUser.payGroups.all()
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
                #print("Wrong Passcode")
                return render_to_response('home.html', {'joingroup_error1' : True}, context)
        except:
            print ("This Group Does Not Exist.")


    paygroup_list = currPayUser.payGroups.all()
    groupform = MakeGroupForm()
    payform = PayForm()
    context_dict={'PayForm' : payform, 'paygroups' : paygroup_list, 'MakeGroupForm' : groupform}    
    return render_to_response('home.html', context_dict, context)

@login_required
def leavegroup(request):
    context = RequestContext(request)
    currPayUser = PayUser.objects.get(userKey=request.user)
    if (request.method == 'POST'):
        try:
            group = PayGroup.objects.get(name=request.POST['group'])
            group.members.remove(request.user)
            currPayUser.payGroups.remove(group)
            if group.members.exists():
                print("There are still existing members in this group.")
            else:
                group.delete()
                print("You were the last member! Group deleted.")
        except:
            print ("Error leaving Group.")


    paygroup_list = currPayUser.payGroups.all()
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
                            return render_to_response('login.html', {'login_error2' : True}, context)
		else:
			return render_to_response('login.html', {'login_error1' : True}, context)
	#Blank form
	else:
		return render_to_response('login.html', {}, context)

@login_required
def userLogout(request):
	logout(request)
	return HttpResponseRedirect('/share/')
