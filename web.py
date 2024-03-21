from flask import Flask, render_template


app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("index.html")


app.run(host="10.2.24.16", port=5000, debug=True)
