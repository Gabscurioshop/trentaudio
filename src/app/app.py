# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from search import search_audio
from display_data import get_audio, get_transcript
#from report import transcript_error

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
    
    titles = [rows[i][5] for i in range(0,len(rows))]
    return render_template('my-result.html', rows=rows, titles=titles)
    
@app.route('/audio-file-handler',methods=['POST'])
def audio_file():
#display data for selected  audio file
    audio_data = request.form['titles']
    row = get_audio(audio_data)
    title = row[0][5]#title of audio_file
    raw_audio = row[0][7]#link to raw audio
    transcript_data = get_transcript(row[0][0])#audio_file_id
    transcript = transcript_data[0][3]#link to transcript
    metadata = row[0][6]#description
    return render_template('audio-file.html',title=title,raw_audio=raw_audio,transcript=transcript,metadata=metadata)
   
@app.route('/report-handler', methods=['POST'])
#get user to file a report
def report():
    #desc = request.form['error_description']
    #transcript_error(desc)
    return render_template('report.html')

if __name__ == '__main__':
    app.run(debug = True)
