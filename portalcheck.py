#!/usr/bin/env python3

from time import sleep, strftime, localtime
import requests
from HTMLTableParser import HTMLTableParser
import os
from OnlinePanel import OnlinePanel

#sms = OnlinePanel('87.107.121.52)

requests.packages.urllib3.disable_warnings()

sem = "932"
session = 'FEF0C5A732CB539F644EB703117C2F46'

url = "https://portal2.aut.ac.ir/aportal/regadm/student.portal/student.portal.jsp?action=edit&st_info=sem_" + sem + "&st_sub_info=courses"

headers = {
    'Cookie': 'JSESSIONID=' + session
}


def get_courses():
    try:
        response = requests.get(url, headers=headers, verify=False)
        parser = HTMLTableParser()
        parser.feed(response.text)
        info = parser.tables[0][0][1]
        summary = parser.tables[2][2]
        courses = []
        for i in range(5, len(parser.tables[2])):
            course = parser.tables[2][i]
            if len(course[2]) > 0:  # Non TA!
                courses.append({
                    'title': course[1],
                    'title2': course[2],
                    'code': course[3],
                    'v': course[4],
                    'grp': course[5],
                    'score': course[6],
                    'prof': course[8],
                })
        return {
            'info': info,
            'summary': summary,
            'courses': courses,
        }
    except:
        return None


sent_codes = []

while [True]:
    cs = get_courses()
    if cs is None:
        continue
    os.system('clear')
    for c in cs['courses']:
        print(c['score'] + '\t' + c['title2'])
        if c['score'] != '0':
            if not c['code'] in sent_codes:
                sent_codes.append(c['code'])
                sms.send('9195085164', c['title'] + '\r\n' + c['score'])

    print('Last updated: ' + strftime("%Y-%m-%d %H:%M:%S", localtime()))
    sleep(5)
