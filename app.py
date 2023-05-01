from flask import Flask,render_template,request,flash,session,g,url_for,redirect
from flask_mysqldb import MySQL
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import Form, StringField, TextAreaField, PasswordField, validators,DateTimeField,DateField,IntegerField

app = Flask(__name__,template_folder='templates')

app.config['SECRET_KEY'] = 'secret-key-goes-here'

# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'Silentkiller@7'
# app.config['MYSQL_DB'] = 'bbms'
#
# mysql = MySQL(app)

# def connect_db():
#     return pymysql.connect(
#         host='localhost',
#         user='root',
#         password = "Silentkiller@7",
#         db='bbms',
#         )
def connect_db():
    return pymysql.connect(
        host='bbms.mysql.pythonanywhere-services.com',
        user='bbms',
        password = "bloodlink@123",
        db='BBMS',
        )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/signup',methods = ['POST', 'GET'])
def signUp():
    if request.method == 'POST':
        name        = request.form['name']
        phoneNumber = request.form['phoneNumber']
        email       = request.form['email']
        bloodType   = request.form['bloodType']
        dateOfBirth = request.form['dateOfBirth']
        gender      = request.form['gender']
        userType    = request.form['userType']
        password1   = request.form['password1']
        password2   = request.form['password2']

        passwd = generate_password_hash(password1, method='sha256')

        #cursor = mysql.connection.cursor()
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM BloodLinkUsers WHERE email = %s', (email))
        account = cursor.fetchone()

        if account:
            flash('Account already exists!', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        else:
            cursor.execute('''INSERT INTO BloodLinkUsers (Email,Password,UserType)
                                        VALUES(%s,%s,%s) '''
                           , (email,passwd,userType))
            conn.commit()

            cursor.execute('SELECT * FROM BloodLinkUsers WHERE email = %s', (email))
            account = cursor.fetchone()

            if userType == 'Donor':
                cursor.execute('''INSERT INTO DONOR (DonorId,Name,Contact,Email,BloodType,DOB,Gender,Address)
                                VALUES(%s,%s,%s,%s,%s,%s,%s,%s) '''
                               ,(account[0],name,phoneNumber,email,bloodType,dateOfBirth,gender,''))
            elif userType == 'Recipient':
                cursor.execute('''INSERT INTO RECIPIENT (RecipientId,Name,Contact,Email,RequiredBloodType,DOB,Gender,Address)
                                            VALUES(%s,%s,%s,%s,%s,%s,%s,%s) '''
                               , (account[0],name, phoneNumber, email,bloodType,dateOfBirth, gender, ''))
            conn.commit()
            conn.close()
            cursor.close()
            flash('User created successfully!', category='success')
    return render_template('signup.html')

@app.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        # Create variables for easy access
        email = request.form['email']
        password = request.form['password']

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM BloodLinkUsers WHERE email = %s', (email))
        account = cursor.fetchone()

        checkPass = check_password_hash(account[2],password)

        print(account)
        print(checkPass)
        if account and checkPass:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account[0]
            session['email'] = account[1]
            session['userType'] = account[3]
            flash('Logged in successfully!',category='success')
            if account[3] == 'Employee':
                return  render_template('adminBase.html')
            return  render_template('index.html')
        else:
            flash('Incorrect username/password!',category='error')
    return render_template('login.html')

@app.route('/logout',methods=['GET', 'POST'])
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('userType',None)
    flash('Logged out successfully!',category='success')
    return render_template('index.html')

@app.route('/contactUs',methods=['GET', 'POST'])
def contactUs():
    return render_template('contactUs.html')


@app.route('/adminBase',methods=['GET', 'POST'])
def adminBase():
    return render_template('adminBase.html')
@app.route('/donorBase',methods=['GET', 'POST'])
def donorBase():
    return render_template('donorBase.html')
@app.route('/recipientBase',methods=['GET', 'POST'])
def recipientBase():
    return render_template('recipientBase.html')

@app.route('/adminDonor',methods=['GET', 'POST'])
def adminDonor():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Donor')
    donorData = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('adminDonor.html',donorData=donorData)
@app.route('/adminRecipient',methods=['GET', 'POST'])
def adminRecipient():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Recipient')
    recipientData = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('adminRecipient.html',recipientData=recipientData)

class donorForm(Form):
    name    = StringField('Name', [validators.Length(min=1, max=200)])
    contact = StringField('Contact', [validators.Length(max=20)])
    email   = StringField('Email', [validators.Length(max=200)])
    bloodType = TextAreaField('Blood Type', [validators.Length(max=200)])
    dob = DateField('Date Of Birth')
    gender = StringField('Gender', [validators.Length(max=30)])


@app.route('/editDonor/<string:donorId>',methods=['GET', 'POST'])
def editDonor(donorId):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Donor where donorId = %s',[donorId])
    donorData = cursor.fetchone()

    form = donorForm(request.form)

    print(donorData)

    form.name.data = donorData[1]
    form.contact.data = donorData[2]
    form.email.data = donorData[3]
    form.bloodType.data = donorData[4]
    form.dob.data = donorData[5]
    form.gender.data = donorData[6]

    cursor.close()
    conn.close()

    if request.method == 'POST':
        name        = request.form['name']
        contact     = request.form['contact']
        email       = request.form['email']
        bloodType   = request.form['bloodType']
        dateOfBirth = request.form['dob']
        gender      = request.form['gender']

        # Create Cursor
        conn = connect_db()
        cur = conn.cursor()

        cur.execute("UPDATE DONOR SET NAME=%s,CONTACT=%s,EMAIL=%s,BLOODTYPE=%s,DOB=%s,GENDER=%s where DONORID = %s"
                    , (name,contact,email,bloodType,dateOfBirth,gender,donorId))
        conn.commit()
        cur.close()
        conn.close()
        flash('Donor Details Updated', category='success')

        return redirect(url_for('adminDonor'))

    return render_template('editDonor.html',form=form)

@app.route('/editRecipient/<string:recipientId>',methods=['GET', 'POST'])
def editRecipient(recipientId):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Recipient where recipientId = %s',[recipientId])
    recipientData = cursor.fetchone()
    form = donorForm(request.form)

    print(recipientData)

    form.name.data = recipientData[1]
    form.contact.data = recipientData[2]
    form.email.data = recipientData[3]
    form.bloodType.data = recipientData[4]
    form.dob.data = recipientData[5]
    form.gender.data = recipientData[6]

    cursor.close()
    conn.close()

    if request.method == 'POST':
        name        = request.form['name']
        contact     = request.form['contact']
        email       = request.form['email']
        bloodType   = request.form['bloodType']
        dateOfBirth = request.form['dob']
        gender      = request.form['gender']

        # Create Cursor
        conn = connect_db()
        cur = conn.cursor()

        cur.execute("UPDATE RECIPIENT SET NAME=%s,CONTACT=%s,EMAIL=%s,RequiredBloodType=%s,DOB=%s,GENDER=%s where recipientId = %s"
                    , (name,contact,email,bloodType,dateOfBirth,gender,recipientId))
        conn.commit()
        cur.close()
        conn.close()
        flash('Recipient Details Updated', category='success')

        return redirect(url_for('adminRecipient'))

    return render_template('editRecipient.html',form=form)

@app.route('/deleteDonor/<string:donorId>', methods=['POST'])
def deleteDonor(donorId):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM bloodlinkusers WHERE userId = %s", [donorId])
    conn.commit()

    cur.execute("DELETE FROM donorAppointment WHERE donorId = %s", [donorId])
    conn.commit()

    cur.execute("DELETE FROM bloodSample WHERE donorId = %s", [donorId])
    conn.commit()
    cur.execute("DELETE FROM Donor WHERE donorId = %s", [donorId])
    conn.commit()
    cur.close()
    conn.close()
    flash('Donor Details Deleted', category='success')

    return redirect(url_for('adminDonor'))

@app.route('/deleteRecipient/<string:recipientId>', methods=['POST'])
def deleteRecipient(recipientId):
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("DELETE FROM bloodlinkusers WHERE userId = %s", [recipientId])
    conn.commit()

    cur.execute("DELETE FROM recipientAppointment WHERE donorId = %s", [recipientId])
    conn.commit()

    cur.execute("DELETE FROM requestedBloodSample WHERE donorId = %s", [recipientId])
    conn.commit()
    cur.execute("DELETE FROM Recipient WHERE recipientId = %s", [recipientId])
    conn.commit()
    cur.close()
    conn.close()
    flash('Recipient Details Deleted', category='success')

    return redirect(url_for('adminRecipient'))

@app.route('/appointment',methods=['GET', 'POST'])
def appointment():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM BloodBank')
    bloodbanks = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('appointment.html',bloodbanks=bloodbanks)

@app.route('/book_appointment', methods=['GET', 'POST'])
def book_appointment():
    if request.method == 'POST':
        # bbid = request.form['bbid']
        bbname = request.form['bbname']
        date = request.form['date']
        time = request.form['time']
        print("the data from server is: "+bbname)
        bbid, bbn = bbname.split(", ")[0][1:], bbname.split(", ")[1][:-1]
        bbn = bbn[:-1].replace("'", "")
        print(bbid)
        print(bbname)
        # Save the appointment details to the MySQL database
        userType = session['userType']
        userId = session['id']
        #userId = '2'
        #USERTYPE = 'Donor'
        conn = connect_db()
        cursor = conn.cursor()
        if(userType == 'Donor'):
            cursor.execute('INSERT INTO donorAppointment (DonorId,BloodBankId,BloodBankName, AppointmentDate, AppointmentTime) '
                           'VALUES (%s, %s, %s, %s,%s)' ,(userId,bbid, bbn, date, time))
        elif (userType == 'Recipient'):
            cursor.execute('INSERT INTO recipientAppointment (RecipientId,BloodBankId,BloodBankName, AppointmentDate, AppointmentTime) '
                           'VALUES (%s, %s, %s, %s,%s)' ,(userId,bbid, bbn, date, time))
        conn.commit()
        cursor.close()
        conn.close()
        # Redirect to a success page
        return render_template('appointment.html')
    else:
        # Fetch data from the MySQL database to populate the dropdown list
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT BloodBankId, Name FROM BloodBank;')
        bloodbank_data = cursor.fetchall()
        bloodbanks = [[row[0], row[1]] for row in bloodbank_data]
        # print(bloodbanks[0])
        # bloodbankIDs = [row[0] for row in bloodbank_data]
        # print(bloodbankIDs)
        # Render the HTML page and pass the data to the template
        search_query = request.args.get('search')
        if search_query:
            # Filter the bloodbanks list based on the search query
            bloodbanks = [row for row in bloodbank_data if search_query.lower() in row[1].lower()]
        # Render the HTML page and pass the data to the template

        cursor.close()
        conn.close()

        return render_template('appointment.html', bloodbanks=bloodbanks, search_query=search_query)
        # return render_template('appointment.html', bloodbanks=bloodbanks)

@app.route('/adminDonorAppointment',methods=['GET', 'POST'])
def adminDonorAppointment():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM DonorAppointmentView')
    donorData = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('adminDonorAppointment.html',donorData=donorData)

@app.route('/adminRecipientAppointment',methods=['GET', 'POST'])
def adminRecipientAppointment():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM RecipientAppointmentView')
    recipientData = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('adminRecipientAppointment.html',recipientData=recipientData)

class bloodSample(Form):
    bloodType = TextAreaField('Blood Type', [validators.Length(max=10)])
    HaemoglobinLevel = IntegerField('HaemoglobinLevel Level')
    rbcCount = IntegerField('RBC Count')
    wbcCount = IntegerField('WBC Count')
    Quantity = IntegerField('Quantity')

@app.route('/editDonorAppointment/<int:appointmentId>/<int:donorId>/<int:bloodBankId>',methods=['GET', 'POST'])
def editDonorAppointment(appointmentId,donorId,bloodBankId):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM BloodSample where AppointmentId=%s and donorId = %s and bloodBankId=%s',[appointmentId,donorId,bloodBankId])
    bloodSampleData = cursor.fetchone()

    form = bloodSample(request.form)

    print(bloodSampleData)
    if bloodSampleData:
        form.bloodType.data = bloodSampleData[4]
        form.HaemoglobinLevel.data = bloodSampleData[5]
        form.rbcCount.data = bloodSampleData[6]
        form.wbcCount.data = bloodSampleData[7]
        form.Quantity.data = bloodSampleData[8]
    else:
        form.bloodType.data = ''
        form.HaemoglobinLevel.data = 0
        form.rbcCount.data = 0
        form.wbcCount.data = 0
        form.Quantity.data = 0

    cursor.close()
    conn.close()

    if request.method == 'POST':
        bloodType           = request.form['bloodType']
        HaemoglobinLevel    = request.form['HaemoglobinLevel']
        rbcCount            = request.form['rbcCount']
        wbcCount            = request.form['wbcCount']
        Quantity            = request.form['Quantity']

        if not bloodSampleData:
            conn = connect_db()
            cur = conn.cursor()

            cur.execute(
                "INSERT INTO BloodSample (appointmentId, donorId, bloodBankId, bloodType, HaemoglobinLevel, rbcCount, wbcCount, Quantity) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (appointmentId,donorId,bloodBankId, bloodType, HaemoglobinLevel,rbcCount,wbcCount,Quantity))
            conn.commit()
            cur.close()
            conn.close()
            flash('Blood Sample Collected', category='success')

            return redirect(url_for('adminDonorAppointment'))
        else:
            conn = connect_db()
            cur = conn.cursor()

            cur.execute(
                "UPDATE BloodSample SET appointmentId=%s, donorId=%s, bloodBankId=%s, bloodType=%s, HaemoglobinLevel=%s, rbcCount=%s, wbcCount=%s, Quantity=%s",
                (appointmentId, donorId, bloodBankId, bloodType, HaemoglobinLevel, rbcCount, wbcCount, Quantity))
            conn.commit()
            cur.close()
            conn.close()
            flash('Blood Sample Details Updated', category='success')

            return redirect(url_for('adminDonorAppointment'))

    return render_template('editDonorAppointment.html',form=form)

class requestedBloodSample(Form):
    bloodType = TextAreaField('Blood Type', [validators.Length(max=10)])
    Quantity = IntegerField('Quantity')
@app.route('/editRecipientAppointment/<int:appointmentId>/<int:recipientId>/<int:bloodBankId>',methods=['GET', 'POST'])
def editRecipientAppointment(appointmentId,recipientId,bloodBankId):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM RequestedBloodSample where AppointmentId=%s and recipientId = %s and bloodBankId=%s',[appointmentId,recipientId,bloodBankId])
    bloodSampleData = cursor.fetchone()

    form = requestedBloodSample(request.form)

    print(bloodSampleData)
    if bloodSampleData:
        form.bloodType.data = bloodSampleData[4]
        form.Quantity.data = bloodSampleData[5]
    else:
        form.bloodType.data = ''
        form.Quantity.data = 0

    cursor.close()
    conn.close()

    if request.method == 'POST':
        bloodType           = request.form['bloodType']
        Quantity            = request.form['Quantity']

        if not bloodSampleData:
            conn = connect_db()
            cur = conn.cursor()

            cur.execute(
                "INSERT INTO RequestedBloodSample (appointmentId, recipientId, bloodBankId, bloodType,Quantity) VALUES (%s, %s, %s, %s, %s)",
                (appointmentId,recipientId,bloodBankId, bloodType,Quantity))
            conn.commit()
            cur.close()
            conn.close()
            flash('Requested Blood Sample Collected', category='success')

            return redirect(url_for('adminRecipientAppointment'))
        else:
            conn = connect_db()
            cur = conn.cursor()

            cur.execute(
                "UPDATE RequestedBloodSample SET bloodType=%s, Quantity=%s where appointmentId=%s and recipientId=%s and bloodBankId=%s",
                (bloodType,Quantity,appointmentId, recipientId, bloodBankId))
            conn.commit()
            cur.close()
            conn.close()
            flash('Requested Blood Sample Details Updated', category='success')

            return redirect(url_for('adminRecipientAppointment'))

    return render_template('editRecipientAppointment.html',form=form)


@app.route('/acceptAppointment/<int:appointmentId>/<int:id>/<int:bloodBankId>',methods=['GET', 'POST'])
def acceptAppointment(appointmentId,id,bloodBankId):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Recipient where recipientId = %s',[id])
    recipientData = cursor.fetchone()

    cursor.execute('SELECT * FROM Donor where donorId = %s',[id])
    donorData = cursor.fetchone()

    cursor.close()
    conn.close()

    if request.method == 'POST':

        if donorData:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute("UPDATE donorAppointment SET appointmentstatus = %s where appointmentId=%s",[1,appointmentId])
            conn.commit()

            cur.execute("select * from BloodSample where appointmentId=%s and donorId=%s and bloodBankId = %s",(appointmentId,id,bloodBankId))
            bloodSample = cur.fetchone()

            cur.execute("Insert into Inventory (bloodBankId,BloodType,Quantity) values (%s,%s,%s)",(bloodBankId,bloodSample[4],bloodSample[8]))
            conn.commit()
            cur.close()
            conn.close()
            flash('Donor Accepted', category='success')
            return redirect(url_for('adminDonorAppointment'))
        elif recipientData:
            conn = connect_db()
            cur = conn.cursor()

            cur.execute("select * from RequestedBloodSample where appointmentId=%s and recipientId=%s and bloodBankId = %s",(appointmentId,id,bloodBankId))
            requestedBloodSample = cur.fetchone()

            cur.execute(
                "select * from ViewInventory where bloodBankId=%s and bloodType=%s",(requestedBloodSample[3],requestedBloodSample[4]))
            inventory = cur.fetchone()
            print(inventory)
            if inventory and int(inventory[6]) > 0:

                cur.execute("UPDATE recipientAppointment SET appointmentStatus =%s where appointmentId=%s",
                            [1, appointmentId])
                conn.commit()

                cur.execute("Insert into Inventory (bloodBankId,BloodType,Quantity) values (%s,%s,%s)",(bloodBankId,requestedBloodSample[4],(-1 * requestedBloodSample[5])))
                conn.commit()
                cur.close()
                conn.close()
                flash('Recipient Accepted', category='success')
            else:
                flash('Not Enough Inventory Available', category='error')

            return redirect(url_for('adminRecipientAppointment'))

    if donorData:
        return redirect(url_for('adminDonorAppointment'))
    else:
        return redirect(url_for('adminRecipientAppointment'))

@app.route('/deleteAppointment/<int:appointmentId>/<int:id>/<int:bloodBankId>',methods=['GET', 'POST'])
def deleteAppointment(appointmentId,id,bloodBankId):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Recipient where recipientId = %s',[id])
    recipientData = cursor.fetchone()

    cursor.execute('SELECT * FROM Donor where donorId = %s',[id])
    donorData = cursor.fetchone()

    cursor.close()
    conn.close()

    if request.method == 'POST':

        if donorData:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute("UPDATE donorAppointment SET appointmentStatus = %s where appointmentId =%s",[2,appointmentId])
            conn.commit()
            cur.close()
            conn.close()
            flash('Donor Appointment Rejected', category='success')
            return redirect(url_for('adminDonorAppointment'))
        elif recipientData:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute("UPDATE recipientAppointment SET appointmentStatus =%s where appointmentId =%s",[2,appointmentId])
            conn.commit()
            cur.close()
            conn.close()
            flash('Recipient Appointment Rejected', category='success')
            return redirect(url_for('adminRecipientAppointment'))

    if donorData:
        return redirect(url_for('adminDonorAppointment'))
    else:
        return redirect(url_for('adminRecipientAppointment'))

@app.route('/adminAppointmentHistory',methods=['GET', 'POST'])
def adminAppointmentHistory():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM AppointmentHistory')
    appointmentHistory = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('appointmentHistory.html',appointmentHistory=appointmentHistory)

@app.route('/userAppointmentHistory',methods=['GET', 'POST'])
def userAppointmentHistory():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM userAppointmentHistory where userId=%s",[session['id']])
    appointmentHistory = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('userAppointmentHistory.html',appointmentHistory=appointmentHistory)

@app.route('/bloodStock',methods=['GET', 'POST'])
def bloodStock():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM ViewInventory')
    bloodStock = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('bloodStock.html',bloodStock=bloodStock)

@app.route('/donorDashboard',methods=['GET', 'POST'])
def donorDashboard():
    conn = connect_db()
    cursor = conn.cursor()
    donorId = session['id']
    cursor.execute('SELECT * FROM Donor where donorId = %s',[donorId])
    donorData = cursor.fetchone()

    form = donorForm(request.form)

    print(donorData)

    form.name.data = donorData[1]
    form.contact.data = donorData[2]
    form.email.data = donorData[3]
    form.bloodType.data = donorData[4]
    form.dob.data = donorData[5]
    form.gender.data = donorData[6]

    cursor.close()
    conn.close()

    if request.method == 'POST':
        name        = request.form['name']
        contact     = request.form['contact']
        email       = request.form['email']
        bloodType   = request.form['bloodType']
        dateOfBirth = request.form['dob']
        gender      = request.form['gender']

        # Create Cursor
        conn = connect_db()
        cur = conn.cursor()

        cur.execute("UPDATE DONOR SET NAME=%s,CONTACT=%s,EMAIL=%s,BLOODTYPE=%s,DOB=%s,GENDER=%s where DONORID = %s"
                    , (name,contact,email,bloodType,dateOfBirth,gender,donorId))
        conn.commit()
        cur.close()
        conn.close()
        flash('Donor Details Updated', category='success')

        return redirect(url_for('donorDashboard'))

    return render_template('donorDashboard.html',form=form)

@app.route('/recipientDashboard',methods=['GET', 'POST'])
def recipientDashboard():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Recipient where recipientId = %s',[session['id']])
    recipientData = cursor.fetchone()
    form = donorForm(request.form)

    print(recipientData)

    form.name.data = recipientData[1]
    form.contact.data = recipientData[2]
    form.email.data = recipientData[3]
    form.bloodType.data = recipientData[4]
    form.dob.data = recipientData[5]
    form.gender.data = recipientData[6]

    cursor.close()
    conn.close()

    if request.method == 'POST':
        name        = request.form['name']
        contact     = request.form['contact']
        email       = request.form['email']
        bloodType   = request.form['bloodType']
        dateOfBirth = request.form['dob']
        gender      = request.form['gender']

        # Create Cursor
        conn = connect_db()
        cur = conn.cursor()

        cur.execute("UPDATE RECIPIENT SET NAME=%s,CONTACT=%s,EMAIL=%s,RequiredBloodType=%s,DOB=%s,GENDER=%s where recipientId = %s"
                    , (name,contact,email,bloodType,dateOfBirth,gender,session['id']))
        conn.commit()
        cur.close()
        conn.close()
        flash('Recipient Details Updated', category='success')

        return redirect(url_for('recipientDashboard'))

    return render_template('recipientDashboard.html',form=form)
@app.route('/aboutUs',methods=['GET', 'POST'])
def aboutUs():
    return render_template('aboutUs.html')

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
