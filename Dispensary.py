# all the imports
import os
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from flaskext.mysql import MySQL
import datetime
<<<<<<< HEAD
import subprocess
=======
>>>>>>> 8a81dc1a9a630eb94b07915f11a077ec56151f19
 
mysql = MySQL()
# create our little application :)
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
<<<<<<< HEAD
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
=======
app.config['MYSQL_DATABASE_PASSWORD'] = 'kiran123'
>>>>>>> 8a81dc1a9a630eb94b07915f11a077ec56151f19
app.config['MYSQL_DATABASE_DB'] = 'Dispensary'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
app.config.from_object(__name__)
app.config['USERNAME']=''
<<<<<<< HEAD

=======
>>>>>>> 8a81dc1a9a630eb94b07915f11a077ec56151f19

def get_cursor():
    return mysql.connect().cursor()

@app.teardown_appcontext
def close_db(cursor):
    """Closes the database again at the end of the request."""
    mysql.connect().close()
<<<<<<< HEAD

=======
>>>>>>> 8a81dc1a9a630eb94b07915f11a077ec56151f19
@app.route('/')
def show_entries():
    db = get_cursor()
    db.execute('select title, text from entries order by id desc')
    entries = db.fetchall()
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST']) #add
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_cursor()
<<<<<<< HEAD
    db.execute('insert into Users (Sno, RegNo, \'FirstName\', \'MiddleName\',\'LastName\', \'BloodGroup\', \'DateofBirth\', Age, Type, \'Phonenumber\', Address, email) values (?,?,?,?,?,?,?,?,?,?,?,?)',
        [request.form['Sno'], request.form['RegNo'],request.form['FirstName'],request.form['MiddleName'],request.form['LastName'],request.form['BloodGroup'],request.form['DateOfBirth'],request.form['Age'],request.form['Type'],request.form['PhoneNumber'],request.form['text'],request.form['email']])
    db.commit()
=======
    sno=request.form['Sno']
    regno= request.form['RegNo']
    fname=request.form['FirstName']
    mname=request.form['MiddleName']
    lname=request.form['LastName']
    bgroup=request.form['BloodGroup']
    dob=request.form['DateOfBirth']
    age=request.form['Age']
    typ=request.form['Type']
    phn=request.form['PhoneNumber']
    address=request.form['text']
    email=request.form['email']
    gender='Male'
    sql='insert into Users \
    (Sno, RegNo, FirstName, MiddleName,LastName, BloodGroup, DateofBirth, Age, Type, Phonenumber, Address,\
     email,gender) values (%s,%s,"%s","%s","%s","%s","%s",%s,%s,"%s","%s","%s","%s")'
    db.execute(sql%(sno,regno,fname,mname,lname,bgroup,dob,age,typ,phn,address,email,gender))
    db.execute("COMMIT")
>>>>>>> 8a81dc1a9a630eb94b07915f11a077ec56151f19
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))#show_entries

# @app.route('/reg', methods=['POST']) #reg
# def add_user():
#     if not session.get('logged_in'):
#         abort(401)
#     db = get_cursor()
<<<<<<< HEAD
#     db.execute('insert into Users (Sno, RegNo, First Name, Middle Name,Last Name, Blood Group, Date of Birth, Age, Type, Phone number, Address, email) values (?, ?,?,?,?,?,?,?,?,?,?,?)',
=======
#     db.execute('insert into Users (Sno, RegNo, First Name, Middle Name,Last Name, Blood Group, Date of Birth, Age, Type, Phone number, Address, email) values (%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
>>>>>>> 8a81dc1a9a630eb94b07915f11a077ec56151f19
#         [request.form['Sno'], request.form['RegNo'],request.form['FirstName'],request.form['MiddleName'],request.form['LastName'],request.form['BloodGroup'],request.form['DateOfBirth'],request.form['Age'],request.form['Type'],request.form['PhoneNumber'],request.form['text'],request.form['email']])

