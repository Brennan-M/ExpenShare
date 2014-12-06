#ExpenShare 
**Software Engineering Methods and Tools 2014**

ExpenShare is an online application designed to help people split costs and share expenses. You can now create one or more group(s) with your friends and log your transactions, then let ExpenShare do the work and calculate how much each group member owes each other. This application can be used for roommates to split living expenses, friends to split travel costs, or any other necessary use!

Check out the [finished product](http:www.google.com)!

##Contributors
Taylor Andrews, Ian Char, and Brennan McConnell

##Dependencies
 * [django](https://www.djangoproject.com/)

##Folders
```
└── Expenshare
    └── doc               # Folder containing the documentation.
    |	├── html          # Documentation in html format.
    |   |   └── search
    |   └── latex         # Documentation in latex format.
    ├── Expenshare        # Contains the ExpenShare project.
    |	├── Expenshare    # Contains files that determine overall ExpenShare settings.
    |	├── share         # Contains Django framework models, views, and forms. 
    |   |   └── migrations
    |	├── static        # Static tools used in conjunction with Django. 
    |   |   ├── bootstrap # Contains bootstrap for ExpenShare.
    |   |   |   ├── css
    |   |   |   ├── fonts
    |   |   |   └── js
    |   |   ├── css       # Contains css file for ExpenShare.
    |   |   └── js        # Contains js file for ExpenShare.
    |   └── templates     # Html for the ExpenShare website.
```

##Files
| File                    | Details                                  |
| ----------------------- | ---------------------------------------- |
| ExpenshareERDiagram.pdf | ER diagram for ExpenShare database       |
| refman.pdf              | Latex generated output for documentation |
| manage.py               | Launches the ExpenShare websie           | 
| populate.py             | Populates the ExpenShare database        |
| settings.py             | Overall settings for the website         |
| forms.py                | Implementation of Django forms           |
| models.py               | Implementation of Django models          |
| views.py                | Implementation of Django views           |
| urls.py                 | Determines format of website urls        |
| home.html               | Expenshare user homepage                 |
| login.html              | Login page for users                     |
| ExpenseLog.html         | Log of expenses for a particular group   |
| register.html           | Registration page for new users          |

**Note:** More files are contained in the project, only the critical ones are listed above. 

##Documentation
Create documentation using latex:
```
cd doc/latex
make
```

##Usage

#### 1. Install dependencies
```
git clone https://github.com/django/django.git
```

#### 2. Run manage.py
```
cd Expenshare
python manage.py runserver
```

#### 3. Open localhost in browser

##Tests
Run tests using: 

```
cd Expenshare
python manage.py test
```













