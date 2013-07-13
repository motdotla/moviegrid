from flask import Flask
app = Flask(__name__)

@app.route("/")
def index():
  return "moviegrid"

@app.route("/parse")
def parse():
  return "parse"

if __name__ == "__main__":
  app.run()
