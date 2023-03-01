from flask import Flask, render_template
import requests

app = Flask(__name__)

def get_weather_results(zip_code, api_key):
    api_url = https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API key}

@app.route("/")
@app.route("/home")
def index():
    return render_template("index.html")


@app.route("/homepage")
def homepage():
    return render_template("homepage.html")


if __name__ == '__main__':
    app.run(debug=True)