#     db.commit()
#     flash('New entry was successfully posted')
#     return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    db=get_cursor()
    if request.method == 'POST':
        uname=str(request.form['username'])
        pwd=str(request.form['password'])
        sql='select Count(*) from Login where UserName="%s" and Password="%s"'%(uname,pwd)
        db.execute(sql)
        data = db.fetchone()[0]
        if data ==0:
<<<<<<< HEAD
           error='Invalid username/password'
=======
            error='Invalid username/password'
>>>>>>> 8a81dc1a9a630eb94b07915f11a077ec56151f19
        else:
            session['logged_in'] = True
            app.config['USERNAME'] = uname
            flash('You were logged in'+app.config['USERNAME']+str(session['logged_in']))
        return redirect(url_for('show_entries'))
    return render_template('login.html', error=error) #login.html

t=0
@app.route('/inventory')
def inventory():
<<<<<<< HEAD
    db = get_cursor()
    db.execute('select * from Pharmacy order by Sno')
    entries = db.fetchall()
=======
    db=get_cursor()
    db.execute('select * from Pharmacy order by Sno')
    entries = db.fetchall()
    db.execute('commit')
>>>>>>> 8a81dc1a9a630eb94b07915f11a077ec56151f19
    return render_template('pharmventory.html',entries = entries)

@app.route('/insert',methods=['GET','POST'])
def insert():
    global t
    db=get_cursor()
    db.execute('select Count(1) from Pharmacy')
    t=db.fetchone()[0]
    flash(t)
    #t=db.fetchall[0][0]
    if request.form['btn'] == 'insert':
<<<<<<< HEAD
        sno = int(request.form['Sno'])
        name = str(request.form['Name'])
        quantity = int(request.form['qty'])
        batchno = request.form['bno']
        mfg = datetime.datetime.strptime(request.form['mfgdate'])
        exp = datetime.datetime.strptime(request.form['expdate'])
        db.execute('insert into Pharmacy values(%s,%s,%s,%s,%s,%s)'%(sno,name,quantity,batchno,mfg.isoformat(),exp.isoformat()))
=======
        sno = (request.form['Sno'])
        name = (request.form['Name'])
        quantity = (request.form['qty'])
        batchno = request.form['bno']
        flash(request.form['mfgdate']+' and '+request.form['expdate'])
        mfg=str(request.form['mfgdate'])
        year=int(mfg[0:4])
        month=int(mfg[5:7])
        date=int(mfg[8:10])
        mfg=datetime.date(year,month,date)
        exp = str(request.form['expdate'])
        year=int(exp[0:4])
        month=int(exp[5:7])
        date=int(exp[8:10])
        exp=datetime.date(year,month,date)
        sql = 'insert into Pharmacy values(%s,"%s",%s,%s,"%s","%s")'
        db.execute(sql%(sno,name,quantity,batchno,mfg,exp))
        db.execute("COMMIT")
>>>>>>> 8a81dc1a9a630eb94b07915f11a077ec56151f19
        flash('New entry successfully inserted')
        return redirect(url_for('inventory'))
    else:
        for i in range( 1, t+1):
            r = str(i)
            if request.form['btn'] == 'update' + r:
                sno=request.form['Sno' + r]
                name=request.form['Name' + r]
                quantity=request.form['qty' + r]
                batchno=request.form['bno' + r]
                mfg = request.form['mfgdate' + r]
<<<<<<< HEAD
                exp = request.form['expdate' + r]
                query = 'update pharmacy set Name=?,Quantity=?,Batchno=?,ManufactureDate=?,ExpiryDate=? where Sno=?'
                db.execute(query,[name,quantity,batchno,mfg,exp,sno])
                db.commit()
                flash('Record '+sno+' updated')
                return redirect(url_for('inventory'))       
            elif request.form['btn'] == 'delete' + r:
                sno=request.form['Sno' + r]
                query='delete from pharmacy where Sno=?'
                db.execute(query,[sno])
                db.commit()
