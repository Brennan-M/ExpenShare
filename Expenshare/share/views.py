##
# @file views.py
# @brief Contains the functions which implement all the logic behind ExpenShare.
#        Each view handles various http requests and returns appropriate responses.
# @authors Taylor Andrews, Ian Char, Brennan McConnell
# @date 11/26/2014
#

from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from share.models import PayUser, PayGroup, PaymentLog, MemberView, FellowUser
from share.forms import UserForm, PayForm, MakeGroupForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from decimal import Decimal

##
# @brief Returns the default ExpenShare page.
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
# @brief Displays the home page for the current User.
# @details Home displays any paygroups an user is in.
#          It allows a user to report new expenses and create new groups.
# @param request An http request from ExpenShare
# @return Redirects to home page
#
@login_required
def home(request):
    context = RequestContext(request)

    #Find the current PayUser
    curr_pay_user = PayUser.objects.get(userKey=request.user)
    paygroup_list = curr_pay_user.payGroups.all()
    payform = PayForm()
    groupform = MakeGroupForm()
    context_dict = {'PayForm' : payform, 'paygroups' : paygroup_list, 'MakeGroupForm' : groupform}

    return render_to_response('home.html', context_dict, context)

##
# @brief Displays the history webpage which shows all previous expenses for a specific group.
# @details The page checks the current group the user has chosen and
#          shows the expense history of that group.
#          This is on the ExpenseLog.html page.
# @param request An http request from ExpenShare
# @return Directs to expense history unless user cannot acces that group
#
@login_required
def history(request):
    context = RequestContext(request)

    curr_pay_user = PayUser.objects.get(userKey=request.user)
    paygroup_list = curr_pay_user.payGroups.all()
    payform = PayForm()
    groupform = MakeGroupForm()

    try:
        curr_group = PayGroup.objects.get(name=request.POST['group'])
        part_of = False
    except:
        context_dict = {'PayForm' : payform,
                        'paygroups' : paygroup_list,
                        'MakeGroupForm' : groupform, 'history_error1' : True}
        return render_to_response('home.html', context_dict, context)

    if curr_group in curr_pay_user.payGroups.all():
        part_of = True

    if part_of == False:
        context_dict = {'PayForm' : payform,
                        'paygroups' : paygroup_list,
                        'MakeGroupForm' : groupform, 'history_error2' : True}
        return render_to_response('home.html', context_dict, context)

    paylog_list = curr_group.paymentLogs.order_by('-date')
    context_dict = {'paylog': paylog_list, 'group': curr_group}
    return render_to_response('ExpenseLog.html', context_dict, context)

##
# @brief This function is used for registering new users.
# @details This function is used to register a new user to the expenshare site.
#          It creates a User Model for an individual when they sign up on the register.html page.
# @param request An http request from ExpenShare
# @return Redirects to next step in registration unless an error occured
#
def register(request):
    context = RequestContext(request)

    #Boolean value saying whether registration was successful or not
    registered = False

    if request.method == 'POST':
        #Attempt to get raw information
        user_form = UserForm(data=request.POST)

        #If getting the information was successful...
        if user_form.is_valid():
            #Save to database
            user = user_form.save()
            #This hashes the users password for safe storage
            user.set_password(user.password)
            user.save()
            #Make a new PayUser account
            pay_user = PayUser(userKey=user)
            pay_user.save()

            registered = True

        else:
            pass

    #Else it was not HTTP POST so have a blank form
    else:
        user_form = UserForm()

    context_dict = {'userForm': user_form, 'registered': registered}

    return render_to_response('register.html', context_dict, context)

##
# @brief This function creates a new PayGroup.
# @details This function creates a new PayGroup and adds the user who created it to it.
# @param request An http request from ExpenShare
# @return Redirects home, passes an error if one occured
#
@login_required
def add_groupform(request):
    context = RequestContext(request)
    curr_pay_user = PayUser.objects.get(userKey=request.user)
    paygroup_list = curr_pay_user.payGroups.all()
    payform = PayForm()
    groupform = MakeGroupForm()
    context_dict = {'PayForm' : payform, 'paygroups' : paygroup_list, 'MakeGroupForm' : groupform}

    if request.method == 'POST':
        groupform = MakeGroupForm(request.POST)

        if groupform.is_valid():
            group = groupform.save()
            group.save()
            curr_pay_user = PayUser.objects.get(userKey=request.user)
            curr_pay_user.payGroups.add(group)
            group.members.add(request.user)
            mem_view = MemberView(user=request.user)
            mem_view.save()
            group.memberViews.add(mem_view)
              #After submitting the form, redirects the user back to the homepage
            return render_to_response('home.html', context_dict, context)

        else:
            context_dict = {'PayForm' : payform,
                            'paygroups' : paygroup_list,
                            'MakeGroupForm' : groupform,
                            'creategroup_error1' : True}
            return render_to_response('home.html', context_dict, context)

    context_dict = {'PayForm' : payform,
                    'paygroups' : paygroup_list,
                    'MakeGroupForm' : groupform}
    return render_to_response('home.html', context_dict, context)

