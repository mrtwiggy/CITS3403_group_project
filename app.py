from flask import Flask, render_template
import yaml

with open('config.yml', 'r') as file:
    yaml_options = yaml.safe_load(file)

app = Flask(__name__)

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/reviews")
def reviews():
    return render_template("reviews.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route("/explore")
def explore():
    return render_template("explore.html")

if __name__ == "__main__":
    app.run(debug= True, port= yaml_options["server_port"])