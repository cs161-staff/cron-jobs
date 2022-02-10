# CS 161 Cron Jobs (Miscellaneous Internal Logistics Scripts)

This repository holds an assortment of scripts and cron jobs deployed as Google Cloud Functions and run locally to handle miscellaneous internal infrastructure-related tasks.


### Grading the Feedback Question (Google Cloud Function)
In `main.py`, there's a `grade_feedback` endpoint that's deployed as a Google Cloud Function in the `cs161-logistics` project (owned by `cs161-staff@berkeley.edu`). This pulls data from the [CS 161 Feedback Manager spreadsheet](https://docs.google.com/spreadsheets/d/1xFah6ga8Zzb8NZZZeIOFJI-JJQoZSRQfE1DGwmBvB6c/edit#gid=0), which defines a list of assignments as well as a Gradescope email/password. The spreadsheet contains an Apps-Script based cron job that hits the endpoint every ~5 minutes. The function grades the feedback question on the provided homework assignments, which enables students to see their assignments as "Graded" shortly after submitting.

### Scraping the Feedback Question (Local Script)
To scrape the feedback question, run `python scripts/scrape-feedback.py` locally (after creating a virtualenv using `python -m venv cron-jobs`, activating using `source cron-jobs/bin/activate`, and installing requirements using `pip install -r requirements.txt`). This will prompt you for a username + password, and then scrape the feedback question and dump results into a text file called `feedback.txt`