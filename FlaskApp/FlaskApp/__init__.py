from flask import Flask, render_template, flash

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
    flash('flash test!!!')
    flash('flash test!!!')
    return render_template('dashboard.html', TOPIC_DICT = TOPIC_DICT)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

#Slash is only for testing
@app.route('/slashboard/')
def slashboard():
    try:
        return render_template('dashboard.html', TOPIC_DICT = shamwow)
    except Exception as e:
        return render_template('500.html', error=e)

if __name__ == "__main__":
    app.run()
