import glob
import json
import os.path


def issues():
    files = [i for i in glob.glob('issues/*.json') if "_timeline.json" not in i]
    for issue_file in files:
        f = open(issue_file)
        text = f.read()
        f.close()
        yield json.loads(text)


def get_timeline_issue_file(row):
    project_name = row["project"].replace("/", "_")
    template = "issues/%s_%s_timeline.json" % (project_name, row["issue_id"])
    return template


def was_reopened(tline):
    for event in tline:
        if event["event"] == "reopened":
            return True
    return False

def timeline(refactoring):
    fname = get_timeline_issue_file(refactoring)
    if not os.path.isfile(fname):
        return None
    f = open(fname)
    text = f.read()
    f.close()
    return json.loads(text)