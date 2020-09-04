from jinja2 import Environment,FileSystemLoader
import requests
import HexToWeights
import my_spotify_client
import os
import sys
import webbrowser
import json
from werkzeug.utils import secure_filename
from flask import Flask,render_template,request,redirect,url_for

client_id ='30d402e9b7a8414d82da0ffe3135c610'
client_secret = 'cd255070e8614c53aa0529156bf1d8b0'

#ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def index():
    return render_template('InputPage.html')

@app.route('/upload',methods=['POST'])
#Post when u want to send data to the server, GET is when you want to get data from server 
def upload():
    OutputArr = []
    #joins the directory folder with the images folder
    target = os.path.join(APP_ROOT,'static/')
    if not os.path.isdir(target):
        os.mkdir(target)

    ###########      SAVE IMAGES TO FOLDER FEATURE#############
    #loops through the various images, we allow multiple images to be taken in
    for myImage in request.files.getlist("UserImage"):
        filename = myImage.filename
        #Connects the file name to the images folder
        destination = "/".join([target,filename])
        #Adds the file into the images folder
        myImage.save(destination)
        processDestination = "/".join([destination,filename])
        print(destination)
        OutputArr = processRequest(destination)
    #################################################################
    #path = "static" #path for images
    #dirs = os.listdir(path) #go in directory
    print(OutputArr)
    #Renders the html page, each parameter fits in Jinja2 syntax
    return render_template("index.html",song_title = OutputArr[0],song_artist = OutputArr[1],image_name=filename)

#def jsonParser(jsonFile):
 #   parseFile = json.loads(jsonFile)
    #We don't actually need to do this
def processRequest(Image):
    InfoArr = []
    #Passes the image through for processing
    passImage = my_spotify_client.getImageProperly(Image)
    #Creates Spotify Obj
    mySpotifyObj = my_spotify_client.createSpotifyObj(client_id,client_secret)
    #Get's the Images weight
    getWeightImage = my_spotify_client.getWeight(passImage)
    #Creates the jsonFile 
    my_spotify_client.createJson(mySpotifyObj,getWeightImage)
    #Parses the info of the jsonFile
    #jsonParser(songInfo)
    with open("json_output.txt",'r') as fin:
        parseThrough = json.loads(fin.read())
        songParse = parseThrough["name"]
        artistParse = parseThrough["album"]["artists"][0]["name"]
        
        InfoArr.append(songParse)
        InfoArr.append(artistParse)

    return InfoArr
"""
#We have the userImage from the submission
    #userImage = request.files['UserImage'] 
    #Passes the image through for processing
    passImage = my_spotify_client.getImageProperly(userImage)
    #Creates Spotify Obj
    mySpotifyObj = my_spotify_client.createSpotifyObj(client_id,client_secret)
    #Get's the Images weight
    getWeightImage = my_spotify_client.getWeight(passImage)
    #Creates the jsonFile 
    songInfo = my_spotify_client.createJson(mySpotifyObj,getWeightImage)
    #Parses the info of the jsonFile
    #jsonParser(songInfo)
    parseThrough = json.loads(songInfo)

    return render_template('index.html')
    """
