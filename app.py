from flask import Flask,render_template,request,flash,session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__,template_folder='templates')

app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Silentkiller@7'
app.config['MYSQL_DB'] = 'bbms'

mysql = MySQL(app)

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

        cursor = mysql.connection.cursor()

        cursor.execute('SELECT * FROM BloodLinkUsers WHERE email = %s AND password = %s', (email, check_password_hash(password1,password1)))
        account = cursor.fetchone()

        if account:
            flash('Account already exists!', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        else:
            cursor.execute('''INSERT INTO BloodLinkUsers (Email,Password,UserType)
                                        VALUES(%s,%s,%s) '''
                           , (email,generate_password_hash(passwd),userType))

            mysql.connection.commit()

            cursor.execute('SELECT * FROM BloodLinkUsers WHERE email = %s AND password = %s', (email, check_password_hash(password1,password1)))
            account = cursor.fetchone()
            print(account)
            if userType == 'Donor':
                cursor.execute('''INSERT INTO DONOR (DonorId,Name,Contact,Email,BloodType,DOB,Gender,Address)
                                VALUES(%s,%s,%s,%s,%s,%s,%s,%s) '''
                               ,(account[0],name,phoneNumber,email,bloodType,dateOfBirth,gender,''))
            else:
                cursor.execute('''INSERT INTO RECIPIENT (RecipientId,Name,Contact,Email,BloodType,DOB,Gender,Address)
                                            VALUES(%s,%s,%s,%s,%s,%s,%s,%s) '''
                               , (account[0],name, phoneNumber, email, bloodType, dateOfBirth, gender, ''))
            mysql.connection.commit()
            cursor.close()


    return render_template('signup.html')

@app.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        # Create variables for easy access
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM BloodLinkUsers WHERE email = %s AND password = %s', (email, check_password_hash(password,password)))
        account = cursor.fetchone()
        print(account)
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account[0]
            session['email'] = account[1]
            flash('Logged in successfully!',category='success')
            return  render_template('index.html')
        else:
            flash('Incorrect username/password!',category='error')
    return render_template('login.html')

@app.route('/logout',methods=['GET', 'POST'])
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    flash('Logged out successfully!',category='success')
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
