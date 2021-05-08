# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from search import search_audio
from display_data import get_audio, get_transcript
from signup import create_user
from login import verify_user
from get_role import check_role
from get_status import check_status
from edit_email import change_email
from edit_password import change_password
from edit_name import change_name
from search_users import display_users
from search_records import display_records
from search_approved_records import display_approved_records
from block_unblock import edit_block
from decide_on_report import make_decision
from get_link import get_link
from edit_transcript_link import edit_t_link
from edit_audio_link import edit_a_link
from edit_metadata import edit_md
from add_file import create_file
from edit_role import set_role
from report import add_error
from metadata import edit_md
from privilege_search_users import privilege_display_users
import hashlib
import datetime
#from report import transcript_error

#create application object
app = Flask(__name__)
auth = HTTPBasicAuth()
#Flask-wtf requires encryption key
app.config['SECRET_KEY'] = 'g77MdJuwaAXaLJ20Lx1DRcs161nPSOZP'

#home page
@app.route('/')
def home():
    return render_template('index.html')

#allows user to login and go to their profile
@app.route('/user_profile') 
@auth.login_required
def u_profile():
    flash('Hello {}!'.format(auth.current_user()))
    return render_template('u_profile_page.html')

#allows admin to login and go to their profile
@app.route('/admin_profile') 
@auth.login_required
def a_profile():   
    flash('Hello {}!'.format(auth.current_user()))
    return render_template('a_profile_page.html')

#allows super admin to login and go to their profile
@app.route('/sadmin_profile')
@auth.login_required
def sa_profile():
    flash('Hello {}!'.format(auth.current_user()))
    return render_template('sa_profile_page.html')

#gets form for new email to edit to in db
@app.route('/edit_email_form', methods=['GET', 'POST'])
@auth.login_required
def e_email(): 
    return render_template('edit_email.html')

#edits email in db and return to profile
@app.route('/edit_email', methods=['GET', 'POST'])
@auth.login_required
def edit_email():
    email = request.form['new_email']
    change_email(email, auth.current_user())
    if check_role(auth.current_user()) == 'user':
        return render_template('u_profile_page.html')
    elif check_role(auth.current_user()) == 'admin':
        return render_template('a_profile_page.html')

#gets form for new password to edit to in db
@app.route('/edit_password_form', methods=['GET', 'POST'])
@auth.login_required
def e_password():
    return render_template('edit_password.html')
    
#edit password in db
@app.route('/edit_password', methods=['GET', 'POST'])
@auth.login_required
def edit_password():
    password = request.form['new_password']
    password = generate_password_hash(password)
    change_password(auth.current_user(), password)
    if check_role(auth.current_user()) == 'user':
        return render_template('u_profile_page.html')
    elif check_role(auth.current_user()) == 'admin':
        return render_template('a_profile_page.html')
    
#gets form for new username to edit to in db
@app.route('/edit_name_form', methods=['GET', 'POST'])
@auth.login_required
def e_name():
    return render_template('edit_name.html')
    
#edit name in db
@app.route('/edit_name', methods=['GET', 'POST'])
@auth.login_required
def edit_name():
    name = request.form['new_name']
    change_name(auth.current_user(), name)
    if check_role(auth.current_user()) == 'user':
        return render_template('u_profile_page.html')
    elif check_role(auth.current_user()) == 'admin':
        return render_template('a_profile_page.html')
        
#loads search form to get search terms for users like user email
@app.route('/search_users', methods=['GET', 'POST'])
@auth.login_required     
def search_users():
    return render_template('search_user.html')  
        
#searches db for users and displays them with button to block them    
@app.route('/view_users', methods=['GET', 'POST'])
@auth.login_required
def view_users():
    userquery = request.form['user']
    rows = display_users(userquery)
    u_emails = [rows[i][0] for i in range(0, len(rows))]
    size = len(rows)
    return render_template('user_results.html', rows=rows, size=size, u_emails=u_emails)
    
#blocks the selected user when button clicked  
@app.route('/block', methods=['GET', 'POST'])
@auth.login_required
def change_block_status():
    user = request.form['email']
    status = check_status(user)
    edit_block(user, status)
    return render_template('search_user.html')
    
#form to get terms to search reports by    
@app.route('/search_reports', methods=['GET', 'POST'])
@auth.login_required
def search_reports():
    return render_template('search_reports.html')
    
