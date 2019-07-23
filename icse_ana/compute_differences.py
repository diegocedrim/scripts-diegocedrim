import json, csv
from datetime import datetime
import re

# print datetime.strptime('2011-08-15 21:52:54', '%Y-%m-%d %H:%M:%S')
# exit()

def average_difference(numbers):
    diffs = []
    for i in range(1, len(numbers)):
        if (numbers[i] - numbers[i - 1]) < 0:
            raise BaseException("lista desordenada " + str(numbers))
        diffs.append(numbers[i] - numbers[i - 1])
    return float(sum(diffs))/len(diffs)


def to_unixtimestamp(datestr):
    dateobj = datetime.strptime(datestr, '%Y-%m-%d %H:%M:%S')
    return (dateobj - datetime(1970, 1, 1)).total_seconds()


def time_human(seconds):
    result = None
    current_interval = float(seconds)
    divisors = [1, 60, 60, 24, 30, 12]
    texts_plural = ["seconds", "minutes", "hours", "days", "months", "years"]
    texts_singular = ["second", "minute", "hour", "day", "month", "year"]
    for divisor, plural, singular in zip(divisors, texts_plural, texts_singular):
        if current_interval >= divisor:
            current_interval /= divisor
            if int(current_interval) > 1:
                result = "%.1f %s" % (current_interval, plural)
            else:
                result = "%.1f %s" % (current_interval, singular)
        else:
            break
    return result


with open("batches_per_elements.json") as f, open("differences.csv", "w") as out:
    header = ["project", "element", "avg_commits", "avg_seconds", "avg_human_time", "batches_count", "same_developer"]
    writer = csv.DictWriter(out, fieldnames=header, delimiter=",")
    writer.writeheader()
    data = json.loads(f.read())
    for row in data:
        commits = map(lambda x: x["order"], row["batches"])
        dates = sorted(map(lambda x: to_unixtimestamp(x["start_date_utc"]), row["batches"]))
        row["avg_commits"] = average_difference(commits)
        row["avg_seconds"] = average_difference(dates)
        row["avg_human_time"] = time_human(row["avg_seconds"])
        row["batches_count"] = len(row["batches"])
        row["same_developer"] = True if len(set(map(lambda x: x["author"], row["batches"]))) == 1 else False
        del row["batches"]
        writer.writerow(row)
        # break
