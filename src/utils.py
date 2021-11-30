
import webbrowser
import os
import socket
import shutil


def get_env_data_as_dict(path: str) -> dict:
    with open(path, 'r') as f:
        return dict(tuple(line.replace('\n', '').split('=')) for line
                    in f.readlines() if not line.startswith('#'))


def unZipFiles(fileName):
    from zipfile import ZipFile
    with ZipFile(fileName+'.zip', 'r') as f:
        f.extractall()


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
        'http://'+socket.gethostbyname_ex(socket.gethostname())[-1][-1]+':'+str(get_env_data_as_dict('./.env')["port"])+'/')
