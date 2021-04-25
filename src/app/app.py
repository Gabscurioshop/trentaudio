# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from search import search_audio
from display_data import display

#create application object
app = Flask(__name__)
#Flask-wtf requires encryption key
app.config['SECRET_KEY'] = 'g77MdJuwaAXaLJ20Lx1DRcs161nPSOZP'
@app.route('/')

def home():
    #filter search by keywords, interviewer, interviewee, race, city
    choices = ['Keywords','Interviewer','Interviewee', 'Race','City']
    
    return render_template('index.html',choices=choices)
@app.route('/form-handler', methods=['GET','POST'])    
def results():
    #display search results
    choice = request.form['choices']#type of search
    query = request.form['query']#read user input
    rows = search_audio(choice, query)#get database results
    audio_ids = [rows[i][0] for i in range(0,len(rows))]
    return render_template('my-result.html', rows=rows, audio_ids=audio_ids)
    
@app.route('/audio-file-handler',methods=['POST'])
def audio_file():
#display data for selected  audio file
    audio_data = request.form['audio_ids']
    row = display(audio_data)
    return render_template('audio-file.html',row=row)
'''    
@app.route('/report-handler')
#get user to file a report
def report():
    return render_template('report.html')
'''

if __name__ == '__main__':
    app.run(debug = True)
