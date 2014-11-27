##
# @file views.py
# @brief Each view handles various http requests and returns appropriate responses
# @authors Taylor Andrews, Ian Char, Brennan McConnell
# @date 11/26/2014
#

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
from django.views.decorators.csrf import csrf_protect
from django.template.defaulttags import csrf_token

##
# @brief Default ExpenShare page
# @param request An http request from ExpenShare
# @return Redirects to login
#
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
    
##
# @brief Displays the home page for the current PayUser
# @details Home displays any paygroups an user is in. It allows them to make payments and groups. 
# @param request An http request from ExpenShare
# @return Redirects to home page
#
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

##
# @brief History of expenses between users in a specific paygroup
# @details The page checks the current group the user has chosen and shows the expense history of that group. This is on the ExpenseLog.html page. 
# @param request An http request from ExpenShare
# @return Directs to expense history unless user cannot acces that group
#
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

##
# @brief View for registering new users
# @details This function is used to register a new user to the expenshare site. It creates a User Model for an individual when they sign up on the register.html page.
# @param request An http request from ExpenShare
# @return Redirects to next step in registration unless an error occured
#
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

##
# @brief Allows an user to create a new group
# @details If the group is created correctly it will automatically add the user to the group. The function uses the MakeGroupForm form. 
# @param request An http request from ExpenShare
# @return Redirects home, passes an error if one occured
#
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

##
# @brief Adds a payment into a paygroup
# @details Ensures the user is actually in the group specified. The function updates the amount owed amongst the group members as the payment is added. 
# @param request An http request from ExpenShare
# @return Redirects to expense history, if an error occured redirects home
#
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
            return history(request)
    
        else:
            payLogs = clickedGroup.paymentLogs.order_by('date')
            return render_to_response('ExpenseLog.html', {'paylog' : payLogs, 'group' : clickedGroup, 'payform_error1' : True}, context)
    else:
        payform = PayForm()
    
    paygroup_list = currPayUser.payGroups.all()
    groupform = MakeGroupForm()
    context_dict={'PayForm' : payform, 'paygroups' : paygroup_list, 'MakeGroupForm' : groupform}    
    return render_to_response('home.html', context_dict, context)

##
# @brief Loads a page for the user to join a group
# @details If the user correctly inputs the group name and passcode that group is immediately added to their homepage. 
# @param request An http request from ExpenShare
# @return Redirects user back to their homepage with the group joined or passes an error
#
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

##
# @brief Allows the user to leave a group
# @details The function first determines if the user is even eligible to leave the group. If they are it deletes them from the group. If they are the last member of a group that group is removed. 
# @param request An http request from ExpenShare
# @return Directs user to their homepage with group removed, passes an error if one occured
#
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

##
# @brief Logs an user in 
# @details Errors include logging into an account that is no longer active.
# @param request An http request from ExpenShare
# @return Redirects user to their homepage, passes an error if one occured
#
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

##
# @brief Handles user logout
# @param request An http request from ExpenShare
# @return Http redirect to the homepage
#
@login_required
def userLogout(request):
	logout(request)
	return HttpResponseRedirect('/share/')

##
# @brief Comfirms payment made by an user
# @details Allows user to specify which member of the group they are reporting as having paid them back. Updates the amount owed between users and the group immediately. 
# @param request An http request from ExpenShare
# @return Redirects user to their homepage, will pass an error if one occured
#
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

##
# @brief Removes a payment from a group
# @details Errors include trying to delete someone else's payment or a payment that doesn't exist.
# @param request An http request from ExpenShare
# @return Redirect user to the expense history, passes an error if one occured
#
@login_required
def removePayForm(request):
    context = RequestContext(request)
    context_dict = {}
    user = request.user

    if (request.method=='POST'):
        try:
            group = PayGroup.objects.get(name=request.POST['group'])
            paylog = PaymentLog.objects.get(id=request.POST['log'])
            Exists=False
            Owner=False

            if paylog in group.paymentLogs.all():
                Exists=True
            if paylog.user == user:
                Owner=True
            else:
                paylog_list = group.paymentLogs.order_by('-date')
                groupform = MakeGroupForm()
                context_dict = {'paylog': paylog_list, 'group': group, 'deletePFError2' : True}
                return render_to_response('ExpenseLog.html', context_dict, context)

            if Exists==True and Owner==True:
                for memV in group.memberViews.all():
                    if memV.user.id == request.user.id:
                    	memV.netOwed = ((Decimal(memV.netOwed) + Decimal(group.groupSize - 1) * (Decimal(paylog.amount) / Decimal(group.groupSize))))
                        for fels in memV.fellows.all():
                            fels.owed = ((Decimal(fels.owed) + (Decimal(paylog.amount) / Decimal(group.groupSize))))
                            fels.save()
                    else:
                        memV.netOwed = ((Decimal(memV.netOwed) - (Decimal(paylog.amount) / Decimal(group.groupSize))))
                        for fels in memV.fellows.all():
                            if fels.user.id == request.user.id:
                                fels.owed = ((Decimal(fels.owed) - (Decimal(paylog.amount) / Decimal(group.groupSize))))
                                fels.save()
                    memV.save()
                group.paymentLogs.remove(paylog)
                paylog.delete()
            else:
                paylog_list = group.paymentLogs.order_by('-date')
                context_dict = {'paylog': paylog_list, 'group': group, 'deletePFError1' : True}
                return render_to_response('ExpenseLog.html', context_dict, context)
        
        except:
            paylog_list = group.paymentLogs.order_by('-date')
            context_dict = {'paylog': paylog_list, 'group': group, 'deletePFError1' : True}
            return render_to_response('ExpenseLog.html', context_dict, context)

    paylog_list = group.paymentLogs.order_by('-date')
    groupform = MakeGroupForm()
    context_dict = {'paylog': paylog_list, 'group': group}
    return render_to_response('ExpenseLog.html', context_dict, context)
