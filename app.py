import os
from os.path import join, dirname
from dotenv import load_dotenv

from flask import Flask, render_template, request, jsonify, redirect, url_for, make_response
from pymongo import MongoClient
import hashlib
import jwt
from datetime import datetime 

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)

db = client[DB_NAME]


app = Flask(__name__)

SECRET_KEY = "SPARTA"


def is_user_authenticated(token):
    if not token:
        return False

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return True
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return False

@app.route('/')
def homepage():
    return render_template('homepage_sebelum_login.html')

@app.route('/login')
def login():
    return render_template('sign-up-&-sign-in.html')


# succes
@app.route('/success')
def success():
    return render_template('succes-page.html')


@app.route('/home')
def homepage_after_login():
    return render_template("homepage_setelah_login.html")     


@app.route("/sign_in", methods=["POST"])
def user_sign_in():
    username_receive = request.form["username_give"]
    password_receive = request.form["password_give"]

    pw_hash = hashlib.sha256(password_receive.encode("utf-8")).hexdigest()

    user = db.signup.find_one({"username": username_receive, "password": pw_hash})

    if user is not None:
        return jsonify({"result": "success"})
    else:
        return jsonify(
            {"result": "fail", "msg": "Invalid username or password."})
        
        
@app.route("/sign_up", methods=["POST"])
def user_sign_up():
    name_receive = request.form["name_give"]
    username_receive = request.form["username_give"]
    email_receive = request.form["email_give"]
    password_receive = request.form["password_give"]

    user = db.signup.find_one({"username": username_receive})
    if user:
        return jsonify(
            {
                "result": "fail",
                "msg": "An account with username {} already exists. Please Login!".format(
                    username_receive
                ),
            }
        )

    pw_hash = hashlib.sha256(password_receive.encode("utf-8")).hexdigest()

    db.signup.insert_one(
        {
            "name": name_receive,
            "username": username_receive,
            "email": email_receive,
            "password": pw_hash,
        }
    )

    return jsonify({"result": "success"})

# join member

@app.route('/join_member')
def form_join_member():
    return render_template('join-member.html')

@app.route("/join_member", methods=["POST"])
def join_member():
    name_receive = request.form["name_give"]
    address_receive = request.form["address_give"]
    telfon_receive = request.form["telfon_give"]
    package_receive = request.form["package_give"]
    payment_receive = request.form["payment_give"]
 
    db.member.insert_one(
        {
            "name": name_receive,
            "address": address_receive,
            "telfon": telfon_receive,
            "package": package_receive,
            "payment": payment_receive,
        }
    )

    return jsonify({"result": "success"})


# end join member

@app.route('/index')
def home_admin():
    return render_template('index.html')

@app.route('/admin/login')
def login_admin():
    return render_template('login-admin.html')

@app.route('/admin/register')
def register_admin():
    return render_template('register.html')


@app.route('/admin/fasilitas/tambah_data')
def tambahData_fasilitas():
    return render_template('tambah_data_fasilitas.html')

@app.route('/admin/fasilitas')
def fasilitas_form():
    return render_template('fasilitas_data.html')

@app.route('/home/member/testimonials')
def testimonials():
    return render_template('testimonials.html')

@app.route('/home/member')
def home_member():
    return render_template('homepage_setelah_l&m.html')




        
@app.route("/admin/sign_up", methods=["POST"])
def admin_sign_up():
    name_receive = request.form["name_give"]
    username_receive = request.form["username_give"]
    email_receive = request.form["email_give"]
    password_receive = request.form["password_give"]

    user = db.signup.find_one({"username": username_receive})
    if user:
        return jsonify(
            {
                "result": "fail",
                "msg": "An account with username {} already exists. Please Login!".format(
                    username_receive
                ),
            }
        )

    pw_hash = hashlib.sha256(password_receive.encode("utf-8")).hexdigest()

    db.signup.insert_one(
        {
            "name": name_receive,
            "username": username_receive,
            "email": email_receive,
            "password": pw_hash,
        }
    )

    return jsonify({"result": "success"})


