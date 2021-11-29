from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from urllib.parse import unquote_plus
import os
import shutil
import uuid
import webbrowser
import socket
from threading import Timer


app = Flask(__name__)
port = 5000


def deleteZipFiles():
    directory = "./"
    files_in_directory = os.listdir(directory)
    filtered_files = [
        file for file in files_in_directory if file.endswith(".zip")]
    for file in filtered_files:
        path_to_file = os.path.join(directory, file)
        os.remove(path_to_file)


def open_browser():
    webbrowser.open_new(
        'http://'+socket.gethostbyname_ex(socket.gethostname())[-1][-1]+':'+str(port)+'/')


@app.route("/")
def home():
    print(request.headers)
    host = 'http://' + \
        socket.gethostbyname_ex(socket.gethostname())[-1][-1]+':'+str(port)+'/'
    dirlist = os.listdir("./files")
    filesData = []
    for cat in dirlist:
        filesTemp = {}
        filesTemp[cat] = os.listdir("./files/"+cat)
        filesData.append(filesTemp)
    return render_template("index.html", dirlist=dirlist, filesData=filesData, host=host)


@app.route("/upload", methods=['POST'])
def about():
    try:
        if request.method == "POST":
            files = request.files.getlist("files[]")
            for file in files:
                fileName = file.filename
                file.save(os.path.join(
                    "./files/"+request.form["category"], fileName))
    except:
        return "500"
    return "200"


@app.route("/download/<category>/<name>")
def download(category, name):
    return send_from_directory("./files/", unquote_plus(category)+"/"+unquote_plus(name))


@app.route("/download/<category>")
def downloadCategory(category):
    deleteZipFiles()
    arcName = category+"__"+str(uuid.uuid4())
    shutil.make_archive(arcName, 'zip', './files/'+category)
    return send_from_directory("./", arcName+".zip")


@app.route("/delete/<category>/<name>")
def deleteFile(category, name):
    try:
        os.remove("./files/" + unquote_plus(category)+"/"+unquote_plus(name))
    except:
        pass
    return redirect(url_for('home'))


@app.route("/delete/<category>")
def deleteCategory(category):
    try:
        shutil.rmtree("./files/" + unquote_plus(category), ignore_errors=True)
    except:
        pass
    return redirect(url_for('home'))


@app.route("/create")
def createCategory():
    try:
        os.mkdir("./files/" + request.args["name"])
    except:
        pass
    return redirect(url_for('home'))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    Timer(1, open_browser).start()
    app.run(host="0.0.0.0", port=port, debug=True)
