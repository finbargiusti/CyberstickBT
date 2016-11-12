# Dis is mein file
import os
import shutil
from pdb import set_trace as bp
import string
import json
import stripe
import string
import time
import datetime
from random import randint
import jinja2
from flask import Flask, render_template, request, jsonify, Markup
from flask import send_from_directory, redirect, session, url_for
from werkzeug import secure_filename
import requests
from tinydb import TinyDB, Query

# exension thumbnails
PIC_EXTENSIONS = [
    'aac', 'ai', 'aiff', 'avi', 'c',
    'cpp', 'css', 'dat', 'dmg', 'doc',
    'exe', 'flv', 'gif', 'h', 'hpp',
    'html', 'ics', 'jar', 'jpg', 'key',
    'mid', 'mp3', 'mpg', 'pdf', 'php',
    'png', 'ppt', 'psd', 'py', 'qt',
    'rar', 'rb', 'rtf', 'sql', 'tiff',
    'txt', 'wav', 'xls', 'xml', 'yml',
    'zip'
]

# stripe key selection
stripe_keys = {
    'secret_key': os.environ['SECRET_KEY'],
    'publishable_key': os.environ['PUBLISHABLE_KEY']
}

stripe.api_key = stripe_keys['secret_key']

# tinyDB database
db = TinyDB('databse/db.json')

app = Flask(__name__)

# get words
word_site = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"

response = requests.get(word_site)
WORDS = response.content.splitlines()


# config
app.secret_key = 'you shall not pass'

# random word generator
def randomword():
    randomNumber = randint(0, len(WORDS))
    return WORDS[randomNumber].capitalize()


# upload confirmer
@app.route('/uploadz/<sid>', methods=['GET', 'POST', 'VIEW'])
def upload_fileAP(sid):
    text = ''
    seises = os.listdir("static/uploads")
    for x in range(len(seises)):
        if sid in seises[x]:
            text = seises[x]
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file_path = "static/uploads/" + text + "/"
            file.save(os.path.join(file_path, filename))
            return send_from_directory(file_path, filename)


# purchase page
@app.route('/buy')
def buy():
    return render_template("selectpurchase.html", isinsession=session)


# buy check and send on
@app.route('/buy', methods=['POST'])
def buycheck():
    sessions = request.form['sessions']
    username = request.form['username']
    if int(sessions) <= 99 or sessions == "":
        return render_template("selectpurchase.html",
                               error="Minimum sessions is 100 sessions",
                               isinsession=session)
    else:
        if username == "":
            return redirect("/checkout/" + sessions)
        else:
            return redirect("/checkout/" + sessions + "/" + username)


# stripe checkout w/o prev username
@app.route('/checkout/<sessions>')
def checkout(sessions):
    return render_template("checkout.html",
                           key=stripe_keys['publishable_key'],
                           num=float(sessions),
                           displnum=sessions,
                           isinsession=session)


# stripe checkout w/ prev username
@app.route('/checkout/<sessions>/<username>')
def checkoutuser(sessions, username):
    return render_template("checkout.html",
                           key=stripe_keys['publishable_key'],
                           num=float(sessions),
                           displnum=sessions,
                           isinsession=session,
                           username=username)


# stripe charge w/o username
@app.route('/charge/<amount>', methods=['POST'])
def charge(amount):

    customer = stripe.Customer.create(
        email='customer@example.com',
        source=request.form['stripeToken']
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency='usd',
        description='Cyberstick Charge'
    )

    while True:
        string = randomword() + randomword() + randomword() + randomword() + randomword()
        if len(db.search(Query().id == string)) == 0:
            db.insert({'id': string, 'uses': int(amount)})
            session['username'] = string
            return render_template('thanks.html',
                                   amount=int(amount),
                                   string=string,
                                   isinsession=session)


