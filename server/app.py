#!/usr/bin/env python

import string
import random
import shelve
from subprocess import check_output
import flask
from flask import request, abort
from os import environ

app = flask.Flask(__name__)
app.debug = True

db = shelve.open("shorten.db")
meme_db = shelve.open("meme.db")
shortUrlDict={}
meme_id = 0;
###
# Home Resource:
# Only supports the GET method, returns a homepage represented as HTML
###
@app.route('/home', methods=['GET'])
def home():
    """Builds a template based on a GET request"""
    return flask.render_template(
            'index.html')

###
# Home Resource:
# Only supports the GET method, returns a homepage represented as HTML
###
@app.route('/about', methods=['GET'])
def about():
    """Builds a template based on a GET request"""
    return flask.render_template(
            'about.html')
    
###
# Shorts Resource:
# Only supports the POST method, returns the shortened URL for the entered long url
###
@app.route('/shorts', methods=['POST'])
def shorts():
    """Shortens the given url, and returns the association between the original and the shortened url"""
    #short_url= request.form["shortUrl"]
    long_url = request.form["longUrl"]
    short_url=request.form.get("shortUrl","empty!")
    urlDict = {v:k for k, v in db.items()}
    if(long_url in urlDict and short_url=="empty!"):
        short_url=urlDict[long_url]
        return short_url+"-old"
    elif(short_url != "empty!"):
        if isinstance(short_url, unicode):
            short_url = short_url.encode('utf-8')
        if(short_url in db):
            del db[short_url]
        db[short_url]=long_url
        return short_url+"-stored"
    elif(short_url == "empty!"):
        short_url="lui.gi/"+ id_generator()
        db[short_url]=long_url
        return short_url+"-new"

###
# Random character generator:
# Helper function to automatically spit out a short URL path"
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))
###
# Short Resource:
# Only supports the GET method, returns the shortened URL for the entered long url
###
@app.route('/short/<path:url>', methods=['GET'])
def short(url):
    """Redirects to the original url after looking up the association if it exists. Otherwise throws error"""
    if isinstance(url, unicode):
            url = url.encode('utf-8')
    try:
        longUrl=db[url]
    except KeyError:
        longUrl="error"
        
    if(longUrl=="error"):
        return flask.render_template('error.html'), 404
    else:
        return flask.redirect(longUrl)       


###
# Meme Generator
# Will save the Memes in the dictionary
###
@app.route('/saveMeme', methods=['POST'])
def saveMeme():
    id = "lui.gi/"+ id_generator()
    img = request.form['img'];
    topText = request.form['top']
    bottomText = request.form['bottom']
    meme = []
    meme.append(topText)
    meme.append(img)
    meme.append(bottomText)
    meme_db[id]=meme
    db[id]="http://people.ischool.berkeley.edu/~ramit/server/meme/"+id
    return id

@app.route('/meme')
def meme():
    return flask.render_template("meme.html")
   
@app.route('/meme/<path:url>', methods=["GET"])
def getMeme(url):
      """Redirects to the meme after looking up the association if it exists. Otherwise throws error"""
      if isinstance(url, unicode):
          url = url.encode('utf-8')
      try:
        meme=meme_db[url]
      except KeyError:
        meme="error"        
      if(meme=="error"):
        return flask.render_template('error.html'), 404       
      else:
        img = meme[1]
        top = meme[0]
        bottom = meme[2]
        return flask.render_template("memeTemplate.html",img=img, top=top, bottom=bottom)
    
if __name__ == "__main__":
    app.run(port=int(environ['FLASK_PORT']))
    
