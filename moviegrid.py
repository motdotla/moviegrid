from flask import Flask
from flask.ext import restful
from flask.ext.restful import reqparse
import requests
import xml.etree.ElementTree as ET
import urllib

app = Flask(__name__)
api = restful.Api(app)

class HBO(restful.Resource):
  def get(self):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help="Name cannot be blank!")
    args = parser.parse_args()
    url = "http://catalog.lv3.hbogo.com/apps/mediacatalog/rest/searchService/HBO/search?term=" + args['name']
    return url
    # r = requests.get(url)
    # root = ET.fromstring(r.text)
    # movie_name = root.findtext("body/results/promotionResponse/title", default="NA")
    # T_key = root.findtext("body/results/promotionResponse/TKey", default="NA")
    # link = "http://www.hbogo.com/#search&browseMode=browseGrid?searchTerm=ted/video&assetID=" + T_key + "?videoMode=embeddedVideo?showSpecialFeatures=false"
    # if movie_name == "NA":
    #    return { "message": "error", "errors": [ "Movie not found:" + url ] }
    # else:
    #    return {'title': movie_name, 'url': link }

api.add_resource(HBO, '/hbo')

@app.route("/")
def index():
  return "moviegrid"

@app.route("/parse")
def parse():
  return "parse"

if __name__ == "__main__":
  app.run()
