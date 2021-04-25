# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from search import search_audio

#create application object
app = Flask(__name__)
#Flask-wtf requires encryption key
app.config['SECRET_KEY'] = 'g77MdJuwaAXaLJ20Lx1DRcs161nPSOZP'
@app.route('/')

def home():
    choices = ['Keywords','Interviewer','Interviewee', 'Race','City']
    
    return render_template('index.html',choices=choices)
@app.route('/form-handler', methods=['POST'])    
def results():
    choice = request.form['choices']
    query = request.form['query']
    rows = search_audio(choice, query)
    return render_template('my-result.html', rows=rows)
    
if __name__ == '__main__':
    app.run(debug = True)