=======
                year=int(mfg[0:4])
                month=int(mfg[5:7])
                date=int(mfg[8:10])
                mfg=datetime.date(year,month,date)
                exp = request.form['expdate' + r]
                year=int(exp[0:4])
                month=int(exp[5:7])
                date=int(exp[8:10])
                exp=datetime.date(year,month,date)
                query = 'update Pharmacy set Name="%s",Quantity=%s,Batchno=%s,ManufactureDate="%s",ExpiryDate="%s" where Sno=%s'
                db.execute(query%(name,quantity,batchno,mfg,exp,sno))
                db.execute("COMMIT")
                flash('Record '+sno+' updated')
                return redirect(url_for('inventory'))		
            elif request.form['btn'] == 'delete' + r:
                sno=request.form['Sno' + r]
                query='delete from pharmacy where Sno='+str(sno)
                db.execute(query)
                db.execute("COMMIT")
>>>>>>> 8a81dc1a9a630eb94b07915f11a077ec56151f19
                flash('Record '+sno+' deleted')
                return redirect(url_for('inventory'))
    flash('Nothing occured'+request.form['btn'])
    return redirect(url_for('inventory'))

@app.route('/prescription')
def prescription():
    db = get_cursor()
<<<<<<< HEAD
    cur = db.execute('select * from Prescription order by RegNo asc')
    entries = cur.fetchall()
=======
    db.execute('select * from Prescription order by RegNo asc')
    entries = db.fetchall()
>>>>>>> 8a81dc1a9a630eb94b07915f11a077ec56151f19
    return render_template('prescription.html',entries = entries)

@app.route('/fileprescription', methods=['GET','POST'])
def fileprescription():
    db = get_cursor()
    docno = request.form['DoctorNo']
    regno = request.form['RegNo']
    cause = request.form['Cause']
    meds = request.form['Medicine']
    qty = request.form['Quantity']
    remark = request.form['Remarks']
    db.execute('insert into Prescription values(%s,"%s","%s","%s",%s,"%s")'%(docno,regno,cause,meds,qty,remark))
    db.execute("COMMIT")
    flash('Prescription for '+regno+' has been given')
    return redirect(url_for('prescription'))

@app.route('/employee',methods=['GET','POST'])
def employee():
    db = get_cursor()
    error=None
    chars=[chr(i) for i in xrange(ord('A'), ord('N')+1)]
    query = 'select EmpID from Login where UserName=%s'
    cur = db.execute(query,[app.config['USERNAME']])
    data = cur.fetchone()
    entries =None
    if data is None:
        error = 'User details not entered properly in the database'
    else:
        cur = db.execute('select * from Users join Employee where Users.Regno=Employee.Regno and Users.Regno=%s',[data[0]])
        entries = cur.fetchall()
    return render_template('employee_profile.html',entries = entries,chars=chars)

@app.route('/employeeinfo',methods=['GET','POST'])
def employeeinfo():
    return redirect(url_for('employee'))

@app.route('/student',methods=['GET','POST'])
def student():
    db = get_cursor()
    error=None
    chars=[chr(i) for i in xrange(ord('A'), ord('N')+1)]
    query = 'select EmpID from Login where UserName="%s"'
    db.execute(query%(app.config['USERNAME']))
    data = db.fetchone()
    entries =None
    if data is None:
        error = 'User details not entered properly in the database'
    else:
        db.execute('select * from Users join Student where Users.Regno=Student.Regno and Users.Regno=%s',[data[0]])
        entries = db.fetchall()
        flash(app.config['USERNAME'])
    return render_template('student_profile.html',entries = entries,chars=chars)

@app.route('/studentinfo',methods=['GET','POST'])
def studentinfo():
    return redirect(url_for('student'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))#show_entries.html

if __name__ == '__main__':
    app.debug = True
    app.secret_key=os.urandom(24)
<<<<<<< HEAD
    app.run()
=======
    app.run()
>>>>>>> 8a81dc1a9a630eb94b07915f11a077ec56151f19
