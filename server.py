import os
from flask import Flask, request, redirect, url_for, send_from_directory,flash, render_template
from werkzeug.utils import secure_filename
from flipFlop import *
import json
import codecs


from urllib.request import urlopen
import re

# Setup Flask app.
app = Flask(__name__)
UPLOAD_FOLDER = "./upload"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS= set(['txt'])

app.debug = True
app.secret_key = 'some secret key'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Routes
@app.route('/')
def root():
  return app.send_static_file('index.html')

@app.route('/upload/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/', methods=[ 'GET','POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            #return redirect(request.url)
        file = request.files['file']
        twofile = request.files['twofile']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file You idiot')
            #return redirect(request.url)
        if file and allowed_file(file.filename):#triggered if the allowed file is uploaded
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            with codecs.open(os.path.join(UPLOAD_FOLDER, filename), 'r',encoding='utf-8', errors='ignore') as myfile:
                data=str(myfile.read()).replace("\n", "").replace("/", "").replace(",", "").replace("(", "").replace(")", "").replace("-", "").replace("\"", "").replace("'", "")
            filedata1= str(data).split('.')
            #print(filedata1)
            #file 2
        if twofile.filename == '':
            flash('No selected file You idiot')
            #return redirect(request.url)
        if twofile and allowed_file(twofile.filename):#triggered if the allowed file is uploaded
            filename = secure_filename(twofile.filename)
            twofile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            with codecs.open(os.path.join(UPLOAD_FOLDER, filename), 'r',encoding='utf-8', errors='ignore') as myfile:
                twodata=str(myfile.read()).replace("\n", "").replace("/", "").replace(",", "").replace("(", "").replace(")", "").replace("-", "").replace("\"", "").replace("'", "")
            filedata2= str(twodata).split('.')
            #print(filedata2)

            #return redirect(url_for('uploaded_file',filename=filename))
            filedata1=filedata1[0:min(len(filedata1),100)]
            filedata2=filedata2[0:min(len(filedata2),100)]

            bulkdata = filedata1 +filedata2
            #print(bulkdata)
            retData=flipFlopped(bulkdata)
            #retData= [["ddfssdf",["32320"],["fdssd"]]]
            #print(retData)
            result = {}
            #result[str(filedata2[:10])]=filedata2
            #result[str(filedata2[:10])]=filedata1
            for i in retData:
                for j in range(len(i[1])):
                    result[i[0]]= " <<<<<FLIPFLOPP>>>>>: "+i[1][j]
                for j in range(len(i[2])):
                    result[i[0]]=" <<<<<CONSISTENT>>>>>: "+i[2][j]
            return render_template("result.html",result = result)
            # first cut file lenghts down  the concat them
    else:
        return app.send_static_file('index.html')






@app.route('/<path:path>')
def static_proxy(path):
  # send_static_file will guess the correct MIME type
  return app.send_static_file(path)


if __name__ == '__main__':
    app.run(host= "0.0.0.0", debug=True,use_reloader=False, port=80)
