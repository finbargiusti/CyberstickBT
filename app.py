import os
import time
from random import randint
import jinja2
from flask import Flask, render_template, request, jsonify, Markup
from flask import send_from_directory
from werkzeug import secure_filename

# create the application object

ADVECTIVE_1 = ['shiny', 'flying', 'explosive', 'fantastic', 'embarrassed', 'flashy', 'stingy', 'dapper', 'implosive',
               'confusing']
COLOUR = ['white', 'red', 'emerald', 'maroon', 'umber', 'ivory', 'jasper', 'chocolate', 'jade', 'silver']
NOUN = ['bomb', 'direction', 'push', 'medic', 'pie', 'eggnog', 'quartz', 'border', 'cub', 'soldier']
PIC_EXTENSIONS = ['aac', 'ai', 'aiff', 'avi', 'c', 'cpp', 'css', 'dat', 'dmg', 'doc', 'exe', 'flv', 'gif', 'h', 'hpp',
                  'html', 'ics', 'jar', 'jpg', 'key', 'mid', 'mp3', 'mpg', 'pdf', 'php', 'png', 'ppt', 'psd', 'py',
                  'qt', 'rar', 'rb', 'rtf', 'sql', 'tiff', 'txt', 'wav', 'xls', 'xml', 'yml', 'zip']

app = Flask(__name__)

# config
app.secret_key = 'you shall not pass'


@app.route('/uploadz/<sid>', methods=['GET', 'POST', 'VIEW'])
def upload_fileAP(sid):
    text = ''
    seises = os.listdir("/home/finbar/www/static/uploads")
    for x in range(len(seises)):
        if sid in seises[x]:
            text = seises[x]
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file_path = "/home/finbar/www/static/uploads/" + text + "/"
            file.save(os.path.join(file_path, filename))
            return send_from_directory(file_path, filename)


def isacceptedpic(extension):
	if extension in PIC_EXTENSIONS:
		return True


@app.route('/premium')
def premium():
    return render_template("premium.html")


@app.route('/uploadandroid')
def upload_android():
    path = "/home/finbar/www/static/uploads/"
    now = time.time()
    randomNumber = randint(0, 9)
    name = ADVECTIVE_1[int(randomNumber)]
    randomNumber = randint(0, 9)
    name += COLOUR[int(randomNumber)]
    randomNumber = randint(0, 9)
    name += NOUN[int(randomNumber)]
    seis = name + '-' + str(now)
    upPath = path + seis
    os.mkdir(upPath)
    return render_template('uploadsimplistic.html', displayPath=seis)


@app.route('/downloadfile/<cyberID>/<fileName>')
def downloadzor(cyberID, fileName):
    return send_from_directory("/home/finbar/www/static/uploads/" + cyberID, fileName)


@app.route('/johnluke')
def johnluke():
    return render_template("johnlukesprivatewebsites.html")


@app.route('/api/upload', methods=['GET', 'POST'])
def add_message():
    path = "/home/finbar/www/static/uploads/"
    now = time.time()
    randomNumber = randint(0, 9)
    name = ADVECTIVE_1[int(randomNumber)]
    randomNumber = randint(0, 9)
    name += COLOUR[int(randomNumber)]
    randomNumber = randint(0, 9)
    name += NOUN[int(randomNumber)]
    seis = name + '-' + str(now)
    upPath = path + seis
    os.mkdir(upPath)
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file_path = "/home/finbar/www/static/uploads/" + seis + "/"
            file.save(os.path.join(file_path, filename))
            return (seis)


@app.route('/api/download/<did>')
def downloadApi(did):
    sessionFolder = ""
    sessions = os.listdir("static/uploads")
    for session in sessions:
        name, stime = session.split('-')
        if name == did:
            sessionFolder = session
    fileLoc = os.listdir("/home/finbar/www/static/uploads/" + sessionFolder)
    files = []
    for x in range(len(fileLoc)):
        fileSplit = fileLoc[x].rsplit(".", 1)
        name = fileSplit[0]
        extension = fileSplit[1]
        files.append({'name': name, 'extension': extension})
    filesession = {'session': sessionFolder}
    return jsonify(zfile=files, xfile=filesession)


@app.route('/help')
def help():
    return render_template("help.html")


@app.route('/uplads/<sid>/<filename>')
def uploaded_file(sid, filename):
    print "teste"
    return send_from_directory("/home/finbar/www/static/uploads/" + sid + "/", filename)


@app.route('/upload', methods=['GET', 'POST', 'VIEW'])
def upload_file():
    path = "/home/finbar/www/static/uploads/"
    now = time.time()
    randomNumber = randint(0, 9)
    name = ADVECTIVE_1[int(randomNumber)]
    randomNumber = randint(0, 9)
    name += COLOUR[int(randomNumber)]
    randomNumber = randint(0, 9)
    name += NOUN[int(randomNumber)]
    seis = name + '-' + str(now)
    upPath = path + seis
    os.mkdir(upPath)
    UPLOAD_FOLDER = upPath
    return render_template('upload.html', displayPath=seis, linker=name)


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


@app.route('/download/<did>')
def download(did):
    sessionFolder = ""
    sessions = os.listdir("static/uploads")
    for session in sessions:
        name, stime = session.split('-')
        if name == did:
            sessionTime = stime
            sessionFolder = session
    sessionFilesList = os.listdir("static/uploads/" + sessionFolder + "/")
    print sessionFilesList
    #FIXME Get rid of hard coded html
    seconds = round(900 - (time.time() - float(sessionTime)), 0)
    m, s = divmod(seconds, 60)
    timeRemain = "%02d minutes %02d seconds" % (m, s)
    return render_template('download.html', timeRemain=timeRemain, session=sessionFolder, fileList=sessionFilesList, PIC_EXTENSIONS=PIC_EXTENSIONS)


def istoolong(string):
    return string[:7]+"..."


def short_caption(someitem):
    return len(someitem) < 11

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/')
def home():
    return render_template("index.html")


# ignore from here on -------------------------

@app.route('/maxlisten')
def maxlisten():
    return ('Max stop watching vines')


@app.route('/patrick')
def patrick():
    return ('got your ip dos time')
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


# y route for handling the login page logic
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


app.run(host='0.0.0.0', port=80)