# stripe charge w/ username
@app.route('/charge/<amount>/<username>', methods=['POST'])
def chargeuser(amount, username):
    if len(db.search(Query().id == username)) == 1:
        customer = stripe.Customer.create(
            email=request.form['stripeEmail'],
            source=request.form['stripeToken']
        )

        charge = stripe.Charge.create(
            customer=customer.id,
            amount=amount,
            currency='usd',
            description='Cyberstick Charge'
        )
        available = db.search(Query().id == username)
        db.update({'uses': str(int(available[0]['uses']) + int(amount))}, Query().id == username) 
        session['username'] = username
        return render_template('thanks.html',
                                   amount=int(amount),
                                   string=username,
                                   isinsession=session)
    else:
        return render_template("message.html",
                               message="Key not found. Please contact us",
                               isinsession=session)


# user id generator
def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


# download file route
@app.route('/downloadfile/<cyberID>/<fileName>')
def downloadzor(cyberID, fileName):
    return send_from_directory("static/uploads/" + cyberID,
                                fileName)


# api upload
@app.route('/api/upload/<username>', methods=['GET', 'POST'])
def add_message(username):
    path = "static/uploads/"
    available = db.search(Query().id == username)
    if len(available) != 0:
        now = time.time()
        name = randomword()
        name += randomword()
        name += randomword()
        seis = name + '-' + str(now)
        upPath = path + seis
        os.mkdir(upPath)
        if request.method == 'POST':
            file = request.files['file']
            if file:
                filename = secure_filename(file.filename)
                file_path = "static/uploads/" + seis + "/"
                file.save(os.path.join(file_path, filename))
                return (name)
    else:
        return "error"


# api download
@app.route('/api/download/<did>')
def downloadApi(did):
    sessionFolder = ""
    sessions = os.listdir("static/uploads")
    for session in sessions:
        name, stime = session.split('-')
        if name == did:
            sessionTime = stime
            sessionFolder = session
    sessionFilesList = os.listdir("static/uploads/" + sessionFolder + "/")
    files = []
    for tfile in sessionFilesList:
        fileSplit = tfile.rsplit(".", 1)
        name = fileSplit[0]
        if len(fileSplit) >= 1:
            extension = fileSplit[1]
        else:
            extension = "None!"
        files.append({'name': name, 'extension': extension})
    filesession = {'session': sessionFolder}
    return jsonify(zfile=files, xfile=filesession)


# help page
@app.route('/help')
def help():
    return render_template("help.html", isinsession=session)


# manage page
@app.route('/manage')
def manage():
    if 'username' in session:
        available = db.search(Query().id == session['username'])
        if len(available) != 0:
            sessionTime = []
            sessionFolder = []
            sessions = os.listdir("static/uploads")
            for session1 in sessions:
                if len(session1.split('-')) == 3:
                    name, stime, user = session1.split('-')
                    if user == session['username']:
                        seconds = round(86400 - (time.time() - float(stime)), 0)
                        m, s = divmod(float(seconds), 60)
                        h, m = divmod(m, 60)
                        sessionTime.append("%02d hours, %02d minutes and %02d seconds" % (h, m, s))
                        sessionFolder.append(name)
            return render_template("manage.html", 
                                   sessions=sessionFolder,
                                   times=sessionTime,
                                   isinsession=session)
    else:
       return redirect('/login') 
    


# upload page
@app.route('/upload', methods=['GET', 'POST', 'VIEW'])
def upload_file():
    if 'username' in session:
        kid = session['username']
        available = db.search(Query().id == kid)
        if len(available) != 0:
            if int(available[0]['uses']) >= 0:
                path = "static/uploads/"
                now = time.time()
                name = randomword()
                name += randomword()
                name += randomword()
                seis = secure_filename(name) + '-' + str(now) + '-' + session['username']
                upPath = path + seis
                os.mkdir(upPath)
                UPLOAD_FOLDER = upPath
                db.update({'uses': str(int(available[0]['uses']) - 1)}, Query().id == kid)
                return render_template('upload.html',
                                       displayPath=seis,
                                       linker=name,
                                       kid=available[0]['uses'],
                                       isinsession=session)
            else:
                return render_template("message.html",
                                       message="You are out of uses! Buy more!",
                                       isinsession=session)
        else:
            return render_template("message.html",
        floatmessage="Something went wrong! Please contact us",
                                   isinsession=session)
    else:
        path = "static/uploads/"
        now = time.time()
        name = randomword()
        name += randomword()
        name += randomword()
        seis = secure_filename(name) + '-' + str(now)
        upPath = path + seis
        os.mkdir(upPath)
        UPLOAD_FOLDER = upPath
        return render_template('upload.html',
                               displayPath=seis,
                               linker=name,
                               isinsession=session)
    


