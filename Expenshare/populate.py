import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Expenshare.settings')
import django
django.setup()

from share.models import User
from share.models import PayGroup
from share.models import PaymentLog
from share.models import PayUser
from share.models import MemberView
from share.models import FellowUser

def populate():
	ian = User(username="Ian")
	bren = User(username="Brennan")
	tay = User(username="Taylor")
	andy = User(username="Andy")
	gregg = User(username="Old Gregg")
	ian.set_password("1234")
	bren.set_password("1234")
	tay.set_password("1234")
	andy.set_password("1234")
	gregg.set_password("1234")
	ian.save()
	bren.save()
	tay.save()
	andy.save()
	gregg.save()

	ian = PayUser(userKey=ian)
	bren = PayUser(userKey=bren)
	tay = PayUser(userKey=tay)
	andy = PayUser(userKey=andy)
	gregg = PayUser(userKey=gregg)
	ian.save()
	bren.save()
	tay.save()
	andy.save()
	gregg.save()

	pg1 = PayGroup(name="Group 1", description="Group for all users", passcode="group1")
	pg2 = PayGroup(name="Group 2", description="Group for Ian, Brennan, Taylor", passcode="group2")
	pg3 = PayGroup(name="Group 3", description="Group for Andy and Old Gregg", passcode="group3")
	pg1.save()
	pg2.save()
	pg3.save()

	pg1.members.add(ian.userKey)
	pg1.members.add(bren.userKey)
	pg1.members.add(tay.userKey)
	pg1.members.add(andy.userKey)
	pg1.members.add(gregg.userKey)
	
	pg2.members.add(ian.userKey)
	pg2.members.add(bren.userKey)
	pg2.members.add(tay.userKey)	

	pg3.members.add(andy.userKey)
	pg3.members.add(gregg.userKey)

	ian.payGroups.add(pg1)
	ian.payGroups.add(pg2)
	bren.payGroups.add(pg1)
	bren.payGroups.add(pg2)
	tay.payGroups.add(pg1)
	tay.payGroups.add(pg2)
	andy.payGroups.add(pg1)
	andy.payGroups.add(pg3)
	gregg.payGroups.add(pg1)
	gregg.payGroups.add(pg3)

	tmp = MemberView(user=ian.userKey)
	tmp.save()

	for g in PayGroup.objects.all():
		for mem in g.members.all():
			memV = MemberView(user=mem)
			memV.save()
			for fmem in g.members.all():
				if(mem.id != fmem.id):
					fellU = FellowUser(user=fmem)
					fellU.save()
					memV.fellows.add(fellU)
			g.memberViews.add(memV)

	pl1 = PaymentLog(amount=10, description="Bought some eggs", user=ian.userKey)
	pl2 = PaymentLog(amount=20, description="Bought gas", user=bren.userKey)
	pl3 = PaymentLog(amount=30, description="Bought some ham", user=gregg.userKey)
	pl4 = PaymentLog(amount=40, description="Bought some soap", user=tay.userKey)
	pl1.save()
	pl2.save()
	pl3.save()
	pl4.save()

	pg1.paymentLogs.add(pl1)
	pg1.paymentLogs.add(pl2)
	pg1.paymentLogs.add(pl4)
	pg3.paymentLogs.add(pl3)




if __name__=='__main__':
	print("Populating databse...")
	populate()
	print("Done!")