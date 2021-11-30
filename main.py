from src.utils import *
from zipfile import ZipFile
from threading import Timer
import requests
import uuid
import shutil
import os
from urllib.parse import unquote_plus
from flask import Flask, render_template, request, redirect, url_for, send_from_directory


env = get_env_data_as_dict('./.env')
app = Flask(__name__)
render_template_config = {"version": env["VERSION"]}


@app.route("/")
def home():
    dirlist = os.listdir("./files")
    filesData = []
    for cat in dirlist:
        filesTemp = {}
        filesTemp[cat] = os.listdir("./files/"+cat)
        filesData.append(filesTemp)
    return render_template("index.html",
                           dirlist=dirlist,
                           filesData=filesData,
                           **render_template_config)


@app.route("/add/Category")
def addCategory():
    return render_template("addCategory.html", **render_template_config)


@app.route("/upload")
def uploadFile():
    dirlist = os.listdir("./files")
    return render_template("upload.html", dirlist=dirlist,
                           **render_template_config)


@app.route("/add/file", methods=['POST'])
def upload():
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
    url = 'https://mohsenpoureiny.info/toolWeb/latest.txt'
    try:
        r = requests.get(url, allow_redirects=True).content.decode('utf-8')
        if env["VERSION"] not in str(r) and env["mode"] != "dev":
            downloadUrl = f'https://mohsenpoureiny.info/toolWeb/download/{r}.zip'
            print(downloadUrl)
            newVersion = requests.get(downloadUrl, allow_redirects=True)
            open("newVersion.zip", "wb").write(newVersion.content)
            unZipFiles("newVersion")
            deleteZipFiles()
            print("Updated!")
        else:
            print("Updated!")
    except:
        print("Connect to Internet For Update Check")
    port = int(os.environ.get('PORT', 5000))
    if env["mode"] != "dev":
        Timer(1, open_browser).start()
    app.run(host="0.0.0.0", port=port, debug=True)
