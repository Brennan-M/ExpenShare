import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Expenshare.settings')
import django
django.setup()

from share.models import Group
from share.models import User
from share.models import PayGroup
from share.models import PaymentLog
from share.models import groupRequest

def populate():
	usr1 = User(username="User 1")
	usr2 = User(username="User 2")
	usr3 = User(username="User 3")
	usr1.save()
	usr2.save()
	usr3.save()

	grp1 = Group(name="Group 1")
	grp2 = Group(name="Group 2")
	grp1.save()
	grp2.save()

	pg1 = PayGroup(name=grp1, description="Group 1 descrip")
	pg2 = PayGroup(name=grp2, description="Group 2 descrip")
	pg1.save()
	pg2.save()

	pl1 = PaymentLog(amount=10, description="Group 1", group=pg1, user=usr1)
	pl2 = PaymentLog(amount=20, description="Group 2", group=pg2, user=usr3)
	pl1.save()
	pl2.save()

if __name__=='__main__':
	print("Populating database...")
	populate()
	print("Done!")
