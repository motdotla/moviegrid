from flask import Flask
from flask.ext import restful

app = Flask(__name__)
api = restful.Api(app)

class HBO(restful.Resource):
  def get(self):
    return {'hello': 'world'}

api.add_resource(HBO, '/hbo')

@app.route("/")
def index():
  return "moviegrid"

@app.route("/parse")
def parse():
  return "parse"

if __name__ == "__main__":
  app.run()