#displays reports from search and buttons to approve or disapprove/reject the report so it will/wont change its file in db, respectively    
@app.route('/view_reports', methods=['GET', 'POST'])
@auth.login_required
def view_reports():    
    r_type = request.form['report_type']
    order_by = request.form['order']
    rows = display_records(r_type, order_by)
    r_ids = [rows[i][0] for i in range(0, len(rows))]
    size = len(rows)
    return render_template('report_results.html', rows=rows, size=size, r_ids=r_ids)
    
#approve file change in db    
@app.route('/approve', methods=['GET', 'POST'])
@auth.login_required
def approve_report():
    report_num = request.form['pos_decision']
    decide_on(report_num, 'Approved')
    return render_template('search_reports.html')
    
#reject file change in db    
@app.route('/disapprove', methods=['GET', 'POST'])
@auth.login_required
def reject_report():
    report_num = request.form['neg_decision'] 
    decide_on(report_num, 'Disapproved') 
    return render_template('search_reports.html')  

#changes report status in db and return to search page
@app.route('/decide_on', methods=['GET', 'POST'])
@auth.login_required
def decide_on(report_num, decision):
    email = auth.current_user()
    make_decision(report_num, decision, email)
    return render_template('search_reports.html')

#form to search through only approved reports
@app.route('/search_approved')
@auth.login_required
def search_approved_reports():
    return render_template('search_approved_reports.html')

#sorts and displays approved reports from search & allow admin to edit the associated file
@app.route('/view_approved_reports', methods=['GET', 'POST'])
@auth.login_required
def view_approved_reports():
    r_type = request.form['report_type']
    order_by = request.form['order']
    rows = display_approved_records(r_type, order_by)
    r_ids = [rows[i][0] for i in range(0, len(rows))]
    size = len(rows)
    return render_template('approved_report_results.html', rows=rows, size=size, r_ids=r_ids)

#form to submit new info for file
@app.route('/edit_file_form', methods=['GET', 'POST'])
@auth.login_required
def edit_file_form():
    report_num = request.form['edit']
    t_link = get_link(report_num)
    return render_template('edit_file_form.html', report_num=report_num, t_link=t_link)

#edits trancript link of file in db
@app.route('/edit_t_link', methods=['GET', 'POST'])
@auth.login_required
def edit_transcript_link():
    report_num = request.form['t_link']
    new_t_link = request.form['new_t_link']
    edit_t_link(report_num, new_t_link)
    return render_template('edit_file_form.html', report_num=report_num)

#edits audio link of file in db
@app.route('/edit_a_link', methods=['GET', 'POST'])
@auth.login_required
def edit_audio_link():
    report_num = request.form['a_link']
    new_a_link = request.form['new_a_link']
    edit_a_link(report_num, new_a_link)
    return render_template('edit_file_form.html', report_num=report_num)
    
#get new metadata for file    
@app.route('/edit_metadata_form', methods=['GET', 'POST'])
@auth.login_required
def edit_metadata_form():
    md_type = request.form['md_change']
    report_num = request.form['r_num']
    return render_template('edit_metadata_form.html', report_num=report_num, md_type=md_type)
    
#edit metadata of file in db    
@app.route('/edit_metadata', methods=['GET', 'POST'])
@auth.login_required
def edit_metadata():
    md_type = request.form['md_type']
    report_num = request.form['r_num']
    new_info = request.form['new_info']
    edit_md(md_type, report_num, new_info)
    return render_template('edit_file_form.html', report_num=report_num)
    
#form gets info for the file to be added    
@app.route('/add_file_form', methods=['GET', 'POST'])
@auth.login_required
def add_file_form():
    ct = datetime.datetime.now()
    return render_template('add_file_form.html', ct=ct)
    
