from flask import Flask, render_template, request, redirect, url_for, flash
import time
import random
import string

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Mock user database
users = {}

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in users and users[email]['password'] == password:
            return redirect(url_for('home', display_name=users[email]['display_name'], email=email))
        else:
            flash('Invalid email or password', 'danger')
    return render_template('login.html')

@app.route('/ourgoals')
def help():
    return render_template('ourgoals.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        display_name = request.form['display_name']
        if email in users:
            flash('Email already exists', 'danger')
        else:
            users[email] = {'password': password, 'display_name': display_name}
            flash('Account created successfully', 'success')
            return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/home',methods=['POST','GET'])
def home():
    email = request.args.get('email')
    if request.method == 'POST':
        if email in users:
            random_part = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            timestamp = int(time.time())
            if 'groups' in users[email]:
                users[email]['groups'].append(f"{random_part}-{timestamp}")
            else:
                users[email]['groups'] = [f"{random_part}-{timestamp}"]
            return redirect(url_for('grouphome',email=email,group_code=users[email]['groups'][-1]))
        else:
            flash('User not found', 'danger')
    display_name = users[email]['display_name']
    if 'groups' in users[email]:
        return render_template('home.html', display_name=display_name, group=True, groups=users[email]['groups'], email=email)
    else:
        return render_template('home.html', display_name=display_name, group=False)

@app.route('/grouphome', methods=['GET', 'POST'])
def grouphome():
    email = request.args.get('email')
    group_code= request.args.get('group_code')
    if email in users and 'groups' in users[email]:
        return render_template('grouphome.html', group_code=group_code, email=email)
    else:
        flash('User not found or group not made','danger')
        return redirect(url_for('home',email=email))

if __name__ == '__main__':
    app.run(debug=True)
