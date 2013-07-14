from flask import Flask
from flask.ext import restful
from flask.ext.restful import reqparse
import requests
from flask import Flask, Response, request
import xml.etree.ElementTree as ET
import urllib
import simplejson
import os
import md5
import time
import hashlib

app       = Flask(__name__)
api       = restful.Api(app)
TO        = os.environ.get('SENDGRID_TO')
FROM      = os.environ.get('SENDGRID_FROM')
SUBJECT   = os.environ.get('SENDGRID_SUBJECT')
API_USER  = os.environ.get('SENDGRID_USERNAME')
API_KEY   = os.environ.get('SENDGRID_PASSWORD')
ROVI_KEY  = os.environ.get('ROVI_KEY')
ROVI_SECRET = os.environ.get('ROVI_SECRET')

def get_rovi_meta_data(movie_name):
   timestamp = int(time.time())
   m = hashlib.md5()
   m.update(ROVI_KEY)
   m.update(ROVI_SECRET)
   m.update(str(timestamp))
   sig = m.hexdigest()
   payload = {
       'movie': movie_name, 
       'country': 'US', 
       'language': 'en', 
       'format': 'json', 
       'apikey': ROVI_KEY, 
       'sig': sig
   }
   r = requests.get("http://api.rovicorp.com/data/v1/movie/info", params=payload)
   return r.text

# Find the the official title and streaming link from HBO GO
def hbo_get_streaming_info(movie_name):
    url = "http://catalog.lv3.hbogo.com/apps/mediacatalog/rest/searchService/HBO/search?term=" + movie_name
    r = requests.get(url)
    root = ET.fromstring(r.text)
    movie_name = root.findtext("body/results/assetResponse/title", default="NA")
    T_key = root.findtext("body/results/assetResponse/TKey", default="NA")
    link = "http://www.hbogo.com/#search&browseMode=browseGrid?searchTerm=ted/video&assetID=" + T_key + "?videoMode=embeddedVideo?showSpecialFeatures=false" 
    return movie_name, link

# API request handler, hbo endpoint
class HBO(restful.Resource):
  def get(self):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help="Name cannot be blank!")
    args = parser.parse_args()
    movie_name = urllib.quote_plus(args['name'])
    response = hbo_get_streaming_info(movie_name)
    movie_name = response[0]
    url = response[1]
    if movie_name == "NA":
       return { "message": "error", "errors": [ "Movie not found"] }
    else:
       return {'title': movie_name, 'url': url }

api.add_resource(HBO, '/hbo')

@app.route("/")
def index():
  return "moviegrid" 

@app.route("/parse", methods=['GET', 'POST'])
def sendgrid_parser():
    if request.method == 'POST':
        """Required response to SendGrid.com's Parse API"""
        print "HTTP/1.1 200 OK"
        print

        envelope = simplejson.loads(request.form.get('envelope'))
        to_address = envelope['to'][0]
        from_address = envelope['from']
        movie_name = request.form.get('subject')
        response = hbo_get_streaming_info(movie_name)
        movie_name = response[0]
        url = response[1]
        r = get_rovi_meta_data(movie_name)
        body = "Movie Name: " + movie_name + "<br /><br />HBO GO Link: " + url + "<br /><br />" + r.text
        payload = {
            'to': from_address, 
            'from': FROM, 
            'subject': SUBJECT, 
            'text': body, 
            'html': body, 
            'api_user': API_USER, 
            'api_key': API_KEY 
        }
        r = requests.get("http://sendgrid.com/api/mail.send.json", params=payload)

        return "HTTP/1.1 200 OK"

if __name__ == "__main__":
  app.debug = True
  app.run()
