from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from share.models import PayUser, PayGroup, PaymentLog, MemberView, FellowUser
from share.forms import UserForm, PayForm, MakeGroupForm
from share.forms import UserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import F
from decimal import *

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

    currPayUser = PayUser.objects.get(userKey=request.user)
    paygroup_list = currPayUser.payGroups.all()
    payform = PayForm()
    groupform = MakeGroupForm()

    try:
        currGroup = PayGroup.objects.get(name=request.POST['group'])
        partOf = False
    except:
        context_dict={'PayForm' : payform, 'paygroups' : paygroup_list, 'MakeGroupForm' : groupform, 'history_error1' : True} 
        return render_to_response('home.html', context_dict, context)

    if currGroup in currPayUser.payGroups.all():
        partOf = True

    if (partOf == False):
        context_dict={'PayForm' : payform, 'paygroups' : paygroup_list, 'MakeGroupForm' : groupform, 'history_error2' : True} 
        return render_to_response('home.html', context_dict, context)

    print(request.POST['group'])

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
            memV = MemberView(user=request.user)
            memV.save()
            group.memberViews.add(memV)

            return render_to_response('home.html', context_dict, context)  #After submitting the form, redirects the user back to the homepage
        else:
            context_dict={'PayForm' : payform, 'paygroups' : paygroup_list, 'MakeGroupForm' : groupform, 'creategroup_error1' : True}
            return render_to_response('home.html', context_dict, context)

    context_dict={'PayForm' : payform, 'paygroups' : paygroup_list, 'MakeGroupForm' : groupform}  
    return render_to_response('home.html', context_dict, context)


# Alter this for add_payform
@login_required
def add_payform(request):

    context = RequestContext(request)
    
    currPayUser = PayUser.objects.get(userKey=request.user)

    print("Your Post was: ", request.POST)

    try:
        clickedGroup = PayGroup.objects.get(name=request.POST['group'])
        partOf = False
    except:
        paygroup_list = currPayUser.payGroups.all()
        groupform = MakeGroupForm()
        context_dict={'paygroups' : paygroup_list, 'MakeGroupForm' : groupform, 'payform_error2' : True}
        return render_to_response('home.html', context_dict, context)

    if clickedGroup in currPayUser.payGroups.all():
        partOf = True

    if partOf == False:
        paygroup_list = currPayUser.payGroups.all()
        groupform = MakeGroupForm()
        context_dict={'paygroups' : paygroup_list, 'MakeGroupForm' : groupform, 'payform_error3' : True}
        return render_to_response('home.html', context_dict, context)

    if (request.method=='POST'):
        payform = PayForm(request.POST)
        
        if (payform.is_valid()):
            cost = payform.save(commit=False)   
            cost.user = request.user
            cost.save()

            #Load the playlogs 
            clickedGroup.paymentLogs.add(cost)
            payLogs = clickedGroup.paymentLogs.order_by('date')

            #Calculate new cost of the group
            for memV in clickedGroup.memberViews.all():
            	if memV.user.id == request.user.id:
                    memV.netOwed = ((Decimal(memV.netOwed) - Decimal(clickedGroup.groupSize - 1) * (Decimal(cost.amount) / Decimal(clickedGroup.groupSize))))
                    for fels in memV.fellows.all():
                        fels.owed = ((Decimal(fels.owed) - (Decimal(cost.amount) / Decimal(clickedGroup.groupSize))))
                        fels.save()
                else:
                    memV.netOwed = ((Decimal(memV.netOwed) + (Decimal(cost.amount) / Decimal(clickedGroup.groupSize))))
                    for fels in memV.fellows.all():
                        if fels.user.id == request.user.id:
                            fels.owed = ((Decimal(fels.owed) + (Decimal(cost.amount) / Decimal(clickedGroup.groupSize))))
                            fels.save()
                memV.save()
				
            return render_to_response('ExpenseLog.html', {'paylog' : payLogs, 'group' : clickedGroup})   #After submitting the form, redirects the user back to the homepage
        else:
            payLogs = clickedGroup.paymentLogs.order_by('date')
            return render_to_response('ExpenseLog.html', {'paylog' : payLogs, 'group' : clickedGroup, 'payform_error1' : True}, context)
    else:
        payform = PayForm()
    
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
                for memV in group.memberViews.all():
                	fellMem = FellowUser(user=request.user)
                	fellMem.save()
                	memV.fellows.add(fellMem)
            	newMemV = MemberView(user=request.user)
            	newMemV.save()
            	group.memberViews.add(newMemV)
            	for mems in group.members.all():
            		fellMem = FellowUser(user=mems)
            		fellMem.save()
            		newMemV.fellows.add(fellMem)
                group.members.add(request.user)
                currPayUser.payGroups.add(group)
                group.groupSize += 1
                group.save()
            else:
                paygroup_list = currPayUser.payGroups.all()
                groupform = MakeGroupForm()
                payform = PayForm()
                context_dict={'PayForm' : payform, 'paygroups' : paygroup_list, 'MakeGroupForm' : groupform, 'joingroup_error1' : True}
                return render_to_response('home.html', context_dict, context)

            paygroup_list = currPayUser.payGroups.all()
            groupform = MakeGroupForm()
            payform = PayForm()
            context_dict={'PayForm' : payform, 'paygroups' : paygroup_list, 'MakeGroupForm' : groupform}    
            return render_to_response('home.html', context_dict, context)
        except:
            pass

    paygroup_list = currPayUser.payGroups.all()
    groupform = MakeGroupForm()
    payform = PayForm()
    context_dict={'PayForm' : payform, 'paygroups' : paygroup_list, 'MakeGroupForm' : groupform, 'joingroup_error2' : True}
    return render_to_response('home.html', context_dict, context)

