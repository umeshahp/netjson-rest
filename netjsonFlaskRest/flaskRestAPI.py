from flask import Flask, jsonify, request, send_from_directory, send_file
from netjsonconfig import OpenWrt
import json
import os
import logging
from os.path import expanduser
import socket
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
app = Flask(__name__)

__author__ = 'Umesha HP'

ALLOWED_EXTENSIONS = set(['tar.gz', 'tar', 'gz'])
home = expanduser("~")
path2tmpTar = os.path.join(home, 'tmp')
app.config['UPLOAD_FOLDER'] = path2tmpTar

def ensure_dir(path_dir):
    if os.path.exists(path_dir) is False:
        os.mkdir(path_dir)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/')
def index():
    return "These API's are written in FLASK and Python3!"

@app.route('/spanfi/api/v1/toopen_wrt', methods=['POST'])
def convert_to_openWrt():
    print("Request recieved from Host {}".format(request.remote_addr))
    logging.info("Request recieved from Host {}".format(request.remote_addr))
    data = json.loads(request.data)
    print(data)
    # text = data.get("text", None)
    if len(data) < 1:
        return jsonify({"message": "json data not found"})
    else:
        try:
            obj = OpenWrt(data)
            path2file = os.path.join(path2tmpTar, 'openwrtconfig.tar.gz')
            obj.write('openwrtconfig', path=path2tmpTar)
            logging.debug("Succesfully converted to openwrt")
            return send_file(path2file, as_attachment=True)
        except Exception as err:
            logging.error("Exception in OPENWrt Conversion ", str(err))
            return jsonify({"Exception in OPENWrt Conversion ": str(err)})


@app.route('/spanfi/api/v1/tojson', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    print("Upload_api is called from host {}".format(request.remote_addr))
    logging.info("Upload api is called from host {}".format(request.remote_addr))
    print(len(request.files))
    if 'file' not in  request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        return resp
    file = request.files['file']
    print("File recieved  is {}".format(file.filename))
    if file.filename == '':
        resp = jsonify({'message': 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    if file and allowed_file(file.filename):
        try :
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            router = OpenWrt(native=open(filepath))
            json_schema = router.json()
            return json_schema
        except Exception as err:
            logging.error("Exception in OPENWrt Conversion ", str(err))
            return jsonify({"Exception in OPENWrt Conversion ": str(err)})

    else:
        resp = jsonify({'message': 'Allowed file type is only tar'})
        resp.status_code = 400
        return resp


if __name__ == '__main__':
    ensure_dir(path2tmpTar)
    path2log = os.path.join(path2tmpTar,'logs')
    ensure_dir(path2log)
    logging.basicConfig(filename= os.path.join(path2log,'apps.log'), filemode='w+', format='%(name)s - %(levelname)s - %(message)s')
    logging.warning('This will get logged to a file')
    app.run(host = IPAddr, port = '6000', debug = True)
