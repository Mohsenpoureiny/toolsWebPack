from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from urllib.parse import unquote_plus
import os
import shutil
import uuid

app = Flask(__name__)


def deleteZipFiles():
    directory = "./"
    files_in_directory = os.listdir(directory)
    filtered_files = [
        file for file in files_in_directory if file.endswith(".zip")]
    for file in filtered_files:
        path_to_file = os.path.join(directory, file)
        os.remove(path_to_file)


@app.route("/")
def home():
    dirlist = os.listdir("./files")
    filesData = []
    for cat in dirlist:
        filesTemp = {}
        filesTemp[cat] = os.listdir("./files/"+cat)
        filesData.append(filesTemp)
    return render_template("index.html", dirlist=dirlist, filesData=filesData)


@app.route("/upload", methods=['POST'])
def about():
    if request.method == "POST":
        files = request.files.getlist("files[]")
        for file in files:
            fileName = file.filename
            file.save(os.path.join(
                "./files/"+request.form["category"], fileName))
        return redirect(url_for('home'))


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
    os.remove("./files/" + unquote_plus(category)+"/"+unquote_plus(name))
    return redirect(url_for('home'))


@app.route("/delete/<category>")
def deleteCategory(category):
    os.rmdir("./files/" + unquote_plus(category))
    return redirect(url_for('home'))


@app.route("/create/<category>")
def createCategory(category):
    os.mkdir("./files/" + unquote_plus(category))
    return redirect(url_for('home'))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
