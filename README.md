#ExpenShare 
**Software Engineering Methods and Tools 2014**

ExpenShare is an online application designed to help people split costs and share expenses. You can now create one or more group(s) with your friends and log your transactions, then let ExpenShare do the work and calculate how much each group member owes each other. This application can be used for roommates to split living expenses, friends to split travel costs, or any other necessary use!

Check out the finished product at http://expen-share.herokuapp.com/share/
See a video dem at https://www.youtube.com/watch?v=WwXUiUC29nI

##Contributors
Taylor Andrews, Ian Char, and Brennan McConnell

##Dependencies
 * Django==1.7.1
 * dj-database-url==0.3.0
 * dj-static==0.0.6
 * gunicorn==19.1.1
 * psycopg2==2.5.1
 * static==0.4
 * wsgiref==0.1.2
 * simplejson==3.6.2
 * Pillow==2.3.0

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
    |   ├── db.sqlite3
    |   ├── Procfile            # Contains execution information for Heroku
    |   ├── requirements.txt    # Requirements to run app on Heroku
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

##Usage - Build and Run Locally
#### 1. Install dependencies
```
cd Expenshare
pip install -r requirements.txt
```
#### 2. Change DATABASES
Change DATABASES in Expenshare/settings.py to the following so that it uses SQLite3:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'db.sqlite3'                      # Or path to database file if using sqlite3.
    }
}
```
Additionally, at the top of the same document make the following change:
```
STATIC_ROOT = 'static'
```
Then run the following code in the terminal in Expenshare/Expenshare:
```
python manage.py syncdb
python manage.py makemigrations
pyton manage.py migrate
```
**Note:** this may require you to install and setup your own Postgre database. In order to do this follow steps 4 and 7 [here.](https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-django-with-postgres-nginx-and-gunicorn)

#### 3. Run manage.py
In the terminal, type the following command in Expenshare/Expenshare
```
python manage.py runserver
```

#### 4. Open localhost in browser
Expenshare can then be found at http://127.0.0.1:8000/share/

##Tests
Once you have gotten Expenshare running locally you can run tests in Expenshare/Expenshare by:
```
python manage.py test
```
