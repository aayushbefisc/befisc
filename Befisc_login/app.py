from flask import Flask, render_template, request, redirect, url_for, session
import requests
import json
from bson import ObjectId
import pymongo
from datetime import datetime, timedelta



app = Flask(__name__)

connection_string = "mongodb+srv://aayush:27112000@logindata.pcxo2we.mongodb.net/?retryWrites=true&w=majority"
app.secret_key = 'your_secret_key'

mongo = pymongo.MongoClient(connection_string)


@app.route('/')
def login_page():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    account_version = request.form.get('account_version')

    db = mongo.get_database("mydatabase")
    collection = db.get_collection("users")

    # Check if the username and password exist in the database
    query = {'username': username, 'password': password}
    user = collection.find_one(query)
    
    if user:
        # Set the session variables with user information
        session['user_id'] = str(user['_id'])
        session['account_version'] = user['account_version']

        # Set the session expiration time as a timestamp (in seconds)
        session['expiration_time'] = (datetime.now() + timedelta(hours=4)).timestamp()

        # Check if the selected account version matches the one in the session
        if session['account_version'] == account_version:
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid account version. Please select the correct account version.'
            return render_template('login.html', error=error)
    else:
        error = 'Invalid credentials. Please try again.'
        return render_template('login.html', error=error)


@app.route('/dashboard')
def dashboard():
    db = mongo.get_database("mydatabase")
    collection = db.get_collection("users")
    query = {'_id': ObjectId(session['user_id'])}
    users = collection.find_one(query)

    if users:
        # Check if the session has expired
        if 'expiration_time' in session and session['expiration_time'] < datetime.now().timestamp():
            # Clear the session and log the user out
            session.clear()
            return redirect(url_for('login_page'))
    
        return render_template('dashboard.html', user=users, account_version=session['account_version'])
    else:
        return redirect(url_for('login_page'))
    


@app.route('/profile')
def profile():
    try:
        db = mongo.get_database("mydatabase")
        collection = db.get_collection("users")
        query = {'_id': ObjectId(session['user_id'])}
        users = collection.find_one(query)


        if users:
            if 'expiration_time' in session and session['expiration_time'] < datetime.now().timestamp():
            # Clear the session and log the user out
                session.clear()
                return redirect(url_for('login_page'))
            
            return render_template('profile.html', user=users, account_version=session['account_version'])
        else:
            return redirect(url_for('login_page'))
    except:
        return 'Login Again and check!!!'    
    

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))



@app.route('/insert', methods=['GET', 'POST'])
def insert():
    return redirect(url_for('drop'))


# @app.route('/inbusiness', methods=['GET', 'POST'])
def business():
    url = "https://jyxatg7xrbep4piyupe5fk5a6u0kcvpk.lambda-url.ap-south-1.on.aws/"
    headers = {"authkey": "asdfqwerty"}
    body = {"authkey": "asdfqwerty", "main_key": "business_pan", "page_id": "5", "count": "1", "label": "Mobile Lookup Basic", "purpose": "insert"}
    response = requests.post(url, headers=headers, json=body)
    if response.status_code == 200:
        output = "Insert for business_pan executed successfully"
        return render_template('result.html', output=output)
    else:
        output = "Invalid option selected"
        return render_template('result.html', output=output)
    
# @app.route('/ifscmain', methods=['GET', 'POST'])
def ifsc():
    url = "https://jyxatg7xrbep4piyupe5fk5a6u0kcvpk.lambda-url.ap-south-1.on.aws/"
    headers = {"authkey": "asdfqwerty"}
    body = {"authkey": "asdfqwerty", "main_key": "ifsc_main", "page_id": "4", "count": "2", "label": "Mobile Lookup Basic", "purpose": "insert"}
    response = requests.post(url, headers=headers, json=body)
    if response.status_code == 200:
        output = "Insert for ifsc_main executed successfully"
        return render_template('result.html', output=output)
    else:
        output = "Invalid option selected"
        return render_template('result.html', output=output)
    

@app.route('/drop')
def drop():
    options = ["Business_pan", "Ifsc_main", "Upi_basic","upi_main"]
    
    selected_option = request.args.get('option')
    print(selected_option)
    if selected_option == 'Business_pan':
        result = business()
        return result
    if selected_option == 'Ifsc_main':
        result = ifsc()
        return result
    if selected_option == 'Upi_basic':
        # result = upi_basic()
        return result
    return render_template('drop.html', options=options)


@app.route('/update', methods=['GET', 'POST'])
def update():
    db = mongo.get_database("mydatabase")
    collection = db.get_collection("users")
    query = {'_id': ObjectId(session['user_id'])}
    services = collection.find_one(query)
    
    return render_template('credits.html', services=services)


@app.route('/edit/<credit_type>', methods=['GET', 'POST'])
def edit_credit(credit_type):
    db = mongo.get_database("mydatabase") 
    collection = db.get_collection("users")
    query = {'_id': ObjectId(session['user_id'])}
    service = collection.find_one(query)

    if request.method == 'POST':
        credit_field = f"{credit_type}.count"
        new_amount = float(request.form['new_amount'])
        update = {"$set": {credit_field: new_amount}}
        collection.update_one(query, update=update)
        return redirect('/update')
    
    return render_template('edit_credit.html', service=service, credit_type=credit_type)


if __name__ == '__main__':
    app.run(debug=True)