#adds new file to db    
@app.route('/add_file', methods=['GET', 'POST'])
@auth.login_required
def add_file():
    a_id = request.form['a_id']
    title = request.form['title']
    d_pub = request.form['d_pub']
    pub = request.form['pub']
    desc = request.form['desc']
    a_lang = request.form['a_lang']
    a_file = request.form['a_file']
    d_interview = request.form['d_interview']
    interviewer = request.form['inter']
    interviewee = request.form['intee']
    t_file = request.form['t_file']
    transcriber = request.form['transcriber']
    t_lang = request.form['t_lang']
    create_file(a_id, title, d_pub, pub, desc, a_lang, a_file, d_interview, interviewer, interviewee, t_file, transcriber, t_lang)
    curr_role = check_role(auth.current_user())
    if curr_role == 'admin':
        return render_template('a_profile_page.html')
    elif curr_role == 'sadmin':
        return render_template('sa_profile_page.html')
    else:
        return render_template('index.html')

#get terms to search users by    
@app.route('/edit_admin_status_search', methods=['GET', 'POST'])
@auth.login_required
def edit_admin_status_search():
    return render_template('privilege_search_user.html')  
 
#search through users and allow super admin to click button to change the role privilege of the user or admin    
@app.route('/edit_admin_status_view', methods=['GET', 'POST'])
@auth.login_required
def edit_admin_status_view():
    userquery = request.form['user']
    rows = privilege_display_users(userquery)
    u_emails = [rows[i][0] for i in range(0, len(rows))]
    size = len(rows)
    return render_template('privilege_user_results.html', rows=rows, size=size, u_emails=u_emails)
    
#edits the users role in db and returns to search    
@app.route('/edit_admin_status', methods=['GET', 'POST'])
@auth.login_required
def edit_admin_status():
    email = request.form['email']
    role = check_role(email)
    if role == 'user':
        set_role(email, 'admin')
    elif role == 'admin':
        set_role(email, 'user')
    else:
        flash('Error- cannot downgrade a system admin or a non-user')
    return render_template('privilege_search_user.html')

#get new user info from form
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('signup_page.html')
    
#add new user (role defaults to 'user') to db    
@app.route('/signup_submit', methods=['GET','POST'])
def new_user():
    email = request.form['email']
    name = request.form['name']
    password = request.form['password']
    password = generate_password_hash(password)
    create_user(email, name, password)
    flash('Thank you for signing up, ' + name + '!')
    return render_template('index.html')

#login user if they enter the right email and password and go to their profile    
@app.route('/login', methods=['GET', 'POST'])
@auth.login_required
def login_verification():
    #email = request.form['email']
    #password = request.form['password']
    #verify_password(email, password)
    if auth.current_user() is None:
        return render_template('index.html')
    else:
        curr_role = check_role(auth.current_user())
        if curr_role == 'user':
            return render_template('u_profile_page.html')
        elif curr_role == 'admin':
            return render_template('a_profile_page.html')
        elif curr_role == 'sadmin':
            return render_template('sa_profile_page.html')

#old logout method
#@app.route('/logout')
#@auth.login_required
#def logout():
#    flash('Goodbye {}, you have been logged out!'.format(auth.current_user()))
#    curr_user = verify_password('jefhirejfu84u44r4u8uru4', 'dheuhfhruhfeyyygryg5u4y5')
#    return render_template('index.html')

#checks that the entered email matches the encrypted password
@auth.verify_password
def verify_password(email, password):
    curr_user = verify_user(email, password)
    if curr_user is None:
        flash("Invalid login credentials, try again")
        return None
    else:
        return email

@app.route('/search')
def search():
    #filter search by keywords, interviewer, interviewee, race, city
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
@auth.login_required
#get user to file a report
def report():
    af_id = request.form['id']
    return render_template('report.html',af_id=af_id)
    
@app.route('/report_submit', methods=['GET','POST'])
def trans_report():
    af_id = request.form['id']
    err_desc = request.form['error_description'] 
    if err_desc:
        add_error(err_desc,af_id)#add report to database
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
@auth.login_required
#get user to request to add metadata
def metadata():
    af_id = request.form['id']
    types = ['name','age','city','date created']
    return render_template('metadata.html', af_id=af_id,types=types)
    
@app.route('/metadata_submit', methods=['GET','POST'])
def meta_report():
    af_id = request.form['id']
    err_desc = request.form['description']
    choice = request.form['types']#metadata type 
    if err_desc and choice:
        edit_md(err_desc, choice, af_id)#add report to database
        flash('Metadata request filed!')
        
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
        types = ['name','age','city','date created']
        return render_template('metadata.html',af_id=af_id,types=types)
    

if __name__ == '__main__':
    app.run(debug = True)
