from flask import Flask
from flaskext.mysql import MySQL


# http://flask-mysql.readthedocs.org/en/latest/
# MySQL - Flask documentation

# CREATE DATABASE Dispensary;
# CREATE TABLE User(userId INT NOT NULL AUTO_INCREMENT,userName VARCHAR(100) NOT NULL,password VARCHAR(40) NOT NULL,PRIMARY KEY(userId));
# insert into User values('1','Admin','admin');

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'Dispensary'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 3306 # 3306 by default
mysql.init_app(app)

@app.route("/Authenticate")
def Authenticate():
	username = request.args.get('UserName')
	password = request.args.get('Password')
	cursor = mysql.connect().cursor()
	cursor.execute("SELECT * from User where Username='" + username + "' and Password='" + password + "'")
	data = cursor.fetchone()
	if data is None:
		return "Username or Password is wrong"
	else:
		return "Logged in successfully"

@app.route("/")
def hello():
	return "Welcome to Python Flask App!"

if __name__ == "__main__":
	app.run()