##
# @brief Adds an expense to a group.
# @details Function implements adds a new paymentLog to a PayGroup.
#           The function updates the amount owed amongst the group members as the payment is added.
# @param request An http request from ExpenShare
# @return Redirects to expense history, if an error occured redirects home
#
@login_required
def add_payform(request):
    context = RequestContext(request)

    curr_pay_user = PayUser.objects.get(userKey=request.user)

    try:
        clicked_group = PayGroup.objects.get(name=request.POST['group'])
        part_of = False
    except:
        paygroup_list = curr_pay_user.payGroups.all()
        groupform = MakeGroupForm()
        context_dict = {'paygroups' : paygroup_list,
                        'MakeGroupForm' : groupform,
                        'payform_error2' : True}
        return render_to_response('home.html', context_dict, context)

    if clicked_group in curr_pay_user.payGroups.all():
        part_of = True

    if part_of == False:
        paygroup_list = curr_pay_user.payGroups.all()
        groupform = MakeGroupForm()
        context_dict = {'paygroups' : paygroup_list,
                        'MakeGroupForm' : groupform,
                        'payform_error3' : True}
        return render_to_response('home.html', context_dict, context)

    if request.method == 'POST':
        payform = PayForm(request.POST)

        if payform.is_valid():
            cost = payform.save(commit=False)
            cost.user = request.user
            cost.save()

            #Load the playlogs
            clicked_group.paymentLogs.add(cost)
            pay_logs = clicked_group.paymentLogs.order_by('date')

            #Calculate new cost of the group
            for mem_view in clicked_group.memberViews.all():
                if mem_view.user.id == request.user.id:
                    mem_view.netOwed = ((Decimal(mem_view.netOwed) -
                                         Decimal(clicked_group.groupSize - 1) *
                                         (Decimal(cost.amount) / Decimal(clicked_group.groupSize))))
                    for fels in mem_view.fellows.all():
                        fels.owed = ((Decimal(fels.owed) -
                                      (Decimal(cost.amount) /
                                       Decimal(clicked_group.groupSize))))
                        fels.save()
                else:
                    mem_view.netOwed = ((Decimal(mem_view.netOwed) +
                                         (Decimal(cost.amount) /
                                          Decimal(clicked_group.groupSize))))
                    for fels in mem_view.fellows.all():
                        if fels.user.id == request.user.id:
                            fels.owed = ((Decimal(fels.owed) +
                                          (Decimal(cost.amount) /
                                           Decimal(clicked_group.groupSize))))
                            fels.save()
                mem_view.save()
            return history(request)

        else:
            pay_logs = clicked_group.paymentLogs.order_by('date')
            context_dict = {'paylog' : pay_logs,
                            'group' : clicked_group,
                            'payform_error1' : True}
            return render_to_response('ExpenseLog.html', context_dict, context)
    else:
        payform = PayForm()

    paygroup_list = curr_pay_user.payGroups.all()
    groupform = MakeGroupForm()
    context_dict = {'PayForm' : payform,
                    'paygroups' : paygroup_list,
                    'MakeGroupForm' : groupform}
    return render_to_response('home.html', context_dict, context)

##
# @brief Function which allows a User to join an existing PayGroup.
# @details If the user correctly inputs the group name and passcode, the user is added to the
#          PayGroup requested.
# @param request An http request from ExpenShare
# @return Redirects user back to their homepage with the group joined or passes an error
#
@login_required
def joingroup_form(request):
    context = RequestContext(request)
    curr_pay_user = PayUser.objects.get(userKey=request.user)
    if request.method == 'POST':
        try:
            group = PayGroup.objects.get(name=request.POST['group'])
            passcode = request.POST['passcode']
            realcode = group.passcode
            if passcode == realcode:
                for mem_view in group.memberViews.all():
                    fell_mem = FellowUser(user=request.user)
                    fell_mem.save()
                    mem_view.fellows.add(fell_mem)
                newmem_view = MemberView(user=request.user)
                newmem_view.save()
                group.memberViews.add(newmem_view)
                for mems in group.members.all():
                    fell_mem = FellowUser(user=mems)
                    fell_mem.save()
                    newmem_view.fellows.add(fell_mem)
                group.members.add(request.user)
                curr_pay_user.payGroups.add(group)
                group.groupSize += 1
                group.save()
            else:
                paygroup_list = curr_pay_user.payGroups.all()
                groupform = MakeGroupForm()
                payform = PayForm()
                context_dict = {'PayForm' : payform,
                                'paygroups' : paygroup_list,
                                'MakeGroupForm' : groupform,
                                'joingroup_error1' : True}
                return render_to_response('home.html', context_dict, context)

            paygroup_list = curr_pay_user.payGroups.all()
            groupform = MakeGroupForm()
            payform = PayForm()
            context_dict = {'PayForm' : payform,
                            'paygroups' : paygroup_list,
                            'MakeGroupForm' : groupform}
            return render_to_response('home.html', context_dict, context)
        except:
            pass

    paygroup_list = curr_pay_user.payGroups.all()
    groupform = MakeGroupForm()
    payform = PayForm()
    context_dict = {'PayForm' : payform,
                    'paygroups' : paygroup_list,
                    'MakeGroupForm' : groupform,
                    'joingroup_error2' : True}
    return render_to_response('home.html', context_dict, context)

