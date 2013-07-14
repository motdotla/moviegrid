from flask import Flask
from flask.ext import restful
import requests
import xml.etree.ElementTree as ET

app = Flask(__name__)
api = restful.Api(app)

class HBO(restful.Resource):
  def get(self):
    movie_name = "ted"
    r = requests.get("http://catalog.lv3.hbogo.com/apps/mediacatalog/rest/searchService/HBO/search?term=" + movie_name)
    root = ET.fromstring(r.text)
	result = root.findall(".//title")
    return result

api.add_resource(HBO, '/hbo')

@app.route("/")
def index():
  return "moviegrid"

@app.route("/parse")
def parse():
  return "parse"

if __name__ == "__main__":
  app.run()
