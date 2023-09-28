from flask import Flask, render_template, request, redirect, url_for, session
import requests
import json
from datetime import datetime, timedelta


app = Flask(__name__)


app.secret_key = 'your_secret_key'



@app.route('/')
def login_page():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    url = "https://fpti5rzdjiydcmpcrgdvwj6rei0qotot.lambda-url.ap-south-1.on.aws/"
    headers = {'authkey': '59ZETKREAH7W5KC'}
    body = {"username":username}

    response = requests.post(url, headers=headers, json=body)
    get_user = (response.text)
    # print(get_user)

    if username in get_user and password in get_user:
        global users
        users = (username, password)
    else:
        error = 'Invalid credentials. Please try again.'
        return render_template('login.html', error=error)    

    if users:
        session['expiration_time'] = (datetime.now() + timedelta(hours=4)).timestamp()
        return redirect(url_for('dashboard'))
    else:
        error = 'Invalid credentials. Please try again.'
        return render_template('login.html', error=error)


@app.route('/dashboard')
def dashboard():
    try:
        if users:
            if 'expiration_time' in session and session['expiration_time'] < datetime.now().timestamp():
            # Clear the session and log the user out
                session.clear()
                return redirect(url_for('login_page'))
            
            return render_template('dashboard.html', user=users)
        else:
            return redirect(url_for('login_page'))
    except Exception as e:
        return redirect(url_for('login_page'))
    

