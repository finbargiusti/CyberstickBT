# import the Flask class from the flask module
from flask import Flask, render_template, redirect, \
    url_for, request, session, flash, jsonify, Markup, Response
from functools import wraps
import dataset
import subprocess
import shutil
import glob
import time
import os
import flask
from flask import send_from_directory
from werkzeug import secure_filename
from jinja2 import Environment
from jinja2.loaders import FileSystemLoader
# create the application object


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp3', 'mp4', 'zip', 'rar', 'tar.gz', 'py', 'html', 'jar', 'js', 'css', 'rb', 'cpp', 'c', 'sql', 'exe', 'odt', 'ppt', 'php', 'xml','phtml', 'app', 'stl'])

app = Flask(__name__)

# config
app.secret_key = 'you shall not pass'
db = dataset.connect('sqlite:///databse/users.db')
users = db['users']
posts= db['posts']
replies = db['replies']


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/upload', methods=['GET', 'POST', 'VIEW'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    path = "/home/pi/www/static/uploads/"
    now = time.time()
    upPath = path+str(now)
    os.mkdir(upPath)
    UPLOAD_FOLDER = upPath
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    return render_template('upload.html', displayPath=now)

@app.route('/konami')
def konami():
	return render_template('konami.html')

def stream_template(template_name, **context):
    app.update_template_context(context)
    t = app.jinja_env.get_template(template_name)
    rv = t.stream(context)
    rv.enable_buffering(5)
    return rv

@app.route('/contact')
def contact():
	return render_template('contact.html')


@app.route('/upload', methods=['ENCRYPT'])
def upload_encrypt():
	encrypt_data = request.form['encryptKey']
	return(encryptKey)

@app.route('/download/<id>')
def download(id):
	text = id
	testAge = time.time()
	if testAge-float(text) >= 900:
		shutil.rmtree('/home/pi/www/static/uploads/'+text)
		return "This file was deleted for being too old"
	path = "/home/pi/www/static/uploads/"
	files = path+text+"/"
	fileName = os.listdir(files)
	fileLol = [i.split() for i in fileName]
	linkzor = ""
	numbor = 0
	
	print fileLol
	timez = len(fileLol)
	if timez == 0:
		linkzor = "No files in session."
	for x in range(timez):
		linkzor += Markup('<li><a href="/static/uploads/'+text+'/'+str(fileName[numbor])+'" download="'+str(fileName[numbor])+'">'+str(fileName[numbor])+'</a></li>')
		numbor += 1
	seconds = round(900-(testAge-float(text)), 0)
	print seconds
	m, s = divmod(seconds, 60)
	timeRemain = "%02d minutes %02d seconds" % (m,s)
	print timeRemain
	return render_template('downloader.html', lolzor=linkzor, timeRemain2=timeRemain )

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/')
def home():
	return render_template("index.html")

# ignore from here on -------------------------

@app.route('/maxlisten')
def maxlisten():
	return('Max stop watching vines')

@app.route('/patrick')
def patrick():
	return('got your ip dos time')
	print jsonify({'ip': request.remote_addr}), 200


@app.route('/easteregg')
def easteregg():
	return render_template("csdsports.html")

@app.route('/said')
def said():
	return render_template('said.html')

@app.route('/joshua')
def joshua():
	return render_template("joshua.html")

#y route for handling the login page logic
@app.route('/brian')
def brian():
	return render_template('brian.html')

@app.route('/eetu')
def eetu():
    return render_template("html.html")
	

@app.route('/oscar')
def oscar():
	return render_template("folder/index.html")

@app.errorhandler(404)
def error404(e):
	return render_template("error.html"), 404

@app.errorhandler(500)
def error500(e):
        return render_template("error.html"), 500 


@app.route('/csdget')
def csdget():
	return render_template('csdget.html')

app.run(host='0.0.0.0', port=80, debug=True)