##
# @brief Function which makes a user leave a PayGroup upon request.
# @details Pending eligibility, allows a PayUser to leave a Paygroup. If the PayGroup no longer has
#          any members, it is deleted.
# @param request An http request from ExpenShare
# @return Directs user to their homepage with group removed, passes an error if one occured
#
@login_required
def leavegroup(request):
    context = RequestContext(request)
    curr_pay_user = PayUser.objects.get(userKey=request.user)
    if request.method == 'POST':
        try:
            group = PayGroup.objects.get(name=request.POST['group'])

            #Determine if the user can leave or not
            can_leave = True
            mem_view = group.memberViews.get(user=request.user)
            if mem_view.netOwed != 0:
                can_leave = False
            else:
                for fel in mem_view.fellows.all():
                    if fel.owed != 0:
                        can_leave = False
                        break

            #Remove the user from the group
            if can_leave:
                for fel in mem_view.fellows.all():
                    fel.delete()
                for mem in group.memberViews.all():
                    if mem != mem_view:
                        for fel in mem.fellows.all():
                            if fel.user == mem_view.user:
                                fel.delete()
                mem_view.delete()
                group.members.remove(request.user)
                curr_pay_user.payGroups.remove(group)
                group.groupSize -= 1
                if not group.members.exists():
                    group.delete()
                    paygroup_list = curr_pay_user.payGroups.all()
                    groupform = MakeGroupForm()
                    payform = PayForm()
                    context_dict = {'PayForm' : payform,
                                    'paygroups' : paygroup_list,
                                    'MakeGroupForm' : groupform,
                                    'deleted_group' : True}
                    return render_to_response('home.html', context_dict, context)
                else:
                    paygroup_list = curr_pay_user.payGroups.all()
                    groupform = MakeGroupForm()
                    payform = PayForm()
                    context_dict = {'PayForm' : payform,
                                    'paygroups' : paygroup_list,
                                    'MakeGroupForm' : groupform}
                    group.save()
                    return render_to_response('home.html', context_dict, context)
            else:
                context_dict = {'PayForm' : payform,
                                'paygroups' : paygroup_list,
                                'MakeGroupForm' : groupform,
                                'leavegroup_error1' : True}
                return render_to_response('home.html', context_dict, context)
        except:
            print "Error leaving Group."

    paygroup_list = curr_pay_user.payGroups.all()
    groupform = MakeGroupForm()
    payform = PayForm()
    context_dict = {'PayForm' : payform,
                    'paygroups' : paygroup_list,
                    'MakeGroupForm' : groupform,
                    'leavegroup_error1' : True}
    return render_to_response('home.html', context_dict, context)

