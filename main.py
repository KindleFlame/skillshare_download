import requests
import json
import os
import lib as fs
import re
import subprocess

with open('cookie.json') as f:
    s_ = f.read()
    j_ = json.loads(s_).popitem()[1].popitem()[1]
    main_headers = {i['name']: i['value'] for i in j_}


class Course:

    def __init__(self, soup):
        self.soup = soup

    @property
    def name(self):
        return self.soup.find('h1', attrs={'class': 'class-details-header-name'}).string

    @property
    def lessons(self):
        xx = (i.string for i in self.soup.find_all('script', type='text/javascript'))
        data = next(i for i in xx if 'SS.serverBootstrap' in i.string)
        ss = data.split(';', 1)[1].rsplit(';', 3)[0].split('=', 1)[-1]
        jj = json.loads(ss)
        units = jj['pageData']['unitsData']['units'][0]['sessions']
        for u in units:
            yield u['title'], u['videoId'][3:]


def clear(s):
    s = re.sub('[^A-Za-z0-9]', '_', s)
    s = re.sub('_+', '_', s).strip('_')
    return s


class Manager:
    user_agent_val = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
    headers = {
                'User-Agent': user_agent_val
            }

    def __init__(self, account_id, basepath=''):
        self.account_id = account_id
        self.basepath = basepath

        session = requests.Session()
        session.get('https://www.skillshare.com/login', headers={
            'User-Agent': self.user_agent_val
        })
        session.headers.update({
                    'User-Agent': self.user_agent_val
                })
        session.post(
                'https://www.skillshare.com/login',
                {'email': 'shelestova.des@gmail.com', 'password': 'Barselona2020'},
        )

        self.session = session

    def ffmpeg(self, m3u8_link, filename):
        s = f'ffmpeg -protocol_whitelist "file,http,https,tcp,tls" -i "{m3u8_link}" -bsf:a aac_adtstoasc -vcodec copy -c copy -crf 50 {filename}'
        os.system(s)
        # subprocess.Popen(s)

    def download_mp4(self, video_id, filename):
        link = f"https://edge.api.brightcove.com/playback/v1/accounts/{self.account_id}/videos/{video_id}"

        headers = {
            'Accept': "application/json;pk=BCpkADawqM2OOcM6njnM7hf9EaK6lIFlqiXB0iWjqGWUQjU7R8965xUvIQNqdQbnDTLz0IAO7E6Ir2rIbXJtFdzrGtitoee0n1XXRliD-RH9A-svuvNW9qgo3Bh34HEZjXjG4Nml4iyz3KqF",
            'User-Agent': self.user_agent_val
                   }

        self.session.headers.update(headers)
        res = self.session.get(link).json()

        m3u8_link = next(i['src'] for i in res['sources'])
        self.ffmpeg(m3u8_link, filename)

    def download_lessons(self, soup):
        course = Course(soup)

        dirname = os.path.join(self.basepath, clear(course.name))
        os.makedirs(dirname, exist_ok=True)

        with fs.catch_exceptions():
            for name, video_id in course.lessons:
                filename = os.path.join(dirname, clear(name) + '.mp4')
                self.download_mp4(video_id, filename)

    def download_courses(self, links):
        for link in links:
            print(link)
            session = requests.Session()
            headers = main_headers
            session.headers.update(headers)
            content = session.get(link + '?via=custom-lists').text
            soup = fs.soup(content)
            self.download_lessons(soup)


if __name__ == '__main__':
    account_id = '3695997568001'
    m = Manager(account_id)
    # links = ['https://www.skillshare.com/classes/Cinema-4D-Creating-Procedured-Ornament-2D-and-3D-with-no-plugin/434176040']
    with open('Download_SkillShare.txt') as f:
        links = f.read().split('\n')
    m.download_courses(links)