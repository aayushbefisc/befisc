from flask import Flask, render_template, request, redirect, url_for, session
# from flask_pymongo import PyMongo
from bson import ObjectId
import pymongo
import ssl

app = Flask(__name__)

connection_string = "mongodb+srv://aayush:27112000@logindata.pcxo2we.mongodb.net"
app.secret_key = 'your_secret_key'
mongo = pymongo.MongoClient(connection_string, ssl_cert_reqs=ssl.CERT_NONE)


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
    # user = mongo.db.users.find_one({'username': username, 'password': password})
    print(user)
    
    if user:
        # Store user information in session
        session['user_id'] = str(user['_id'])
        session['account_version'] = user['account_version']  # Set the session variable here
        
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
    if 'user_id' in session:
        user = mongo.db.users.find_one({'_id': ObjectId(session['user_id'])})
        return render_template('dashboard.html', user=user, account_version=session['account_version'])
    else:
        return redirect(url_for('login_page'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))

if __name__ == '__main__':
    app.run(debug=True)
