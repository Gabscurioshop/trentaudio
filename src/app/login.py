'''
app.secret_key = "My precious"

#login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first')
            return redirect(url_for('login'))
    return wrap

#use decorators to link functino to url
@app.route("/")
@login_required
def home():
    return render_template('index.html') #render template

@app.route('/welcome')
def welcome():
    return render_template('welcome.html') #render template
 

#handle login requests
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid credentials. Please try again.'
        else:
            session['logged_in'] =True
            flash('You were just logged in!')
            return redirect(url_for('home'))
    return render_template('login.html', error = error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were just logged out!')
    return redirect(url_for('welcome'))
'''
