from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

#set up flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
# This is telling our app.config that we will connect via mongo_uri
#mongo_uri is similar to a url 
# the actual uri is saying
## the exact connection is in port 27017 and the databse is called mars_app
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   #tells flask to return a template using an index.html
   #tells flask to use the "mars db"
   return render_template("index.html", mars=mars)

@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   #The "scraping" is the scraping.py you have on the root folder
   mars_data = scraping.scrape_all()
   #.update(query_parameter, data, options)
   mars.update({}, mars_data, upsert=True)
   return redirect('/', code=302)
if __name__ == "__main__":
    app.run()