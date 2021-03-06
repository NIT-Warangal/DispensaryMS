# all the imports
import os,binascii
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from flaskext.mysql import MySQL
from flask_mail import Mail,Message
from config import config, ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD
from werkzeug.utils import secure_filename
from flask import send_from_directory
from pdf import convertHtmlToPdf,create_pdf
import datetime
 
import logging
from logging.handlers import SMTPHandler
credentials = None

mysql = MySQL()
# create our little application :)

app = Flask(__name__)

# Managing Bills Position
UPLOAD_FOLDER = 'bills/'
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'tiff', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

for key in config:
    app.config[key] = config[key]

mail = Mail(app)
# Mail
mail.init_app(app)

if MAIL_USERNAME or MAIL_PASSWORD:
    credentials = (MAIL_USERNAME, MAIL_PASSWORD)
    mail_handler = SMTPHandler((MAIL_SERVER, MAIL_PORT), 'no-reply@' + MAIL_SERVER, ADMINS, 'resetpass', credentials)
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

mysql.init_app(app)
app.config.from_object(__name__)

def tup2float(tup):
    return float('.'.join(str(x) for x in tup))

def get_cursor():
    return mysql.connect().cursor()

@app.teardown_appcontext
def close_db():
    """Closes the database again at the end of the request."""
    get_cursor().close()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/changepassword', methods=['GET','POST'])
def changepassword():
    if request.method=="POST":
        db=get_cursor()
        myid = app.config['USERID']
        oldpass=request.form['oldpass']
        newpass=request.form['newpass']
        renewpass=request.form['renewpass']
        if newpass == renewpass:
            # Both entered passwords matched
            tempsql = 'insert into CheckPassword values ("%s",MD5("%s"))'
            db.execute(tempsql%(myid,oldpass))
            db.execute("COMMIT")
            sql = 'select * from Login where Password=(select Password from CheckPassword where RegNo="%s") and EmpID="%s"'
            db.execute(sql%(myid,myid))
            oldvalue = db.fetchall()
            if not oldvalue:
                flash('Your original password doesnot match')
                delsql = 'delete from CheckPassword where RegNo="%s"'
                db.execute(delsql%myid)
                db.execute("commit")
                return redirect(url_for('changepassword'))
            updatesql = 'update Login set Password=MD5("%s") where EmpID="%s"'
            db.execute(updatesql%(newpass,myid))
            db.execute("commit")
            delsql = 'delete from CheckPassword where RegNo="%s"'
            db.execute(delsql%myid)
            db.execute("commit")
            flash("Your password has been successfully changed")
            return redirect(url_for('changepassword'))
        flash('Your New Passwords donot match')
        return redirect(url_for('changepassword'))
    return render_template('changepassword.html')


