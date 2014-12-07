#ExpenShare 
**Software Engineering Methods and Tools 2014**

ExpenShare is an online application designed to help people split costs and share expenses. You can now create one or more group(s) with your friends and log your transactions, then let ExpenShare do the work and calculate how much each group member owes each other. This application can be used for roommates to split living expenses, friends to split travel costs, or any other necessary use!

Check out the [finished product](http:www.google.com)!

##Contributors
Taylor Andrews, Ian Char, and Brennan McConnell

##Dependencies
 * [django](https://www.djangoproject.com/)

##Repository Organization
```
└── Expenshare
    ├── ERDiagrams              # Folder containing the ER diagrams for ExpenShares database.
    |   └── ExpenshareER.pdf
    ├── Expenshare              # Contains the ExpenShare project.
    |	├── Expenshare          # Contains files that determine overall ExpenShare settings.
    |	├── share               # Contains main Source Code.
    |   |   ├── migrations
    |   |   ├── admin.py
    |   |   ├── urls.py
    |   |   ├── forms.py        
    |   |   ├── models.py       # Contains the models used in Expenshare's database.
    |   |   ├── views.py        # Contains bulk of source code, and functions used in ExpenShare.
    |	├── static              # Static tools used in conjunction with Django. 
    |   |   ├── bootstrap       # Contains bootstrap for ExpenShare.
    |   |   |   ├── css
    |   |   |   ├── fonts
    |   |   |   └── js
    |   |   ├── css             # Contains css file for ExpenShare.
    |   |   |   └── styles.css  # CSS file for ExpenShare webpages.
    |   |   └── js              # Contains js file for ExpenShare.
    |   ├── templates           # Html for the ExpenShare website.
    |   |   ├── Expenselog.html
    |   |   ├── home.html
    |   |   ├── login.html
    |   |   └── register.html
    |   ├── manage.py
    |   ├── populate.py
    |   └── tests.py            # Automated test cases for testing ExpenShare. Uses Pythons Unittest Module.
    ├── doc                     # Folder containing the documentation.
    |	├── html                # Contains doxygen generated HTML files for online browsable documentation.
    |   ├── latex               # Documentation in latex format.
    |   └── refman.pdf          # Generated documentation pdf file.
```

##Files
| File                    | Details                                  |
| ----------------------- | ---------------------------------------- |
| ExpenshareER.pdf        | ER diagram for ExpenShare database       |
| refman.pdf              | Latex generated output for documentation |
| manage.py               | Launches the ExpenShare website          | 
| populate.py             | Populates the ExpenShare database        |
| settings.py             | Overall settings for the website         |
| forms.py                | User Forms on ExpenShare website         |
| models.py               | ExpenShare Database Models               |
| views.py                | The Functions Behind ExpenShare          |
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
Find documentation under ExpenShare/doc
```
-- Refer to the html folder for doxygen html generated online browsable documentation.
-- Refer to redman.pdf for a pdf file of ExpenShare's documentation.
```

##Usage - Build and Run
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













