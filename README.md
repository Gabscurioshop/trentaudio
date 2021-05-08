# Trentaudio
Welcome to Trentaudio!
A project by Carolyne Holmes, Gabrielle Curcio, Xuanyi Zhao

# Problem Statement
Currently, the audio and visual content on the [Trentoniana Library](https://trentonlib.org/trentoniana/audio-visual/) provides limited metadata and no transcriptions on certain content. Our project aims at expanding the versatility of the Trentonian Library and making it a better tool for research. 

# Objectives
* Create a clearer user interface that allows for better access to the data
* Create a database system that handles audio-based data
* Link audio files to their corresponding transcripts
* Allow upper-level users to submit possible meta-data for files (such as topics addressed in the file) or issues/errors found with the file
* Allow casual-level users (such as people not logged on) to view transcripts and listen to audio files (presented on the same page)
* Allow an administrator to edit meta-data or add/delete/edit files

# How To Contribute
* View any issues in the issues tab
* Clone this repo and push changes to your branch

# Setup
Before running this program, make sure you have Python3, Psycopg2, and PostgreSQL installed
* install pip for Python 3
** sudo apt update
** sudo apt install python3-pip
* install psycopg2
** pip3 install psycopg2-binary
* install flask
** pip3 install flask
* install HTTPAuth
** pip3 install Flask-HTTPAuth

To run program, make sure you're in src folder and run the following command in your prompt: python3 run.py
This should create the database and populate the tables with data.

To startup server, make sure you're in the app folder and run the following command: export FLASK_APP=app.py flask run 
In your browser: go to 127.0.0.1:5000/ This link should take you to Trentaudio's home page. To stop server, hit Ctrl-C in your command prompt.