##
# @brief Logs a user into their ExpenShare profile.
# @details Allows an existing ExpenShare user to access their profile.
# @param request An http request from ExpenShare
# @return Redirects user to their homepage, passes an error if one occured
#
def user_login(request):
    context = RequestContext(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        #Check to see if a user with the submitted credentials was found
        if user:
            #Check to see if the user account is active
            if user.is_active:
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
# @brief Logs a User out.
# @param request An http request from ExpenShare
# @return Http redirect to the homepage
#
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/share/')

##
# @brief Confirms that a PayUser has received payment for existing expenses by a fellow member
#        of the group.
# @details Allows user to specify which member of the group they are reporting as having paid them
#          back. Updates the amount owed between users and the group.
# @param request An http request from ExpenShare
# @return Redirects user to their homepage, will pass an error if one occured
#
@login_required
def confirm_payment(request):
    context = RequestContext(request)

    group = PayGroup.objects.get(name=request.POST['group'])
    curr_pay_user = PayUser.objects.get(userKey=request.user)
    try:
        mem_view = group.memberViews.get(user=request.user)
        target_user = User.objects.get(username=request.POST['target_member'])
        target_mem = group.memberViews.get(user=target_user)
        my_fellow = target_mem.fellows.get(user=request.user)
        target_fellow = mem_view.fellows.get(user=target_user)
    except:
        paygroup_list = curr_pay_user.payGroups.all()
        groupform = MakeGroupForm()
        payform = PayForm()
        context_dict = {'PayForm' : payform,
                        'paygroups' : paygroup_list,
                        'MakeGroupForm' : groupform,
                        'confirmPayError2' : True}
        return render_to_response('home.html', context_dict, context)

    try:
        amount = Decimal(request.POST['payAmount'])
    except:
        paygroup_list = curr_pay_user.payGroups.all()
        groupform = MakeGroupForm()
        payform = PayForm()
        context_dict = {'PayForm' : payform,
                        'paygroups' : paygroup_list,
                        'MakeGroupForm' : groupform,
                        'confirmPayError1' : True}
        return render_to_response('home.html', context_dict, context)

    if amount > (Decimal(-1) * target_fellow.owed) or amount <= Decimal(0):
        paygroup_list = curr_pay_user.payGroups.all()
        groupform = MakeGroupForm()
        payform = PayForm()
        context_dict = {'PayForm' : payform,
                        'paygroups' : paygroup_list,
                        'MakeGroupForm' : groupform,
                        'confirmPayError1' : True}
        return render_to_response('home.html', context_dict, context)

    target_fellow.owed += amount
    target_fellow.save()
    mem_view.netOwed += amount
    mem_view.save()
    target_mem.netOwed -= amount
    target_mem.save()
    my_fellow.owed -= amount
    my_fellow.save()

    paygroup_list = curr_pay_user.payGroups.all()
    groupform = MakeGroupForm()
    payform = PayForm()
    context_dict = {'PayForm' : payform,
                    'paygroups' : paygroup_list,
                    'MakeGroupForm' : groupform}
    return render_to_response('home.html', context_dict, context)

##
# @brief Removes a payment from a group.
# @details Removes an expense from a PayGroup and removes it from the expense history log.
#          Then recalculates the balances owed between group members
# @param request An http request from ExpenShare
# @return Redirect user to the expense history, passes an error if one occured
#
@login_required
def remove_payform(request):
    context = RequestContext(request)
    context_dict = {}
    user = request.user

    if request.method == 'POST':
        try:
            group = PayGroup.objects.get(name=request.POST['group'])
            paylog = PaymentLog.objects.get(id=request.POST['log'])
            exists = False
            owner = False

            if paylog in group.paymentLogs.all():
                exists = True
            if paylog.user == user:
                owner = True
            else:
                paylog_list = group.paymentLogs.order_by('-date')
                groupform = MakeGroupForm()
                context_dict = {'paylog': paylog_list, 'group': group, 'deletePFError2' : True}
                return render_to_response('ExpenseLog.html', context_dict, context)

            if exists == True and owner == True:
                for mem_view in group.memberViews.all():
                    if mem_view.user.id == request.user.id:
                        mem_view.netOwed = ((Decimal(mem_view.netOwed) +
                                             Decimal(group.groupSize - 1) *
                                             (Decimal(paylog.amount) /
                                              Decimal(group.groupSize))))
                        for fels in mem_view.fellows.all():
                            fels.owed = ((Decimal(fels.owed) +
                                          (Decimal(paylog.amount) /
                                           Decimal(group.groupSize))))
                            fels.save()
                    else:
                        mem_view.netOwed = ((Decimal(mem_view.netOwed) -
                                             (Decimal(paylog.amount) /
                                              Decimal(group.groupSize))))
                        for fels in mem_view.fellows.all():
                            if fels.user.id == request.user.id:
                                fels.owed = ((Decimal(fels.owed) -
                                              (Decimal(paylog.amount) /
                                               Decimal(group.groupSize))))
                                fels.save()
                    mem_view.save()
                group.paymentLogs.remove(paylog)
                paylog.delete()
            else:
                paylog_list = group.paymentLogs.order_by('-date')
                context_dict = {'paylog': paylog_list,
                                'group': group,
                                'deletePFError1' : True}
                return render_to_response('ExpenseLog.html', context_dict, context)

        except:
            paylog_list = group.paymentLogs.order_by('-date')
            context_dict = {'paylog': paylog_list,
                            'group': group,
                            'deletePFError1' : True}
            return render_to_response('ExpenseLog.html', context_dict, context)

    paylog_list = group.paymentLogs.order_by('-date')
    groupform = MakeGroupForm()
    context_dict = {'paylog': paylog_list, 'group': group}
    return render_to_response('ExpenseLog.html', context_dict, context)
