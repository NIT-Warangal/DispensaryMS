# Database Config

config = {
	'MYSQL_DATABASE_USER' : 'root',
	'MYSQL_DATABASE_DB' : 'Dispensary1',
	'MYSQL_DATABASE_PASSWORD' : 'root',
	'MYSQL_DATABASE_HOST' : 'localhost', 
	'USERNAME' : '',
	'USERID' :'',
}

# To run the mail server run
# sudo python -m smtpd -n -c DebuggingServer localhost:25
# mail server settings

MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USERNAME = None
MAIL_PASSWORD = None

# Administrator list
ADMINS = ['you@example.com']