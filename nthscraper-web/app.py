import yaml
import traceback
from flask import Flask, render_template, jsonify
from flask_apscheduler import APScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_MISSED, EVENT_JOB_EXECUTED

with open("settings.yml", "r") as file:
    nthsettings = yaml.safe_load(file)

with open("jobs.yml", "r") as file:
    nthjobs = yaml.safe_load(file)


app = Flask(__name__, template_folder="templates")

# List to store job errors
job_errors = []


class Config:
    """App Configuration."""

    SCHEDULER_JOBSTORES = {
        "default": SQLAlchemyJobStore(url=nthsettings["scheduler"]["db"])
    }

    SCHEDULER_EXECUTORS = {
        "default": {
            "type": nthsettings["scheduler"]["type"],
            "max_workers": nthsettings["scheduler"]["max_workers"],
        }
    }

    SCHEDULER_JOB_DEFAULTS = {
        "coalesce": nthsettings["scheduler"]["coalesce"],
        "max_instances": nthsettings["scheduler"]["max_instances"],
    }

    SCHEDULER_API_ENABLED = nthsettings["scheduler"]["api_enabled"]


@app.route("/")
def index():
    """The home route of our application"""
    return render_template("index.html")


@app.route("/other")
def other():
    """the other route of our application"""
    return render_template("other.html")


@app.route("/scheduler/errors")
def get_scheduler_errors():
    """convert error list into json list"""
    return jsonify(job_errors)


def job_listener(event):
    """
    listen to jobs to identifier job with errors or missed jobs
    """
    if event.exception:
        error_info = {
            "job_id": event.job_id,
            "exception": str(event.exception),
            "traceback": "".join(
                traceback.format_exception(
                    None, event.exception, event.exception.__traceback__
                )
            ),
        }
        job_errors.append(error_info)


def add_jobs(scheduler):
    # Get existing jobs from the job store
    existing_jobs = {job.id for job in scheduler.get_jobs()}
    for ik, iv in nthjobs["jobs"].items():
        # job_config.update(iv)
        if ik not in existing_jobs:
            scheduler.add_job(id=ik, replace_existing=True, **iv)


if __name__ == "__main__":
    app.config.from_object(Config())

    scheduler = APScheduler()
    scheduler.init_app(app)

    scheduler.add_listener(
        job_listener, EVENT_JOB_ERROR | EVENT_JOB_MISSED | EVENT_JOB_EXECUTED
    )

    with app.app_context():
        add_jobs(scheduler)

    scheduler.start()
    app.run(
        debug=False, host=nthsettings["web"]["host"], port=nthsettings["web"]["port"]
    )