@app.route('/profile')
def profile():
    try:
        if users:
            if 'expiration_time' in session and session['expiration_time'] < datetime.now().timestamp():
            # Clear the session and log the user out
                session.clear()
                return redirect(url_for('login_page'))
            
            return render_template('profile.html', user=users)
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
    full_list = total_label()
    url = 'https://vokeqyi2yudiqhigtaz4v4suge0zgjzy.lambda-url.ap-south-1.on.aws/'
    headers = {"authkey": "59ZETKREAH7W5KC"}
    try:
        response = requests.post(url, headers=headers)
        if response.status_code == 200:
            json_response = response.json()
            global client_list
            client_list = json_response.get("list_of_clients", [])
            options = full_list
        else:
            print(f"Request failed with status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return render_template('drop.html', client_list=client_list, options=options)


@app.route('/insertall', methods=['GET', 'POST'])
def insertall():
    url = 'https://vokeqyi2yudiqhigtaz4v4suge0zgjzy.lambda-url.ap-south-1.on.aws/'
    headers = {"authkey": "59ZETKREAH7W5KC"}
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        json_response = response.json()
        global client_list
        client_list = json_response.get("list_of_clients", [])
    return render_template('dropall.html', client_list=client_list)


@app.route('/insertdata', methods=['GET', 'POST'])
def insert_all():
    global client_list
    name = request.args.get('option')
    count = request.form.get('text2')
    url = "https://2cybzlrltyxjaehucdkp36mfi40ofner.lambda-url.ap-south-1.on.aws/"
    headers = {"authkey":"59ZETKREAH7W5KC"}
    body = {"name": f"{name}","count":f"{count}"}
    response = requests.post(url, headers=headers, json=body)
    if response.status_code == 200:
        output = "All Services Inserted successfully"
        return render_template('dropall.html', output=output, client_list=client_list)
    else:
        output = "Invalid option selected"
        return render_template('dropall.html', output=output, client_list=client_list)




def merge_dicts(dict1, dict2):
    return {**dict1, **dict2}
    

@app.route('/findservice', methods=['GET', 'POST'])
def findservice():
    global search_term
    search_term = request.form.get('search-input')
    url = 'https://g5p2ohnssbwy7de4nl3l3choxm0ntths.lambda-url.ap-south-1.on.aws/'
    headers = {"authkey": "59ZETKREAH7W5KC"}
    body = {"name": f"{search_term}"}
    response = requests.post(url, headers=headers, json=body)

    display_text = '' 
    acc_type = ''
    if response.status_code == 200:
        data = response.json()

        global service_exist
        exist_list = data.get("list_of_services", [])
        service_exist = data.get('list_of_services', {})

        acc = service_exist.get('account_type')
        display_text = f'Client Name: {search_term}'
        acc_type = f'Account Type: {acc}'

        exist_list.pop('account_type')
        exist_list.pop('name')

        global label_values
        label_values = []
        for key, value in exist_list.items():
            if 'label' in value:
                label_value = value['label']
                label_values.append(label_value)

    return render_template('viewinsert.html', services=service_exist, display_text=display_text, acc_type=acc_type, merge_dicts=merge_dicts)



@app.route('/drop')
def drop():
    all = total_label()
    url = 'https://vokeqyi2yudiqhigtaz4v4suge0zgjzy.lambda-url.ap-south-1.on.aws/'
    headers = {"authkey": "59ZETKREAH7W5KC"}
    try:
        response = requests.post(url, headers=headers)
        if response.status_code == 200:
            json_response = response.json()
            services_list = json_response.get("list_of_services", [])
            client_list = json_response.get("list_of_clients", [])
        else:
            print(f"Request failed with status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")
    search_name = search_term

    set_service = set(all) #convert set
    set_exist = set(label_values) #convert set

    insert_service = set_service - set_exist #set difference
    insert_service = list(insert_service) 
    options = insert_service

    global selected_option
    selected_option = request.args.get('option')
    if selected_option is not None:
        select = total_select()
    count = request.args.get('text2')
    if selected_option:
        url = "https://si65y6hbdy4jtsnev3wxib7q6q0smtmo.lambda-url.ap-south-1.on.aws/"
        headers = {"authkey": "59ZETKREAH7W5KC"}
        body = {"name": f"{search_name}", "main_key": f"{select}", "count" : f"{count}", "purpose": "insert"}
        response = requests.post(url, headers=headers, json=body)
        if response.status_code == 200:
            if select in service_exist:
                output = f"{select}" + " is existing already."
                return render_template('drop.html', output=output)
            else:
                output = f"Insert for {select}" + "  executed successfully"
                return render_template('drop.html', output=output)
        else:
            output = "Invalid option selected"
            return render_template('drop.html', output=output)
    return render_template('drop.html', options=options, client_list=client_list)



@app.route('/update', methods=['GET', 'POST'])
def update():
    url = 'https://vokeqyi2yudiqhigtaz4v4suge0zgjzy.lambda-url.ap-south-1.on.aws/'
    headers = {"authkey": "59ZETKREAH7W5KC"}
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        json_response = response.json()
        client_list = json_response.get("list_of_clients", [])


    global search_name
    search_name = request.form.get('search-input')
    url = 'https://g5p2ohnssbwy7de4nl3l3choxm0ntths.lambda-url.ap-south-1.on.aws/'
    headers = {"authkey": "59ZETKREAH7W5KC"}
    body = {"name": f"{search_name}"}
    response = requests.post(url, headers=headers, json=body)
    if search_name == None:
        display_text = ''
    else:    
        display_text = f'Client Name: {search_name}'
 
    if response.status_code == 200:
        data = response.json()
        services = data.get('list_of_services', [])
        services = dict(services)

        keys_to_remove = list(services.keys())[:2]
        for key in keys_to_remove:
            services.pop(key)
        sorted_data = sorted(services.items(), key=lambda x: ord(x[1].get('page_id', '0')[0]))
        services = dict(sorted_data)

    if not services:
        services = None  
    return render_template('credits.html', services=services, client_list=client_list, display_text=display_text)


@app.route('/edit/<credit_type>', methods=['GET', 'POST'])
def edit_credit(credit_type):
    if request.method == 'POST':
        name = search_name
        new_amount = int(request.form['new_amount'])
        url = "https://si65y6hbdy4jtsnev3wxib7q6q0smtmo.lambda-url.ap-south-1.on.aws/"
        headers = {"authkey": "59ZETKREAH7W5KC"}
        body = {"name": f"{name}", "main_key": f"{credit_type}", "count" : f"{new_amount}", "purpose": "update"}
        response = requests.post(url, headers=headers, json=body)
        if response.status_code == 200:
            output = 'Edited Successfully'
            return render_template('credits.html',output=output)
    else:
        return render_template('edit_credit.html', credit_type=credit_type)
    
 
@app.route('/process', methods=['POST'])
def process():
    global selected_cards
    selected_cards = request.json.get('selected_cards', [])     
    return selected_cards


@app.route('/edit_all', methods=['GET', 'POST'])
def edit_all():
    for card in selected_cards:
        if request.method == 'POST':
            name = search_name
            new_amount = int(request.form['new_amount'])
            url = "https://si65y6hbdy4jtsnev3wxib7q6q0smtmo.lambda-url.ap-south-1.on.aws/"
            headers = {"authkey": "59ZETKREAH7W5KC"}
            body = {"name": f"{name}", "main_key": f"{card}", "count" : f"{new_amount}", "purpose": "update"}
            response = requests.post(url, headers=headers, json=body)
            if response.status_code != 200:
                return redirect('/update')
        else:
            return render_template('edit_all.html', credit_type=card) 
    return redirect('/update')     

def total_label():
    url = "https://g5p2ohnssbwy7de4nl3l3choxm0ntths.lambda-url.ap-south-1.on.aws/"
    payload = json.dumps({"name": "befisc_test"})
    headers = {'authkey': '59ZETKREAH7W5KC','Content-Type': 'application/json'}
    response = requests.request("POST", url, headers=headers, data=payload)
    json_response = response.json()
    services_list = json_response.get("list_of_services", [])
    services_list.pop('account_type')
    services_list.pop('name')
    label_values = []
    for key, value in services_list.items():
        if 'label' in value:
            label_value = value['label']
            label_values.append(label_value)
    return label_values


def total_select():
    url = "https://g5p2ohnssbwy7de4nl3l3choxm0ntths.lambda-url.ap-south-1.on.aws/"
    payload = json.dumps({"name": "befisc_test"})
    headers = {'authkey': '59ZETKREAH7W5KC','Content-Type': 'application/json'}
    response = requests.request("POST", url, headers=headers, data=payload)
    json_response = response.json()
    services_list = json_response.get("list_of_services", [])
    print(type(services_list))
    services_list.pop('account_type')
    services_list.pop('name')

    global selected
    for key, value in services_list.items():
        if 'label' in value and value['label'] == selected_option:
            selected = key
            break
    return selected    


if __name__ == '__main__':
    app.run(debug=True)