@app.route('/forgetpassword',methods=['GET','POST'])
def forgetpassword():
    if request.method=="POST":
        db=get_cursor()
        regno = request.form['regno']
        email = request.form['email']
        sql = 'select * from Login where EmpID = (select RegNo from Users where email ="%s" and RegNo="%s")'
        db.execute(sql%(email,regno))
        values = db.fetchall()
        if not values:
            flash('Registration No. and Employee ID dont match')
            return redirect(url_for('forgetpassword'))
        tempval = ""
        for val in values:
            tempval = val[1]
        db.execute("commit")
        new_password=binascii.b2a_hex(os.urandom(15))
        now = datetime.datetime.now()
        resetsql = 'insert into ResetPassword values ("%s","%s",MD5("%s"),"%s")'
        db.execute(resetsql%(regno,now.strftime("%d/%m/%y %H:%M"),new_password,new_password))
        db.execute("commit")
        updatesql = 'update Login set Password=MD5("%s") where EmpID="%s"'
        db.execute(updatesql%(new_password,regno))
        db.execute("commit")
        msg = Message("Dispensary Password Reset",sender="noreply-password@dispensary.nitw.ac.in",recipients=[email])
        msg.body = "Hello, "+tempval+"\nYou have requested for a new password at "+now.strftime("%d/%m/%y %H:%M")+"\nYour New Password is "+new_password+"\n\nThank You!\nAdmin"
        mail.send(msg)
        print "message sent"
        # flash('Your New Password is '+new_password)
        # We need to send this via email not flash it
        return render_template('forgetpassword.html',values=values)
    return render_template('forgetpassword.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/bills', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        db = get_cursor()
        file = request.files['file']
        now = datetime.datetime.now()
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            sql ='insert into Bills values ("%s","%s","%s")'
            db.execute(sql%(filename,now,now.strftime("%H:%M")))
            db.execute("COMMIT")
            flash(filename+' successfully uploaded at '+now.strftime("%H:%M"))
            return redirect(url_for('uploaded_file',filename=filename))
        else:
            flash('This type of file is invalid. Use \'pdf\', \'png\', \'tiff\', \'jpg\', \'jpeg\', \'gif\'')
    return render_template('fileupload.html')

@app.route('/')
def screen():
    db = get_cursor()
    sql = 'select * from Users where RegNo = "%s"'
    db.execute(sql%app.config['USERID'])
    names = db.fetchall()
    newssql = 'select * from DoctorNews order by Date DESC'
    db.execute(newssql)
    news = db.fetchone()
    db.execute("commit")
    return render_template('screen.html',names=names, news=news) #show_entries

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/showfiles')
def showfiles():
    db=get_cursor()
    sql = 'select * from Bills order by Time desc'
    db.execute(sql)
    bills = db.fetchall()
    if not bills:
        flash('There are no bills uploaded yet')
        return redirect(url_for('screen'))
    return render_template('showfiles.html',bills = bills)

@app.route('/checkletter', methods=['GET', 'POST'])
def checkletter():
    regno = app.config['USERID']
    if regno:
        db = get_cursor()
        sql = 'select * from Letters where RegNo="%s" order by Date desc'
        db.execute(sql%regno)
        letters = db.fetchall()
        enddate = []
        for item in letters:
            enddate.append(item[1]+datetime.timedelta(days=item[2]))
        db.execute("commit")
        if not letters:
            flash('You havenot been given any letters yet')
            return redirect(url_for('screen'))
        return render_template('checkletter.html',letters = letters,enddate=enddate)
    else:
        flash('You have to be logged in')
        return render_template('checkletter.html')


@app.route('/printletter',methods=['GET','POST'])
def printletter():
    if request.method=="POST":
        db=get_cursor()
        regno=request.form['regno']
        sql = 'select * from Users,Student where Users.RegNo="%s" and Users.RegNo = Student.RegNo'%(regno)
        db.execute(sql)
        entries = db.fetchall()
        if not entries:
            flash('No one with that data found.')
            return redirect(url_for('screen'))
        today=datetime.date.today()
        now = datetime.datetime.now()
        days_extend = int(request.form['days']) # No. of days to put leave for
        newdate = today+datetime.timedelta(days=days_extend)
        sql = 'insert into Letters values ("%s","%s","%s")'
        db.execute(sql%(regno,now,days_extend))
        db.execute("commit")
        # pdf = create_pdf(str(render_template('Letter.html')))
        return render_template('Letter.html',entries = entries, today=today, days=days_extend, newdate = newdate)
    else:
        flash('Error occured with the form')
        return redirect(url_for('screen'))

@app.route('/postNews',methods=['GET','POST'])
def postNews():
    if request.method=="POST":
        db=get_cursor()
        date = datetime.datetime.now()
        content = request.form['content']
        sql = 'insert into DoctorNews values ("%s","%s")'
        db.execute(sql%(date,content))
        db.execute("commit")
        flash('Posted the news.')
        return redirect(url_for('screen'))
    return redirect(url_for('screen'))


@app.route('/register')
def register():
    return render_template('show_entries.html')

@app.route('/add', methods=['POST']) #add
def add():
    db = get_cursor()
    # sno=request.form['Sno']
    regno= request.form['Regno']
    if not regno.isdigit():
        flash('The registration number can only be numeric.')
        return redirect(url_for('register'))
    uname=request.form['uname']
    sql='select * from Users join Login where Users.RegNo=Login.EmpID and (Users.RegNo="%s" or UserName="%s")'%(regno,uname)
    db.execute(sql)
    data=db.fetchall()
    if not data:
        fname=request.form['FirstName']
        mname=request.form['MiddleName']
        lname=request.form['LastName']
        bgroup=request.form['BloodGroup']
        dob =datetime.datetime.strptime(request.form['dateofbirth'],"%d/%m/%Y")
        age=int(years_between(dob))
        typ=request.form['Type']
        phn=request.form['phno']
        address=request.form['address']
        email=request.form['emailid']
        gender=request.form['sex']
        password=request.form['pwd']
        con_password=request.form['con_password']
        if con_password!=password:
            flash('Confirm password doesnot match with password')
            return redirect(url_for('register'))
        sql='insert into Users \
        (RegNo, FirstName, MiddleName,LastName, BloodGroup, DateofBirth, Age, Type, Phonenumber, Address,\
         email,gender) values (%s,"%s","%s","%s","%s","%s",%s,%s,"%s","%s","%s","%s")'
        db.execute(sql%(regno,fname,mname,lname,bgroup,dob,age,typ,phn,address,email,gender))
        db.execute("COMMIT")
        db.execute("insert into Login values('%s','%s',MD5('%s'),%s)"%(regno,uname,password,typ))
        db.execute("COMMIT")
        flash('New user '+ regno + ' registered')
        return redirect(url_for('screen'))#show_entriesreturn render_template(url_for('show_entries.html'))
    flash('There exists a user already with that regno/username')
    return redirect(url_for('register'))

@app.route('/student_details')
def student_details():
    db=get_cursor()
    chars=[chr(i) for i in xrange(ord('A'), ord('N')+1)]
    sql='select Count(*) from Student where RegNo="%s"'%(app.config['USERID'])
    db.execute(sql)
    data = db.fetchone()[0]
    if not data:
        return render_template('student_details.html',chars=chars)
    flash('You have already filled in this data!')
    return redirect(url_for('screen'))

@app.route('/student_register',methods=['GET','POST'])
def student_register():
    db=get_cursor()
    if request.method=="POST":
        regno=app.config['USERID']
        year_join=int(request.form['year'])
        degree=request.form['course']
        branch=request.form['branch']
        section=request.form['section']
        rno=request.form['roll_number']
        if not rno.isdigit():
            flash('This roll number is not allowed.')
            return redirect(url_for('screen'))
        emergency_phn=request.form['emergency_contact']
        if not emergency_phn.isdigit():
            flash('Enter a valid phone number')
            return redirect(url_for('screen'))
        hostel=request.form['hostel']
        hostelroomno=request.form['room_number']
        db.execute('insert into Student (`Year`, `Section`, `Branch`, `Degree`, `RegNo`, `RollNo`, `Emergencyphone`, `Hostel`, `HostelRoomNo`) values(%s,"%s","%s","%s","%s","%s","%s","%s","%s")'%(year_join,section,branch,degree,regno,rno,emergency_phn,hostel,hostelroomno))
        db.execute("COMMIT")
        # flash(regno+str(year_join)+degree+' '+branch+section+rno+emergency_phn+hostel+' '+hostelroomno)
        flash('Record for '+regno+' has been successfully inserted') 
    return redirect(url_for('student'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

store=0
@app.route('/login', methods=['GET', 'POST'])
def login():
    global store
    error = None
    db=get_cursor()
    session['temp']=0
    if request.method == 'POST':
        uname=str(request.form['username'])
        pwd=str(request.form['password'])
        sql='select Count(*) from Login where UserName="%s" and Password=MD5("%s")'%(uname,pwd)
        db.execute(sql)
        data = db.fetchone()[0]
        if not data:
            error='Invalid username/password'
        else:
            session['logged_in'] = True
            sql='select Occupation from Login where UserName="%s" and Password=MD5("%s")'%(uname,pwd)
            db.execute(sql)
            result=db.fetchone()[0]
            session['temp']=result
            sql='select EmpID from Login where UserName="%s" and Password=MD5("%s")'%(uname,pwd)
            db.execute(sql)
            uid=db.fetchone()[0]
            db.execute("COMMIT")
            app.config['USERNAME'] = uname
            app.config['USERID'] = uid
            flash('You were logged in ')
            return redirect(url_for('screen'))
    return render_template('login.html', error=error) #login.html

t=0
@app.route('/inventory')
def inventory():
    global store
    db=get_cursor()
    db.execute('select * from Pharmacy order by Sno')
    entries = db.fetchall()
    db.execute('commit')
    return render_template('pharmventory.html',entries = entries)

@app.route('/insert',methods=['GET','POST'])
def insert():
    global t
    db=get_cursor()
    db.execute('select Count(1) from Pharmacy')
    t=db.fetchone()[0]
    if request.form['btn'] == 'Insert':
        sno = (request.form['Sno'])
        name = (request.form['Name'])
        quantity = (request.form['qty'])
        batchno = request.form['bno']
        mfg =datetime.datetime.strptime(request.form['mfgdate'],"%d/%m/%Y")
        exp =datetime.datetime.strptime(request.form['expdate'],"%d/%m/%Y")
        sql = 'insert into Pharmacy values(%s,"%s",%s,%s,"%s","%s")'
        db.execute(sql%(sno,name,quantity,batchno,mfg,exp))
        db.execute("COMMIT")
        flash('New entry successfully inserted')
        return redirect(url_for('inventory'))
    else:
        flash('Record not inserted')
    return redirect(url_for('inventory'))

@app.route('/updel',methods=['GET','POST'])
def updel():
    global t
    db=get_cursor()
    db.execute('select Count(1) from Pharmacy')
    t=db.fetchone()[0]
    for i in range( 1, t+1):
            r = str(i)
            if request.form['btn1'] == 'update'+r:
                sno=request.form['Sno' + r]
                name=request.form['Name' + r]
                quantity=request.form['qty' + r]
                batchno=request.form['bno' + r]
                mfg =datetime.datetime.strptime(request.form['mfgdate' + r],"%d/%m/%Y")
                exp =datetime.datetime.strptime(request.form['expdate' + r],"%d/%m/%Y")
                query = 'update Pharmacy set Name="%s",Quantity=%s,Batchno=%s,ManufactureDate="%s",ExpiryDate="%s" where Sno=%s'
                db.execute(query%(name,quantity,batchno,mfg,exp,sno))
                db.execute("COMMIT")
                flash('Record '+sno+' updated')
                return redirect(url_for('inventory'))       
            elif request.form['btn1'] == 'delete'+r:
                sno=request.form['Sno' + r]
                query='delete from Pharmacy where Sno='+str(sno)
                db.execute(query)
                db.execute("COMMIT")
                flash('Record '+sno+' deleted')
                return redirect(url_for('inventory'))
            i=i+1
    flash('Nothing occured')
    return redirect(url_for('inventory'))

@app.route('/prescription')
def prescription():
    db = get_cursor()
    db.execute('select * from Prescription order by RegNo asc')
    entries = db.fetchall()
    db.execute('select * from Pharmacy order by Sno asc')
    pharmacy=db.fetchall()
    return render_template('prescription.html',entries = entries,pharmacy=pharmacy)

@app.route('/fileprescription', methods=['GET','POST'])
def fileprescription():
    db = get_cursor()
    regno=request.form['RegNo']
    sql='select Count(*) from Users where Regno="%s"'%(regno)
    db.execute(sql)
    data=db.fetchone()[0]
    if data>0:
        inde=request.form['numofrows']
        for i in range(0,int(inde)):
            medicine=request.form['selectMedicine'+str(i)]
            quantity=int(request.form['Quantity'+str(i)])
            sql='insert into PrescriptionIndex(`medicine`,`quantity`) values("%s",%s)'%(medicine,quantity)
            db.execute(sql)
            db.execute("commit")
            sql='select quantity from Pharmacy where Name="%s"'%(medicine)
            db.execute(sql)
            get_quantity=db.fetchone()[0]
            if (get_quantity-quantity)>0:
                continue
            else:
                flash('Medicine named '+medicine+' has been given a quantity greater than what the inventory consists')
                return redirect(url_for('prescription'))
        sql='select max(Sno) from PrescriptionIndex'
        db.execute(sql)
        indexEnd=db.fetchone()[0]
        db.execute("commit")
        indexStart=indexEnd-int(inde)+1
        doctorno=app.config['USERID']
        cause=request.form['Cause']
        remarks=request.form['Remarks']
        date_of_prescription=datetime.date.today()
        sql='insert into Prescription values(%s,"%s","%s",%s,%s,"%s","%s","%s")'%(doctorno,regno,cause,indexStart,indexEnd,remarks,date_of_prescription,1)
        db.execute(sql)
        db.execute("commit")
        flash('Prescription for '+regno+' is given')
        return redirect(url_for('screen'))
    flash('User doesnot exist')
    return redirect(url_for('prescription'))

@app.route('/checkprescription',methods=['GET','POST'])
def checkprescription():
    db=get_cursor()
    sql="select * from Prescription where RegNo='%s' order by Date"%(app.config['USERID'])
    db.execute(sql)
    entries = db.fetchall()
    db.execute("commit")
    medicine=[]
    for entry in entries:
        sql='select * from PrescriptionIndex where Sno>=%s and Sno<=%s'%(entry[3],entry[4])
        db.execute(sql)
        medicine.append(db.fetchall())
        db.execute("COMMIT")
    data=medicine
    return render_template('checkprescription.html',entries=entries,medicine=data)

@app.route('/report',methods=['GET','POST'])
def report():
    if request.method=="POST":
        db=get_cursor()
        reportdate=datetime.datetime.strptime(request.form['reportdate'],"%d/%m/%Y")
        datevalue = datetime.datetime.today()
        sql="select * from Prescription where Date='%s'"
        db.execute(sql%reportdate)
        entries=db.fetchall()
        db.execute("COMMIT")
        if not entries and reportdate >= datevalue:
            flash('No reports on that date, you cannot look for a future date')
            return redirect(url_for('screen'))
        medicine=[]
        for entry in entries:
            sql='select * from PrescriptionIndex where Sno>=%s and Sno<=%s'%(entry[3],entry[4])
            db.execute(sql)
            medicine.append(db.fetchall())
            db.execute("COMMIT")
        data=medicine
        return render_template('report.html',entries=entries,medicine=data)
    return redirect(url_for('screen'))

@app.route('/checkpendingprescription')
def checkpendingprescription():
    db=get_cursor()
    datevalue = datetime.datetime.today()
    sql='select * from Prescription where Pending=1 and Date="%s"'
    depsql = 'select * from DependencyPrescription where Pending=1 and Date="%s"'
    db.execute(sql%(datevalue.strftime("%Y-%m-%d")))
    entries=db.fetchall()
    db.execute("commit")
    db.execute(depsql%(datevalue.strftime("%Y-%m-%d")))
    depentries = db.fetchall()
    db.execute("commit")
    medicine=[]
    dmedicine=[]
    for entry in entries:
        sql='select * from PrescriptionIndex where Sno>=%s and Sno<=%s'%(entry[3],entry[4])
        db.execute(sql)
        medicine.append(db.fetchall())
        db.execute("COMMIT")
    for value in depentries:
        sql ='select * from PrescriptionIndex where Sno>=%s and Sno<=%s'%(value[4],value[5])
        db.execute(sql)
        dmedicine.append(db.fetchall())
        db.execute("COMMIT")
    data = medicine
    depdata = dmedicine
    return render_template('checkpendingprescription.html',entries=entries, depentries=depentries, data=data,depdata=depdata)

@app.route('/updateinventory',methods=['GET','POST'])
def updateinventory():
    global t
    db=get_cursor()
    db.execute('select count(1) from Prescription where Pending=1')
    t = db.fetchone()[0]
    start = 0
    end = 0
    db.execute('select count(1) from DependencyPrescription where Pending=1')
    e = db.fetchone()[0]
    nval = t+e
    t = nval
    for i in range(0,t+1):
        r = str(i)
        if request.form['btn']== 'btndirect'+r:
            regno=request.form['Regno'+r]
            datevalue = datetime.datetime.today()
            datevalue = datevalue.strftime("%Y-%m-%d")
            sql='select * from Prescription where Regno="%s" and Date="%s" and Pending=1'%(regno,datevalue)
            db.execute(sql)
            values=db.fetchone()
            n=0
            for item in values:
                n=n+1
            if n>0:
                start=int(values[3])
                end=int(values[4])
                for x in range(start,end+1):
                    sql='select * from PrescriptionIndex where Sno="%s"'%(x)
                    db.execute(sql)
                    result=db.fetchall()
                    medicine=''
                    quantity=0
                    for item in result:
                        medicine=item[1]
                        quantity=item[2]
                    updatesql='update Pharmacy set Quantity = Quantity-%s where Name="%s"'%(quantity,medicine)
                    db.execute(updatesql)
                    db.execute("commit")
                    x=x+1
                query = 'update Prescription set Pending=0 where RegNo="%s" and Date="%s"'%(regno,datevalue)
                db.execute(query)
                db.execute('commit')
            flash('Pending status removed. Inventory Updated. '+str(datevalue))
            return redirect(url_for('checkpendingprescription'))
        elif request.form['btn']=='btndep'+r:
            regno=request.form['Regno'+r]
            datevalue = datetime.datetime.today()
            datevalue = datevalue.strftime("%Y-%m-%d")
            sql='select * from DependencyPrescription where Regno="%s" and Date="%s"'%(regno,datevalue)
            db.execute(sql)
            values=db.fetchone()
            if values:
                flash('depend true')
            if values:
                start=int(values[4])
                end=int(values[5])
                for x in range(start,end+1):
                    sql='select * from PrescriptionIndex where Sno="%s"'%(x)
                    db.execute(sql)
                    result=db.fetchall()
                    medicine=''
                    quantity=0
                    for item in result:
                        medicine=item[1]
                        quantity=item[2]
                    updatesql='update Pharmacy set Quantity = Quantity-%s where Name="%s"'%(quantity,medicine)
                    db.execute(updatesql)
                    db.execute("commit")
                    x=x+1
                query='update DependencyPrescription set Pending=0 where RegNo="%s" and Date="%s"'%(regno,datevalue)
                db.execute(query)
                db.execute("commit")
            flash('Pending status removed. Inventory Updated.')
            return redirect(url_for('checkpendingprescription'))
        i=i+1
    flash('An Unknown Error Occured')
    return render_template('checkpendingprescription.html')

@app.route('/checkpatienthistory',methods=['GET','POST'])
def checkpatienthistory():
    if request.method=="POST":
        db=get_cursor()
        regno=request.form['regno']
        sql="select * from Prescription where RegNo='%s' order by Date"%(regno)
        db.execute(sql)
        entries=db.fetchall()
        db.execute("COMMIT")
        if not entries:
            flash('No one with that data found.')
            return redirect(url_for('screen'))
        medicine=[]
        for entry in entries:
            sql='select * from PrescriptionIndex where Sno>=%s and Sno<=%s'%(entry[3],entry[4])
            db.execute(sql)
            medicine.append(db.fetchall())
            db.execute("COMMIT")
        data=medicine
        flash('Viewing patient prescription history')
        return render_template('patienthistory.html',entries=entries,data=data)
    return redirect(url_for('screen'))

@app.route('/checkdependencypatienthistory',methods=['GET','POST'])
def checkdependencypatienthistory():
    if request.method=="POST":
        db=get_cursor()
        empid=request.form['regno']
        sql='select * from Dependencies where Regno="%s"'%(empid)
        db.execute(sql)
        entries=db.fetchall()
        db.execute("commit")
        if not entries:
            flash('No dependencies for this employee')
            return redirect(url_for('screen'))
        return render_template('choosedependencyhistory.html',entries=entries)
    flash('No dependencies found')
    return redirect(url_for('screen'))

@app.route('/selectdependencyhistory',methods=['POST'])
def selectdependencyhistory():
    db=get_cursor()
    empid=request.form['empid']
    dependencyname=''
    num_of_dependencies=request.form['numofrows']
    for i in range(0,int(num_of_dependencies)):
        if request.form['btn']=='select'+str(i):
            dependencyname=request.form['dependencyname'+str(i)]
    pharmacy = []
    db.execute('select DoctorNo,Regno,DependencyName,Cause,IndexStart,IndexEnd,Remarks from DependencyPrescription where RegNo="%s"'%empid)
    entries = db.fetchall()
    db.execute("commit")
    # flash(entries)
    # Tuple Index Error
    for entry in entries:
        db.execute('select * from PrescriptionIndex where Sno between "%s" and "%s"'%(entry[4],entry[5]))
        pharmacy.append(db.fetchall())
        db.execute("commit")
    return render_template('checkdependencyhistory.html',entries=entries,pharmacy=pharmacy)

@app.route('/employee',methods=['GET','POST'])
def employee():
    db = get_cursor()
    db.execute('select * from Users join Employee where Users.RegNo=Employee.RegNo and Users.RegNo="%s"'%(app.config['USERID']))
    entries = db.fetchall()
    return render_template('employee_profile.html',entries = entries)

@app.route('/employeeinfo',methods=['GET','POST'])
def employeeinfo():
    if request.method=="POST":
        db=get_cursor()
        lname=request.form['lname']
        fname=request.form['fname']
        mname=request.form['mname']
        regno=app.config['USERID']
        sex=request.form['gender']
        dob =datetime.datetime.strptime(request.form['dob'],"%d/%m/%Y")
        email=request.form['email']
        phno=request.form['phone_number']
        age=int(years_between(dob))
        db.execute('update Users set FirstName="%s",MiddleName="%s",LastName="%s",DateofBirth="%s",Age=%s,Phonenumber="%s",email="%s",gender="%s" where Regno=%s'%(fname,mname,lname,dob,age,phno,email,sex,regno))
        db.execute('COMMIT')
        emergency_phn=request.form['emergency_contact']
        occupation=request.form['occupation']
        location = request.form['location']
        db.execute('Update Employee set EmergencyContact="%s",Location="%s",Occupation="%s" where RegNo="%s"'%(emergency_phn,location,occupation,regno))
        db.execute("COMMIT")
        flash("Record Updated")
    return redirect(url_for('employee'))

@app.route('/employee_details',methods=['GET','POST'])
def employee_details():
    db=get_cursor()
    sql='select Count(*) from Employee where RegNo="%s"'%(app.config['USERID'])
    db.execute(sql)
    data = db.fetchone()[0]
    if not data:
        return render_template('employee_details.html')
    flash('You have already filled the data!')
    return redirect(url_for('screen'))

@app.route('/employee_register',methods=['GET','POST'])
def employee_register():
    if request.method=='POST':
        db=get_cursor()
        regno=app.config['USERID']
        occupation=request.form['occupation']
        emergency_phn=request.form['emergency_phn']
        location=request.form['location']
        number_of_dependencies=int(request.form['num_of_dependencies'])
        sql='insert into Employee values("%s","%s","%s","%s","%s")'%(regno,occupation,emergency_phn,location,number_of_dependencies)
        db.execute(sql)
        db.execute("COMMIT")
        flash("Record for "+regno+" has been added")
        return redirect(url_for('employee'))
    return render_template('show_entries.html')    

@app.route('/register_dependency',methods=['GET','POST'])
def register_dependency():
    if request.method=='POST':
        i=0
        db=get_cursor()
        number_of_dependencies=0
        for i in range(1,10):
            if request.form['btn']=='add'+str(i):
                number_of_dependencies=i
                for j in range(0,number_of_dependencies):
                    regno=app.config['USERID']
                    name=request.form['name'+str(j)]
                    dob=request.form['dob'+str(j)]
                    dob =datetime.datetime.strptime(dob,"%d/%m/%Y")
                    sex=request.form['gender'+str(j)]
                    relation=request.form['rel'+str(j)]
                    sql='insert into Dependencies values("%s","%s","%s","%s","%s")'%(regno,name,dob,sex,relation)
                    db.execute(sql)
                db.execute("commit")
                flash('Entered '+name+' as Dependency for '+regno)
                #Shouldn't the Dependency details also go into the Users table ?
    return render_template('register_dependency.html')

@app.route('/show_dependency',methods=['GET','POST'])
def show_dependency():
    db=get_cursor()
    sql='select * from Dependencies where Regno="%s"'%(app.config['USERID'])
    db.execute(sql)
    entries=db.fetchall()
    age=[]
    for entry in entries:
        age.append(int(years_between(entry[2])))
    return render_template('show_dependency.html',entries=entries,age=age)

@app.route('/update_dependency',methods=['POST'])
def update_dependency():
    db=get_cursor()
    numofrows=request.form['numofrows']
    for i in range(0,int(numofrows)):
        if request.form['btn']=='update'+str(i):
            name=request.form['name'+str(i)]
            dob=request.form['dob'+str(i)]
            dob =datetime.datetime.strptime(dob,"%d/%m/%Y")
            gender=request.form['gender'+str(i)]
            rel=request.form['rel'+str(i)]
            sql='update dependencies set name="%s",dateofbirth="%s",sex="%s",relation="%s" where RegNo="%s"'%(name,dob,gender,rel,app.config['USERID'])
            db.execute(sql)
            db.execute("commit")
            flash('Details of '+name+' has been updated')
    return redirect(url_for('show_dependency'))

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
    return render_template('student_profile.html',entries = entries,chars=chars)

def years_between(d1):
    d2=datetime.datetime.today()
    return ((d2-d1).days-(d2-d1).seconds/86400.0)/365.2425

@app.route('/studentinfo',methods=['GET','POST'])
def studentinfo():
    db=get_cursor()
    if request.method=="POST":
        lname=request.form['lname']
        fname=request.form['fname']
        mname=request.form['mname']
        regno=request.form['registration_number']
        sex=request.form['gender']
        dob =datetime.datetime.strptime(request.form['dob'],"%d/%m/%Y")
        email=request.form['email']
        phno=request.form['phone_number']
        age=int(years_between(dob))
        db.execute('update Users set FirstName="%s",MiddleName="%s",LastName="%s",DateofBirth="%s",Age=%s,Phonenumber="%s",email="%s",gender="%s" where Regno=%s'%(fname,mname,lname,dob,age,phno,email,sex,regno))
        db.execute("COMMIT")
        year_join=int(request.form['year'])
        degree=request.form['course']
        branch=request.form['branch']
        section=request.form['section']
        rno=request.form['roll_number']
        hostel=request.form['hostel']
        hostelroomno=request.form['room_number']
        db.execute('update Student set Year=%s,Section="%s",Branch="%s",Degree="%s",RollNo="%s",Hostel="%s",HostelRoomNo="%s" where RegNo="%s"'%(year_join,section,branch,degree,rno,hostel,hostelroomno,regno))
        db.execute("COMMIT")
        flash('Record '+regno+' updated') 
    return redirect(url_for('student'))

@app.route('/choosereferingid',methods=['POST'])
def choosereferingid():
    db=get_cursor()
    empid=request.form['regno']
    sql='select * from Dependencies where Regno="%s"'%(empid)
    db.execute(sql)
    entries=db.fetchall()
    db.execute("commit")
    if not entries:
        flash('No dependencies for this employee')
        return redirect(url_for('screen'))
    return render_template('choosedependency.html',entries=entries)

@app.route('/selectdependency',methods=['POST'])
def selectdependency():
    db=get_cursor()
    empid=request.form['empid']
    dependencyname=''
    num_of_dependencies=request.form['numofrows']
    for i in range(0,int(num_of_dependencies)):
        if request.form['btn']=='select'+str(i):
            dependencyname=request.form['dependencyname'+str(i)]
    db.execute('select * from Prescription order by RegNo asc')
    entries = db.fetchall()
    db.execute('select * from Pharmacy order by Sno asc')
    pharmacy=db.fetchall()    
    return render_template('dependencyprescription.html',empid=empid,dependencyname=dependencyname,entries=entries,pharmacy=pharmacy)

@app.route('/dependencyprescription',methods=['POST'])
def dependencyprescription():
    db=get_cursor()
    regno=request.form['empid']    
    inde=request.form['numofrows']
    for i in range(0,int(inde)):
        medicine=request.form['selectMedicine'+str(i)]
        quantity=int(request.form['Quantity'+str(i)])
        sql='insert into PrescriptionIndex(`medicine`,`quantity`) values("%s",%s)'%(medicine,quantity)
        db.execute(sql)
        db.execute("commit")
        sql='select quantity from Pharmacy where Name="%s"'%(medicine)
        db.execute(sql)
        get_quantity=db.fetchone()[0]
        if (get_quantity-quantity)>0:
            continue
        else:
            flash('Medicine named '+medicine+' has been given a quantity greater than what the inventory consists')
            return redirect(url_for('prescription'))
    sql='select max(Sno) from PrescriptionIndex'
    db.execute(sql)
    indexEnd=db.fetchone()[0]
    db.execute("commit")
    indexStart=indexEnd-int(inde)+1
    doctorno=app.config['USERID']
    dependencyname=request.form['dependencyname']
    cause=request.form['Cause']
    remarks=request.form['Remarks']
    date_of_prescription=datetime.date.today()
    sql='insert into DependencyPrescription values(%s,"%s","%s","%s",%s,%s,"%s","%s",%s)'%(doctorno,regno,dependencyname,cause,indexStart,indexEnd,remarks,date_of_prescription,1)
    db.execute(sql)
    db.execute("commit")
    flash('Prescription for '+regno+' is given')
    return redirect(url_for('screen'))

@app.route('/showdependencyprescription')
def showdependencyprescription():
    db=get_cursor()
    sql="select * from DependencyPrescription where RegNo='%s' order by Date"%(app.config['USERID'])
    db.execute(sql)
    entries = db.fetchall()
    db.execute("commit")
    medicine=[]
    for entry in entries:
        sql='select * from PrescriptionIndex where Sno>=%s and Sno<=%s'%(entry[4],entry[5])
        db.execute(sql)
        medicine.append(db.fetchall())
        db.execute("COMMIT")
    data=medicine
    return render_template('checkdependencyprescription.html',entries=entries,medicine=data)

@app.route('/logout')
def logout():
    if session['logged_in'] != None:
        if session['logged_in']==True:
            session.pop('logged_in', None)
            session.pop('temp',0)
            flash('You were logged out')
        else:
            flash('Welcome Back!')
    return redirect(url_for('screen'))#show_entries.html

if __name__ == '__main__':
    app.debug = True
    app.secret_key=os.urandom(24)
    # app.permanent_session_lifetime = datetime.timedelta(seconds=200)
    app.run()
