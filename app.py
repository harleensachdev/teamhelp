from flask import Flask, render_template, request, redirect, url_for, flash

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
            return redirect(url_for('home', display_name=users[email]['display_name']))
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

@app.route('/home')
def home():
    display_name = request.args.get('display_name', 'User')
    return render_template('home.html', display_name=display_name)

if __name__ == '__main__':
    app.run(debug=True)
