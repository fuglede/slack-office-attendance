import datetime
import json
import sys
from urllib import request
import urllib.parse


def post(url, data):
    data = urllib.parse.urlencode(data).encode("utf-8")
    req = request.Request(
        url,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data=data,
        method="POST",
    )
    resp = request.urlopen(req)
    return json.loads(resp.read().decode(resp.headers.get_content_charset()))


def send_message(message, token, channel):
    # Send the message, then add two reactions to make it easier for users to
    # add their own.
    data = {"channel": channel, "text": message, "token": token}
    res = post("https://slack.com/api/chat.postMessage", data=data)

    ts = res["ts"]
    data = {"channel": channel, "name": "house", "token": token, "timestamp": ts}
    post("https://slack.com/api/reactions.add", data=data)

    data = {"channel": channel, "name": "office", "token": token, "timestamp": ts}
    post("https://slack.com/api/reactions.add", data=data)


def next_workday():
    # Mon-Thu produces the following day, but Fri should produce Mon.
    now = datetime.date.today()
    if now.weekday() > 4:
        return RuntimeError("script should only be called Mon-Fri")
    return now + datetime.timedelta(days=1 if now.weekday() < 4 else 3)


def main():
    _, token, channel = sys.argv
    day = next_workday()
    message = day.strftime("%A %B %-d") + ", office seatings"
    send_message(message, token, channel)


if __name__ == "__main__":
    main()
