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
  - sudo apt update
  - sudo apt install python3-pip
* install psycopg2
  - pip3 install psycopg2-binary
* install flask
  - pip3 install flask
* install HTTPAuth
  - pip3 install Flask-HTTPAuth

To run program, make sure you're in src folder and run the following command in your prompt: python3 run.py
This should create the database and populate the tables with data.

To startup server, make sure you're in the app folder and run the following command: export FLASK_APP=app.py flask run 
In your browser: go to 127.0.0.1:5000/ This link should take you to Trentaudio's home page. To stop server, hit Ctrl-C in your command prompt.

# How to Use
You can choose to login to access other features or just use the search feature without logging in.
  * To search the audio files, select the field you want to search by from the drop down menu, then type in the query you wish to search by. You may then select the date order you want the results to be sorted by on the results page.
  
## User:
  * You can search audio and edit your account information on your profile

## Administrator:
  * You can search audio, edit your account information, search & block/unblock users, add audio files to the database, and search reports made of records to approve/reject the changes or make changes to the audio file information
    - To block/unblock users, you must first search through users and then click the button to change their status. If they are blocked, this will unblock them. If they are unblocked, this will block them.
    - To edit an audio file's information, you must search through approved reports (via the search approved reports button) and then select the edit button. Note- only one field can be edited at a time.
    - To approve or reject a report, you must first search all reports (via the search reports button) and then select the approve or reject button, depending on what you want to do.

## Super Administrator:
  * This account can only be created in the PostgreSQL shell by editing the desired user's role to 'sadmin' via the command:
    - UPDATE USR SET ROLE = 'sadmin' WHERE USR_EMAIL = 'email of the user you want to make super admin';
  * You can do all that users and administrators can, but you can also upgrade the privilege of a user to an admin or downgrade the privilege of an admin to a user.
    - To change their privilege, you must first search the users and then click the button to change their role.

## Logout:
  * Due to current issues, to logout you must clear your web browser's cache and return to the home page at http://127.0.0.1:5000/ to login again.