@login_required
def leavegroup(request):
    context = RequestContext(request)
    currPayUser = PayUser.objects.get(userKey=request.user)
    if (request.method == 'POST'):
        try:
            group = PayGroup.objects.get(name=request.POST['group'])

            #Determine if the user can leave or not
            canLeave = True
            memV = group.memberViews.get(user=request.user)
            if memV.netOwed != 0:
            	canLeave = False
            else:
                for fel in memV.fellows.all():
                    if fel.owed != 0:
                        canLeave = False
                        break 

            #Remove the user from the group
            if canLeave:
                for fel in memV.fellows.all():
                	fel.delete()
            	for mem in group.memberViews.all():
            		if mem != memV:
            			for fel in mem.fellows.all():
            				if fel.user == memV.user:
            					fel.delete()
            	memV.delete()
                group.members.remove(request.user)
                currPayUser.payGroups.remove(group)
                group.groupSize -= 1
                if not group.members.exists():
                    group.delete()
                    paygroup_list = currPayUser.payGroups.all()
                    groupform = MakeGroupForm()
                    payform = PayForm()
                    context_dict={'PayForm' : payform, 'paygroups' : paygroup_list, 'MakeGroupForm' : groupform, 'deleted_group' : True}    
                    return render_to_response('home.html', context_dict, context)
                else:
                    paygroup_list = currPayUser.payGroups.all()
                    groupform = MakeGroupForm()
                    payform = PayForm()
                    context_dict={'PayForm' : payform, 'paygroups' : paygroup_list, 'MakeGroupForm' : groupform}
                    group.save()    
                    return render_to_response('home.html', context_dict, context)
            else:
                context_dict={'PayForm' : payform, 'paygroups' : paygroup_list, 'MakeGroupForm' : groupform, 'leavegroup_error1' : True}
                return render_to_response('home.html', context_dict, context)
        except:
            print ("Error leaving Group.")

    paygroup_list = currPayUser.payGroups.all()
    groupform = MakeGroupForm()
    payform = PayForm()
    context_dict={'PayForm' : payform, 'paygroups' : paygroup_list, 'MakeGroupForm' : groupform, 'leavegroup_error1' : True}    
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

@login_required
def confirmPayment(request):
    context = RequestContext(request)
	
    group = PayGroup.objects.get(name=request.POST['group'])
    currPayUser = PayUser.objects.get(userKey=request.user) 
    try:
        memV = group.memberViews.get(user=request.user)
        targetUser = User.objects.get(username=request.POST['targetMember'])
        targetMem = group.memberViews.get(user=targetUser)
        myFellow = targetMem.fellows.get(user=request.user)
        targetFellow = memV.fellows.get(user=targetUser)
    except:
        paygroup_list = currPayUser.payGroups.all()
        groupform = MakeGroupForm()
        payform = PayForm()
        context_dict={'PayForm' : payform, 'paygroups' : paygroup_list, 'MakeGroupForm' : groupform, 'confirmPayError2' : True}    
        return render_to_response('home.html', context_dict, context)

    try:
        amount = Decimal(request.POST['payAmount'])
    except:  
        paygroup_list = currPayUser.payGroups.all()
        groupform = MakeGroupForm()
        payform = PayForm()
        context_dict={'PayForm' : payform, 'paygroups' : paygroup_list, 'MakeGroupForm' : groupform, 'confirmPayError1' : True}    
        return render_to_response('home.html', context_dict, context)

    if amount > (Decimal(-1) * targetFellow.owed) or amount <= Decimal(0):
    	paygroup_list = currPayUser.payGroups.all()
        groupform = MakeGroupForm()
        payform = PayForm()
        context_dict={'PayForm' : payform, 'paygroups' : paygroup_list, 'MakeGroupForm' : groupform, 'confirmPayError1' : True}    
        return render_to_response('home.html', context_dict, context)

    targetFellow.owed += amount
    targetFellow.save()
    memV.netOwed += amount
    memV.save()
    targetMem.netOwed -= amount
    targetMem.save()
    myFellow.owed -= amount
    myFellow.save()

    paygroup_list = currPayUser.payGroups.all()
    groupform = MakeGroupForm()
    payform = PayForm()
    context_dict={'PayForm' : payform, 'paygroups' : paygroup_list, 'MakeGroupForm' : groupform}    
    return render_to_response('home.html', context_dict, context)
