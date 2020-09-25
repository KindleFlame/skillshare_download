import requests
import json
import os
import lib
import re

with open('cookie.json') as f:
    s = f.read()
    j = json.loads(s).popitem()[1].popitem()[1]
    headers = {i['name']: i['value'] for i in j}

class Course:

    def __init__(self, soup):
        self.soup = soup

    @property
    def name(self):

        return ''

    @property
    def lessons(self):

        return []


def clear(s):
    s = re.sub('[^A-Za-z0-9]', '_', s)
    s = re.sub('_+', '_', s)
    return s


class Main:
    def __init__(self, account_id, headers, basepath=''):
        self.account_id, self.headers = account_id, headers
        self.basepath = basepath

    def auth():
        pass

    def ffmpeg(self, m3u8_link, filename):
        s = f'ffmpeg -protocol_whitelist "file,http,https,tcp,tls" -i "{m3u8_link}" -bsf:a aac_adtstoasc -vcodec copy -c copy -crf 50 {filename}'
        os.system(s)

    def download_mp4(self, video_id, filename):
        link = f"https://edge.api.brightcove.com/playback/v1/accounts/{self.account_id}/videos/{video_id}"
        res = requests.get(link, headers=headers).json()
        m3u8_link = next(i['src'] for i in res['sources'])
        self.ffmpeg(m3u8_link, filename)

    def download_lessons(self, soup):
        course = Course(soup)

        dirname = os.path.join(self.basepath, clear(course.name))
        os.makedirs(dirname, exist_ok=True)

        for name, video_id in course.lessons:
            filename = os.path.join(dirname, clear(name) + '.mp4')
            self.download_mp4(video_id, filename)

    def download_courses(self, links):
        session = self.auth()

        for link in links:
            content = session.get(link)
            soup = lib.soup(content)
            self.download_lessons(soup)

video_id = '6080615332001'
video_dir = 'Cinema 4D Creating Procedured Ornament with no plugin'

video_dir = video_dir.replace(' ', '_')

account_id = '3695997568001'
link = f"https://edge.api.brightcove.com/playback/v1/accounts/{account_id}/videos/{video_id}"


res = requests.get(link, headers=headers).json()
files = [i['src'] for i in res['sources']]

os.mkdir(video_dir)
for i, file in enumerate(files):
    s = f'ffmpeg -protocol_whitelist "file,http,https,tcp,tls" -i "{file}" -bsf:a aac_adtstoasc -vcodec copy -c copy -crf 50 {video_dir}/file{i}.mp4'
    os.system(s)

