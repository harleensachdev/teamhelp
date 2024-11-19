from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)  # This creates the web app
app.secret_key = "your_secret_key"  # A secret key to keep data safe

# Mock user database
users = {}  # A dictionary to store users' info (like a list of accounts)

@app.route('/')
def index():
    return redirect(url_for('login'))  # Redirects to the login page when someone visits the home page

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':  # If the user is sending data (logging in)
        email = request.form['email']  # Get the email from the form
        password = request.form['password']  # Get the password from the form
        if email in users and users[email]['password'] == password:  # Check if the email and password match
            return redirect(url_for('home', display_name=users[email]['display_name']))  # Go to the home page
        else:
            flash('Invalid email or password', 'danger')  # Show an error message
    return render_template('login.html')  # Show the login page

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':  # If the user is creating an account
        email = request.form['email']  # Get the email from the form
        password = request.form['password']  # Get the password from the form
        display_name = request.form['display_name']  # Get the display name
        if email in users:  # Check if the email is already in use
            flash('Email already exists', 'danger')  # Show an error message
        else:
            users[email] = {'password': password, 'display_name': display_name}  # Save the user's info
            flash('Account created successfully', 'success')  # Show a success message
            return redirect(url_for('login'))  # Go back to the login page
    return render_template('signup.html')  # Show the signup page

@app.route('/home')
def home():
    display_name = request.args.get('display_name', 'User')  # Get the user's name, or use "User" if not provided
    return render_template('home.html', display_name=display_name)  # Show the home page with the user's name

if __name__ == '__main__':
    app.run(debug=True)  # Start the app in debug mode (so errors are easier to find)
