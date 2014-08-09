NIT-Warangal Dispensary Management System
=========================================

- [x] v1.0 Released. ; 6th June 2014

Expected Deployment date : 20th July 2014

This project is an effort to reduce the amount of paperwork thats used in the dispensary system at NIT-Warangal. It aims to computerize the process of a student/professor getting their medication and at the same time serve as a validation system to pharmacy medication and inventory system.

### Development Set Up
-----------------------
##### Mac OS X and Linux

```
1. Go to the required folder , eg. ~/Documents
2. git clone https://github.com/NIT-Warangal/DispensaryMS
3. cd DispensaryMS
4. virtualenv venv
5. source venv/bin/activate
6. pip install -r requirements.txt
7. open the config.py file and set the required files.
8. Open mysql and set up the database and sync the .sql file
9. Open a new terminal tab and enter into venv as in step 5
10. sudo python -m smtpd -n -c DebuggingServer localhost:25
11. Switch back to the previous tab while keeping this running.
12. python Dispensary.py
```
-----------------------
##### Windows setup
```
1. Open cmd in administrator mode.
2. Type "pip install flask".
3. Type "pip install -r requirements.txt".
4. Type "pip install flask-mysql" (if its fails do step 5 )
5. Download connecter from http://www.codegood.com/
6. Go to project folder and type "python server.py"

(It may show some errors for some dependencies)
1. Type "pip install -r requirements.txt".
2. Type "python server.py"
(Assumed the SQL using is XAMPP's MYSQL)

```
-----------------------

### Server Deployment
#### For best use a Ubuntu server or a CentOS server
```
1. Follow the same development setup
2. open screen mode in terminal
3. run python Dispensary.py
```

