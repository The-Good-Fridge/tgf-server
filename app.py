from flask import Flask, request, jsonify
import pyrebase
import json
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

config = {
    "apiKey": "AIzaSyCOAo72xGq_9wtWzOmH-NQljf5IDlOEoFM",
    "authDomain": "thegoodfridge-74422.firebaseapp.com",
    "databaseURL": "https://thegoodfridge-74422.firebaseio.com",
    "projectId": "thegoodfridge-74422",
    "storageBucket": "thegoodfridge-74422.appspot.com",
    "messagingSenderId": "892903011031",
    "appId": "1:892903011031:web:b3f11720dfb8105f127692",
    "measurementId": "G-QHL6DH1KMD"
}

firebase = pyrebase.initialize_app(config)

auth = firebase.auth()

cred = credentials.Certificate('./serviceAccountKey.json')
default_app = firebase_admin.initialize_app(cred)

db = firestore.client()

@app.route("/")
def index():
    return "<h1> Hello World </h1>"

@app.route('/api/login', methods=['GET'])
def login():
    email = request.args.get('email')
    password = request.args.get('password')
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        ret = "Login Successful" #+ str(user)
        return ret, 200

    except Exception as e:
        response = e.args[0].response
        error = response.json()['error']
        return error

@app.route('/api/register', methods=['GET'])
def register():
    email = request.args.get('email')
    password = request.args.get('password')
    try:
        user = auth.create_user_with_email_and_password(email, password)
        # auth.send_email_verification(user['idToken'])
        ret = "Register Successful " + str(user)
        return ret, 200

    except Exception as e:
        response = e.args[0].response
        error = response.json()['error']
        return error, 400
        # return str(e)#"Account already taken. Please sign in", 400

@app.route('/api/values', methods=['GET', 'POST', 'PUT'])
def post_values():
    email = request.args.get('email[]')
    first_name = request.args.get('first_name[]')
    last_name = request.args.get('last_name[]')

    value1 = "true" == request.args.get('environment[]')
    value2 = "true" == request.args.get('animal[]')
    value3 = "true" == request.args.get('human[]')

    environment_issues = request.args.getlist('environment_issues[]')
    animal_issues = request.args.getlist('animal_issues[]')
    human_issues = request.args.getlist('human_issues[]')

    try:
        ref = db.collection(u'users').document(str(email))
        ref.set({
            u'first_name': first_name,
            u'last_name': last_name,
            u'environment': value1,
            u'animal': value2,
            u'human': value3,
            u'environment_issues': environment_issues,
            u'animal_issues': animal_issues,
            u'human_issues': human_issues
        })
        return 'Success', 200

    except Exception as e:
        ret = 'Failed with error: ' + str(e)
        return ret, 400

@app.route('/api/values/update', methods=['GET', 'POST', 'PUT'])
def update_values():
    email = request.args.get('email[]')
    first_name = request.args.get('first_name[]')
    last_name = request.args.get('last_name[]')

    value1 = "true" == request.args.get('environment[]')
    value2 = "true" == request.args.get('animal[]')
    value3 = "true" == request.args.get('human[]')

    environment_issues = request.args.getlist('environment_issues[]')
    animal_issues = request.args.getlist('animal_issues[]')
    human_issues = request.args.getlist('human_issues[]')

    try:
        ref = db.collection(u'users').document(str(email))
        ref.update({
            u'first_name': first_name,
            u'last_name': last_name,
            u'environment': value1,
            u'animal': value2,
            u'human': value3,
            u'environment_issues': environment_issues,
            u'animal_issues': animal_issues,
            u'human_issues': human_issues
        })
        return 'Success', 200

    except Exception as e:
        ret = 'Failed with error: ' + str(e)
        return ret, 400

@app.route('/data', methods=['GET'])
def get_data():
    email = request.args.get('email')

    try:
        ref = db.collection(u'users').document(str(email))
        data = ref.get()

        return jsonify(data.to_dict()), 200

    except Exception as e:
        ret = 'Failed with error: ' + str(e)
        return ret, 400


@app.route('/grocery_list/get', methods=['GET'])
def get_grocery():
    email = request.args.get('email')

    try:
        ref = db.collection(u'users').document(str(email))
        data = ref.get()

        return jsonify(data.to_dict()), 200

    except Exception as e:
        ret = 'Failed with error: ' + str(e)
        return ret, 400

@app.route('/grocery_list', methods=['POST'])
def post_grocery():
    email = request.args.get('email[]')
    g_list = request.args.getlist('items[]')
    print(email, g_list)

    #if g_list:
    #    g_list = g_list.replace('\'', '')
    #    g_list = g_list.replace(', ', ',')
    #    g_list = g_list.split(',')

    try:
        ref = db.collection(u'groceries').document(str(email))
        if g_list:
            ref.set({
                u'email': email,
                u'grocery_list': g_list
            })
        else:
            raise Exception('Empty grocery list')
            #g_list = jsonify(ref.get().to_dict()['grocery_list'])
        
        grocery_dict = {
            "recommendations": g_list,
            "other": g_list
        }

        return grocery_dict, 200

    except Exception as e:
        ret = 'Failed with error: ' + str(e)
        return ret, 400

def check_grocery(g_list):
    print(g_list)

@app.route('/goal', methods=['GET', 'POST', 'PUT'])
def goal():
    email = request.args.get('email')
    goal = request.args.get('goal')
    progress = request.args.get('progress')

    if goal:
        goal = int(goal)

    if progress:
        progress = int(progress)

    try:
        ref = db.collection(u'users').document(str(email))

        if goal:
            if progress:
                update = {"goals": {'goal': goal, 'progress': progress}}
            else:
                update = {"goals": {'goal': goal}}
        else:
            update = {"goals": {"progress": progress}}
        
        ref.update(update)

        return "Success", 200
    
    except Exception as e:
        ret = 'Failed with error: ' + str(e)
        return ret, 400

#suggestions (get the product, get the data from sentiment)


if __name__ == '__main__':
    app.run()
