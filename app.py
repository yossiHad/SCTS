from flask import Flask, render_template, request, redirect, url_for, send_file
import os

app = Flask(__name__)

# Hardcoded credentials for the demo
admin_credentials = {"admin": "adminpass"}
user_credentials = {"user": "userpass"}
stolen_credentials = [("admin2", "adminpass2")]

# Paths to the secret files
real_secret_path = os.path.join(os.getcwd(), "secret.txt")
fake_secret_path = os.path.join(os.getcwd(), "fake_secret.txt")

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if (username, password) in stolen_credentials:
            return redirect(url_for('fake_admin'))
        elif username in admin_credentials and admin_credentials[username] == password:
            return redirect(url_for('admin'))
        elif username in user_credentials and user_credentials[username] == password:
            return redirect(url_for('user'))
        else:
            return "Invalid credentials, please try again."
    return render_template('login.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/fake_admin')
def fake_admin():
    return render_template('fake_admin.html')

@app.route('/user')
def user():
    return render_template('user.html')

@app.route('/download_real_secret')
def download_real_secret():
    return send_file(real_secret_path, as_attachment=True)

@app.route('/download_fake_secret')
def download_fake_secret():
    return send_file(fake_secret_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
