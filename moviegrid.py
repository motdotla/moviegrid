from flask import Flask
from flask.ext import restful
from flask.ext.restful import reqparse
import requests
import xml.etree.ElementTree as ET
import urllib
import simplejson

app = Flask(__name__)
api = restful.Api(app)

class HBO(restful.Resource):
  def get(self):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help="Name cannot be blank!")
    args = parser.parse_args()
    movie_name = urllib.quote_plus(args['name'])
    url = "http://catalog.lv3.hbogo.com/apps/mediacatalog/rest/searchService/HBO/search?term=" + movie_name
    r = requests.get(url)
    root = ET.fromstring(r.text)
    movie_name = root.findtext("body/results/assetResponse/title", default="NA")
    T_key = root.findtext("body/results/assetResponse/TKey", default="NA")
    link = "http://www.hbogo.com/#search&browseMode=browseGrid?searchTerm=ted/video&assetID=" + T_key + "?videoMode=embeddedVideo?showSpecialFeatures=false"
    if movie_name == "NA":
       return { "message": "error", "errors": [ "Movie not found"] }
    else:
       return {'title': movie_name, 'url': link }

api.add_resource(HBO, '/hbo')

@app.route("/")
def index():
  return "moviegrid"

@app.route('/parse', methods=('GET', 'POST'))
def sendgrid_parser():
    if request.method == 'POST':
        """Required response to SendGrid.com's Parse API"""
        print "HTTP/1.1 200 OK"
        print

        envelope = simplejson.loads(request.form.get('envelope'))
        to_address = envelope['to'][0]
        from_address = envelope['from']
        text = request.form.get('text')
        subject = request.form.get('subject')
        num_attachments = int(request.form.get('attachments', 0))
        payload = {'to': from_address, 'from': 'hackers@SendGrid.com', 'subject': 'MovieGrid Results', 'text': from_address, 'html': from_address, 'api_user': config['sendgrid_api_user'], 'api_key': config['sendgrid_api_key']}
        r = requests.get("http://sendgrid.com/api/mail.send.json", params=payload)

        return "HTTP/1.1 200 OK"

if __name__ == "__main__":
  app.run()
