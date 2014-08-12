import os,binascii
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from flaskext.mysql import MySQL
from config import config, ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD

app = Flask(__name__)

for key in config:
    app.config[key] = config[key]

mysql = MySQL()

def get_cursor():
	return mysql.connect().cursor()

def logintest():
	db = get_cursor()
	for i in range(1,100):
		EmpID=i
		UserName = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(10)])
		Password = binascii.b2a_hex(os.urandom(15))
		Occupation = i%5
		sql = 'insert into Login values ("%s","%s",MD5("%s"),"%s")'
		db.execute(sql%(EmpID,UserName,Password,Occupation))
		db.execute("Commit")

logintest()