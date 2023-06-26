from pymongo import MongoClient
from datetime import datetime, timedelta
from flask import  Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask (__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['UPLOAD_FOLDER'] = './static/profile_pics'

password = 'atlaspw24'
con_str = f'mongodb+srv://xz_gen:{password}@cluster0.b2xpcwp.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(con_str)
db = client.dbsparta

@app.route('/', methods=['GET'])
def home():
    return render_template('homepage.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)