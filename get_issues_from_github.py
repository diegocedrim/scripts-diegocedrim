import csv
import requests
from requests.auth import HTTPBasicAuth
import os.path
import json


auth = HTTPBasicAuth('diegocedrim', 'cfd35f4b08269fcc99b9e4ef3945d73a6800a535')
headers = {'Accept': 'application/vnd.github.mockingbird-preview'}


def get_issue_file(row):
    project_name = row["project"].replace("/", "_")
    template = "issues/%s_%s.json" % (project_name, row["issue_id"])
    return template


def get_timeline_issue_file(row):
    project_name = row["project"].replace("/", "_")
    template = "issues/%s_%s_timeline.json" % (project_name, row["issue_id"])
    return template


def already_downloaded(row):
    fname = get_issue_file(row)
    return os.path.isfile(fname)


def already_downloaded_timeline(row):
    fname = get_timeline_issue_file(row)
    return os.path.isfile(fname)


def download_issue(row):
    if already_downloaded(row):
        return
    fname = get_issue_file(row)
    with open(fname, "w") as out:
        response = requests.get(row["issue_url"], auth = auth)
        if response.status_code != 200:
            print "Problem with ref_id = %s. Status: %s" % (row["ref_id"], response.status_code)
            #raise BaseException("Error on " + str(row) + " " + str(response.status_code))
        else:
            jsonResult = response.json()
            out.write(json.dumps(jsonResult, sort_keys=True, indent=4))
    if os.path.isfile(fname) and response.status_code != 200:
        os.remove(fname)


def download_timeline_issue(row):
    if already_downloaded_timeline(row):
        return
    fname = get_timeline_issue_file(row)
    with open(fname, "w") as out:
        response = requests.get(row["issue_url"] + "/timeline", auth = auth, headers=headers)
        if response.status_code != 200:
            print "Problem with ref_id = %s. Status: %s" % (row["ref_id"], response.status_code)
            # raise BaseException("Error on " + str(row) + " " + str(response.status_code))
        else:
            jsonResult = response.json()
            out.write(json.dumps(jsonResult, indent=4))
    if os.path.isfile(fname) and response.status_code != 200:
        os.remove(fname)


with open('data/refactorings_and_issues_complete.csv') as input:
    reader = csv.DictReader(input, delimiter=';', quotechar='"')
    i = 1
    for row in reader:
        print "Downloading row %s" % i
        i += 1
        download_issue(row)
        download_timeline_issue(row)
        # if i == 2:
        #     exit()