from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo as pym
import scraping_mars

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mars_app'
mongo = pym(app)

@app.route('/')
def index():
    mars = mongo.db.mars.find_one()
    return render_template('index.html', mars=mars)

# @app.route("/")
# def index():
#     mars_hemispheres_dict = mars_hemispheres_dict
#     return render_template("index.html", dict=mars_hemispheres_dict)

@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping_mars.scrape_data()
   mars.update_one({}, {"$set":mars_data}, upsert=True)
   return redirect('/', code=302)

if __name__ == '__main__':
    app.run(debug=True)