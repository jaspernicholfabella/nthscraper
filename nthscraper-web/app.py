import yaml
from flask import Flask, render_template
from flask_apscheduler import APScheduler

from utils import log_cpu_usage, log_ram_usage

with open("zsconfig.yml", "r") as file:
    zsconfig = yaml.safe_load(file)


scheduler = APScheduler()
app = Flask(__name__, template_folder="templates")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/other")
def other():
    return render_template("other.html")


if __name__ == "__main__":
    scheduler.add_job(func=log_cpu_usage, trigger="interval", seconds=5, id="cpujob")
    scheduler.add_job(func=log_ram_usage, trigger="interval", seconds=10, id="ramjob")
    scheduler.start()
    app.run(debug=False, host=zsconfig["web"]["host"], port=zsconfig["web"]["port"])
