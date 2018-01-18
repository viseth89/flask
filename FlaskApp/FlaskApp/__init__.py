from flask import Flask, render_template, flash, request, url_for, redirect
from flask import Flask, render_template

from content_management import Content

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
    error = None
    try:
        if request.method == 'POST':
            attempted_username=request.form['username']
            attempted_password=request.form['password']

            #flash(attempted_username)
            #flash(attempted_password)

            if attempted_username == 'admin' and attempted_password == 'password':
                return redirect(url_for('dashboard'))
            else:
                error ='Invalid credentials. Try Again.'

        return render_template('login.html', error=error)


    except Exception as e:
        #flash(e)
        return render_template('login.html', error=error)

# Slash is only for testing

@app.route('/slashboard/')
def slashboard():
    try:
        return render_template('dashboard.html', TOPIC_DICT=shamwow)
    except Exception as e:
        return render_template('500.html', error=e)


if __name__ == '__main__':
    app.run(debug=True)