@app.route('/upload/<seiser>', methods=['GET', 'POST', 'VIEW'])
def edit_session(seiser):
    if 'username' in session:
        kid = session['username']
        available = db.search(Query().id == kid)
        if len(available) != 0:
            sessions = os.listdir("static/uploads")
            for session1 in sessions:
                if len(session1.split('-')) == 3:
                    name, stime, user = session1.split('-')
                    if user == session['username']:
                        sessionFilesList = os.listdir("static/uploads/" + session1 + "/")
                        return render_template('upload.html',
                                               files=sessionFilesList,
                                               displayPath=session1,
                                               linker=name,
                                               kid=available[0]['uses'],
                                               isinsession=session)
        else:
            return render_template("message.html",
        floatmessage="Something went wrong! Please contact us",
                                   isinsession=session)
    else:
        return redirect('/login')

# login page
@app.route('/login', methods=['GET', 'POST', 'VIEW'])
def login():
    if request.method == 'POST':
        key = request.form['username']
        available = db.search(Query().id == key)
        if len(available) != 0:
            session['username'] = key
            return redirect(url_for('upload_file'))
        else:
            return render_template("login.html", error=Markup("Could not find any keys with that id &#9785;"))
    return render_template("login.html", isinsession=session)


# konami easteregg image
@app.route('/konami')
def konami():
    return render_template('konami.html')


# contact page
@app.route('/contact')
def contact():
    return render_template('contact.html', isinsession=session)


# download page
@app.route('/download/<did>')
def download(did):
    sessions = os.listdir("static/uploads")
    for session in sessions:
        name, stime = session.split('-')[0], session.split('-')[1]
        if len(session.split('-')) == 3:
            sessionUser = session.split('-')[2]
        if name == did:
            sessionTime = stime
            sessionFolder = session
    sessionFilesList = os.listdir("static/uploads/" + sessionFolder + "/")
    if sessionUser:
        seconds = round(86400 - (time.time() - float(sessionTime)), 0)
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        timeRemain = "%02d hours, %02d minutes, %02d seconds" % (h, m, s)
    else:
        seconds = round(900 - (time.time() - float(sessionTime)), 0)
        m, s = divmod(seconds, 60)
        timeRemain = "%02d minutes %02d seconds" % (m, s)
    return render_template('download.html',
                           timeRemain=timeRemain,
                           session=sessionFolder,
                           fileList=sessionFilesList,
                           PIC_EXTENSIONS=PIC_EXTENSIONS,
                           isinsession=session)


# delete session from manage
@app.route('/delete/<did>')
def deletesession(did):
    if 'username' in session:
        sessionFolder = ""
        sessions = os.listdir("static/uploads")
        for session1 in sessions:
            name = session1.split('-')[0]
            if len(session1.split('-')) == 3:
                if name == did:
                    if session1.split('-')[2] == session['username']:
                        sessionFolder = session1 
        kid = session['username']
        available = db.search(Query().id == kid)
        if len(available) != 0:
            if sessionFolder is not None:
                if sessionFolder.split('-')[2] == session['username']:
                    shutil.rmtree('static/uploads/'+sessionFolder)
                    return redirect("/manage")
            else:
                return redirect("/manage")


# about page
@app.route('/about')
def about():
    return render_template('about.html', isinsession=session)


# home
@app.route('/')
def home():
    return render_template("index.html", isinsession=session)


# 404 page
@app.errorhandler(404)
def error404(e):
    return render_template("error.html", isinsession=session), 404


# 500 page
@app.errorhandler(500)
def error500(e):
    return render_template("error.html", isinsession=session), 500

app.run(host='0.0.0.0', port=80, debug=True)
