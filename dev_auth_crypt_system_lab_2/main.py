from flask import Flask, render_template, request, redirect, url_for, session
import models as dbHandler
from random import randint
import hashlib
from flask_mail import Mail, Message
from decorators import async_func

app = Flask(__name__)
app.secret_key = '73870e7f-634d-433b-946a-8d20132bafac'

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'authsystemtest@gmail.com'  # введите свой адрес электронной почты здесь
app.config['MAIL_DEFAULT_SENDER'] = 'authsystemtest@gmail.com'  # и здесь
app.config['MAIL_PASSWORD'] = '123QWEasd!'  # введите пароль

mail = Mail(app)

@app.route('/temp_code', methods=['POST', 'GET'])
def check_code():
    if session.get('data')['login'] == 'Process':
        username = session.get('data')['username']
        temp_code_bd = dbHandler.get_temp_code(username)[0][0]
        if request.method=='POST':
            temp_code_from_user = request.form['temp_code']
            temp_code_from_user_md5 = str(hashlib.md5(str(temp_code_from_user).encode()).hexdigest())
            if temp_code_bd == temp_code_from_user_md5:
                session['data'] = dict(username=username, login='True')
                return redirect(url_for('success'))
            else:
                return render_template('temp_code.html', tempcodefalse=True)
        else:
            return render_template('temp_code.html')
    else:
        return redirect(url_for('login'))

@app.route('/success')
def success():
    if session.get('data')['login'] == 'True':
        username = session['data']['username']
        return render_template('success.html', name=username)
    else:
        return redirect(url_for('login'))

@async_func
def send_async_email(msg):
    with app.app_context():
        mail.send(msg)

def generate_and_send_temp_code(username, email):
    temp_code = randint(10000, 99999)
    hash_temp_code = str(hashlib.md5(str(temp_code).encode()).hexdigest())
    #send code email
    msg = Message("Код подтверждения", recipients=[email])
    msg.body = "Ваш код подтверждения - {}".format(temp_code)
    send_async_email(msg)
    return hash_temp_code


@app.route('/', methods=['POST', 'GET'])
def login():
    session['data'] = dict(login='False')
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        user = dbHandler.retrieveUsers(username)
        if user:
            if password == user[0][1]:
                email = user[0][2]
                md5_hash_temp_code = generate_and_send_temp_code(username, email)
                dbHandler.insert_temp_code(username, md5_hash_temp_code)
                session['data'] = dict(username=username, login='Process')
                return redirect(url_for('check_code'))
            else:
                return render_template('index.html', Passwordfalse=True)
        else:
            return render_template('index.html', loggedfalse=True)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)