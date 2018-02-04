from flask import Flask, render_template, flash, request, url_for, redirect, session, g
from content_management import Content

from flask_wtf import Form
from wtforms import TextField, BooleanField, validators, PasswordField, Form

from passlib.hash import sha256_crypt

from MySQLdb import escape_string as thwart

from dbconnect import connection
import gc






TOPIC_DICT = Content()

app = Flask(__name__)

# kept gett this error
# RuntimeError: The session is unavailable because no secret key was set.  Set the secret_key on the application to something unique and secret.
# So I googled this answer for making app.secret_key

app.secret_key = 'my unobvious secret key'


@app.route('/')
def homepage():
    return render_template('main.html')


@app.route('/dashboard/')
def dashboard():
    flash('flash test!!!')

    return render_template('dashboard.html', TOPIC_DICT=TOPIC_DICT)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


@app.errorhandler(405)
def method_not_found(e):
    return render_template('405.html')


@app.route('/about/')
def about():
    return (render_template('about.html'))


@app.route('/login/', methods=['GET', 'POST'])
def login_page():
    error = ''
    try:
        if request.method == 'POST':
            attempted_username = request.form['username']
            attempted_password = request.form['password']

            # flash(attempted_username)
            # flash(attempted_password)

            if attempted_username == 'admin' and attempted_password == 'password':
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid credentials. Try Again.'

        return render_template('login.html', error=error)


    except Exception as e:
        # flash(e)
        return render_template('login.html', error=error)


# Slash is only for testing

@app.route('/slashboard/')
def slashboard():
    try:
        return render_template('dashboard.html', TOPIC_DICT=shamwow)
    except Exception as e:
        return render_template('500.html', error=e)


class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=20)])
    email = TextField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField('New Password', [validators.Required(),
                                              validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the Terms of Service and Privacy Notice (updated Jan 22, 2015)',
                              [validators.Required()])


# @app.route('/register/', methods=['GET', 'POST'])
# def register():
#     try:
#         form = RegistrationForm(request.form)
#
#         if request.method == 'POST' and form.validate():
#             username = form.username.data
#             email = form.email.data
#             password = sha256_crypt.encrypt((str(form.password.data)))
#             c, conn = connection()
#
#             x=c.excecute('SELECT * FROM users WHERE username = (%s)'),
#             (thwart(username))
#             #video 16
#             if int(len(x)) > 0:
#                 flash("That username is already taken, please choose another")
#                 return render_template("register.html", form=form)
#             else:
#                 c.execute("INSERT INTO users (username, password, email, tracking) VALUES (%s, %s, %s, %s)",
#                     (thwart(username), thwart(password), thwart(email), thwart('/introduction-to-python-programming/')))
#
#                 conn.commit()
#
#                 flash('Thanks for registering!')
#
#                 c.close()
#                 conn.close()
#                 # garbage collection
#                 gc.collect()
#
#                 session['logged_in']=True
#                 session['username']=username
#
#                 return redirect(url_for('dashboard'))
#         return render_template('register.html',form=form)
#
#
#     except exception as e:
#         return (str(e))

@app.route('/register/', methods=["GET", "POST"])
def register_page():
    try:
        form = RegistrationForm(request.form)

        if request.method == "POST" and form.validate():
            username = form.username.data
            email = form.email.data
            password = sha256_crypt.encrypt((str(form.password.data)))
            c, conn = connection()

            x = c.execute("SELECT * FROM users WHERE username = (%s)",
                          (thwart(username)))

            if int(x) > 0:
                flash("That username is already taken, please choose another")
                return render_template('register.html', form=form)

            else:
                c.execute("INSERT INTO users (username, password, email, tracking) VALUES (%s, %s, %s, %s)",
                          (thwart(username), thwart(password), thwart(email),
                           thwart("/introduction-to-python-programming/")))

                conn.commit()
                flash("Thanks for registering!")
                c.close()
                conn.close()
                gc.collect()

                session['logged_in'] = True
                session['username'] = username

                return redirect(url_for('dashboard'))

        return render_template("register.html", form=form)

    except Exception as e:
        return (str(e))

# @app.route('/register/', methods=["GET", "POST"])
# def register_page():
#     try:
#         form = RegistrationForm(request.form)
#
#         if request.method == "POST" and form.validate():
#             username = form.username.data
#             email = form.email.data
#             password = sha256_crypt.encrypt((str(form.password.data)))
#             c, conn = connection()
#
#             x = c.execute("SELECT * FROM users WHERE username = (%s)",
#                           (thwart(username)))
#
#             if int(x) > 0:
#                 flash("That username is already taken, please choose another")
#                 return render_template('register.html', form=form)
#
#             else:
#                 c.execute("INSERT INTO users (username, password, email, tracking) VALUES (%s, %s, %s, %s)",
#                           (thwart(username), thwart(password), thwart(email),
#                            thwart("/introduction-to-python-programming/")))
#
#                 conn.commit()
#                 flash("Thanks for registering!")
#                 c.close()
#                 conn.close()
#                 gc.collect()
#
#                 session['logged_in'] = True
#                 session['username'] = username
#
#                 return redirect(url_for('dashboard'))
#
#         return render_template("register.html", form=form)
#
#     except Exception as e:
#         return (str(e))


if __name__ == '__main__':
    app.run(debug=True)
