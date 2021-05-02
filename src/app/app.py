#app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from search import search_audio
from display_data import get_audio, get_transcript
from signup import create_user
from login import verify_user
from get_role import check_role
from edit_email import change_email
from report import add_error
from metadata import edit_md
import hashlib
#from report import transcript_error

#create application object
app = Flask(__name__)
auth = HTTPBasicAuth()
#Flask-wtf requires encryption key
app.config['SECRET_KEY'] = 'g77MdJuwaAXaLJ20Lx1DRcs161nPSOZP'

#home route
@app.route('/')
def home():
    return render_template('index.html')
    
@app.route('/user_profile') 
@auth.login_required
def u_profile():
    return render_template('u_profile_page.html')
    
@app.route('/admin_profile') 
@auth.login_required
def a_profile():   
    return render_template('a_profile_page.html')
    
@app.route('/edit_email_form', methods=['GET', 'POST'])
def e_email(): 
    return render_template('edit_email.html')
    
@app.route('/edit_email', methods=['GET', 'POST'])
def edit_email():
    email = request.form['new_email']
    change_email(email)
    return render_template('u_profile_page.html')
    
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('signup_page.html')
    
@app.route('/signup_submit', methods=['GET','POST'])
def new_user():
    email = request.form['email']
    name = request.form['name']
    password = request.form['password']
    password = generate_password_hash(password)
    create_user(email, name, password)
    flash('Thank you for signing up, ' + name + '!')
    return render_template('index.html')
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login_page.html')
    
@app.route('/login_verify', methods=['GET', 'POST'])
def login_verification():
    email = request.form['email']
    password = request.form['password']
    curr_user = verify_password(email, password)
    if curr_user is None:
        return render_template('index.html')
        
    curr_role = check_role(email)
    if curr_role == 'user':
        return render_template('u_profile_page.html')
    #elif curr_role == 'admin':
    #elif curr_role == 'sadmin':
    return render_template('index.html')

@auth.verify_password
def verify_password(email, password):
    curr_user = verify_user(email, password)
    if curr_user is None:
        flash("Invalid login credentials, try again")
        return None
    return email

#search route
@app.route('/search', methods=['GET','POST'])
def search():
    #search options
    choices = ['Keywords','Interviewer','Interviewee', 'Race','City']
    return render_template('search_page.html',choices=choices)
    
#search resultss route
@app.route('/results', methods=['GET','POST'])    
def results():
    #display search results
    choice = request.form['choices']#user's search option
    query = request.form['query']#user's query
    rows = search_audio(choice, query)#database results
    af_ids = [rows[i][0] for i in range(0,len(rows))]
    size = len(rows)#number of tuples
    return render_template('results.html', rows=rows,size=size,af_ids=af_ids)
    
@app.route('/audio', methods=['GET','POST'])
#display audio info for one file
def audio_file():
    audio_data = request.form['id']
    a_file = get_audio(audio_data)
    af_id = a_file[0][0]#audio_file id
    title = a_file[0][5]#title of audio_file
    raw_audio = a_file[0][7]#link to raw audio
    transcript_data = get_transcript(a_file[0][0])#audio_file_id
    transcript = transcript_data[0][3]#link to transcript
    metadata = a_file[0][6]#description
    return render_template('audio-file.html', af_id = af_id, title=title,raw_audio=raw_audio,transcript=transcript,metadata=metadata)

   
@app.route('/report', methods=['GET','POST'])
#@auth.login_required
#get user to file a report
def report():
    af_id = request.form['id']
    return render_template('report.html',af_id=af_id)
    
@app.route('/report_submit', methods=['GET','POST'])
def trans_report():
    af_id = request.form['id']
    err_desc = request.form['error_descripton'] 
    if err_desc:
        add_error(err_desc)#add report to database
        flash('Report filed!')
        
        #retrieve audio data
        a_file = get_audio(af_id)
        title = a_file[0][5]#title of audio_file
        raw_audio = a_file[0][7]#link to raw audio
        transcript_data = get_transcript(a_file[0][0])#audio_file_id
        transcript = transcript_data[0][3]#link to transcript
        metadata = a_file[0][6]#description
        return render_template('audio-file.html', af_id = af_id, title=title,raw_audio=raw_audio,transcript=transcript,metadata=metadata)
        
    else:
        flash('Blank Description')
        return render_template('report.html',af_id=af_id)
        
@app.route('/metadata', methods=['GET','POST'])
#@auth.login_required
#get user to request to add metadata
def metadata():
    af_id = request.form['id']
    types = ['audio','transcript']
    return render_template('metadata.html',af_id=af_id,types=types)
    
#@app.route('/metadata_submit', methods=['GET','POST'])
#def meta_report():

if __name__ == '__main__':
    app.run(debug = True)