@app.route("/admin/sign_in", methods=["POST"])
def admin_sign_in():
    username_receive = request.form["username_give"]
    password_receive = request.form["password_give"]

    pw_hash = hashlib.sha256(password_receive.encode("utf-8")).hexdigest()

    user = db.signup.find_one({"username": username_receive, "password": pw_hash})

    if user is not None:
        return jsonify({"result": "success"})
    else:
        return jsonify(
            {"result": "fail", "msg": "Invalid username or password."}
        )



@app.route('/fasilitas', methods=['GET'])
def show_fasilitas():
    fasilitas = list(db.fasilitas.find({},{'_id':False}))
    return jsonify({'fasilitas': fasilitas})

@app.route('/fasilitas', methods=['POST'])
def tambahFasilitas():
    nama_receive = request.form["nama_give"]
    gambar = request.files['gambar_give']
    extension = gambar.filename.split('.')[-1]
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
    gambarname = f'gambar-{mytime}.{extension}'
    save_to = f'static/{gambarname}'
    gambar.save(save_to)

    doc = {
        'nama': nama_receive,
        'gambar': gambarname,
    }
    db.fasilitas.insert_one(doc),
    return jsonify({'msg':'Yeayy! Data Berhasil di Upload!'})


# Add this route to fetch the data from the database and return it to the client
@app.route("/admin/fasilitas/data", methods=["GET"])
def get_fasilitas_data():
    # Assuming you are using pymongo to interact with MongoDB
    fasilitas_data = list(db.fasilitas.find({}, {"_id": 0}))

    return jsonify(fasilitas_data)


# crud member admin

@app.route('/admin/membership')
def form_membership():
    return render_template('membership_data.html')


@app.route("/admin/membership", methods=["POST"])
def membership():
    name_receive = request.form["nama_give"]
    address_receive = request.form["address_give"]
    telfon_receive = request.form["telfon_give"]
    package_receive = request.form["package_give"]
    payment_receive = request.form["payment_give"]
 
    db.membership.insert_one(
        {
            "name": name_receive,
            "address": address_receive,
            "telfon": telfon_receive,
            "package": package_receive,
            "payment": payment_receive,
        }
    )

    return jsonify({"result": "success"})

# Add this route to fetch the data from the database and return it to the client
@app.route("/admin/membership/data", methods=["GET"])
def get_membership_data():
    # Assuming you are using pymongo to interact with MongoDB
    membership_data = list(db.membership.find({}, {"_id": 0}))

    return jsonify(membership_data)


# crud user admin

@app.route('/admin/user_data')
def form_user_data():
    return render_template('user_data.html')


@app.route("/admin/user_data", methods=["POST"])
def user_data():
    name_receive = request.form["name_give"]
    username_receive = request.form["username_give"]
    email_receive = request.form["email_give"]
    password_receive = request.form["password_give"]
    
    pw_hash = hashlib.sha256(password_receive.encode("utf-8")).hexdigest()
 
    db.user_data.insert_one(
        {
            "name": name_receive,
            "username": username_receive,
            "email": email_receive,
            "password": pw_hash,
        }
    )

    return jsonify({"result": "success"})

# Add this route to fetch the data from the database and return it to the client
@app.route("/admin/user_data/data", methods=["GET"])
def get_userData_data():
    # Assuming you are using pymongo to interact with MongoDB
    user_data = list(db.user_data.find({}, {"_id": 0}))

    return jsonify(user_data)

# crud user admin

@app.route('/admin/testimoni')
def form_testimoni():
    return render_template('testimoni_data.html')


@app.route("/admin/testimoni", methods=["POST"])
def testimoni():
    name_receive = request.form["name_give"]
    rating_receive = request.form["rating_give"]
    comment_receive = request.form["comment_give"]
    

 
    db.testimoni.insert_one(
        {
            "name": name_receive,
            "rating": rating_receive,
            "comment": comment_receive,
        }
    )

    return jsonify({"result": "success"})


# Add this route to fetch the data from the database and return it to the client
@app.route("/admin/testimoni/data", methods=["GET"])
def get_testimoni_data():
    # Assuming you are using pymongo to interact with MongoDB
    testimoni_data = list(db.testimoni.find({}, {"_id": 0}))

    return jsonify(testimoni_data)

if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)
