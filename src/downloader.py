#!/usr/bin/python3

import requests
import sys
import os

from InquirerPy import inquirer
from yt_dlp import YoutubeDL

VIDEO_PATH = "BTK_KURSLARI"
try:
    os.mkdir(VIDEO_PATH)
except FileExistsError:
    pass

ACCESS_TOKEN = ""
try:
    with open('token.txt','r') as file:
        ACCESS_TOKEN = file.read().strip()
except FileNotFoundError:
    print("token.txt dosyası açılamadı!")
    sys.exit()
if not ACCESS_TOKEN:
    print("ACCES_TOKEN bulunamadı! Kendi ACCES_TOKEN'ininiz eklemek için README.md'ye göz atınız")
    sys.exit()

BASE_URL = "https://www.btkakademi.gov.tr/api/service/v1"

headers = {}
headers['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0"
headers["Authorization"] = f"Bearer {ACCESS_TOKEN}"
headers["Accept"] = "application/json, text/plain, */*"
headers["Content-Type"] =  "application/json"

def GetCourseId(CourseUrl: str) -> str:
    return CourseUrl.split("-")[-1]


def GetHlsStream(CourseId: str, LessonId: str, headers={}):
    try:
        response = requests.post(
                f"{BASE_URL}/course/deliver/start/{LessonId}",
                headers=headers,
                json={"programId": int(CourseId)},
        )
    except Exception as err:
        return {"error":err}
        
    if not response.ok:
        return {"error":f"Bad status:{response.status_code}"}

    data = response.json()
    hls_api_id = data.get("remoteCourseReference")
    try:
        response = requests.get(f'https://cinema8.com/api/v1/uscene/rawvideo/flavor/{hls_api_id}')
    except Exception as err:
        print(err)
        return {"error":err}

    if not response.ok:
        return {"error":f"Bad status:{response.status_code}"}
    data = response.json()
    return {"name":data.get('name'),"hls_url":data.get('hlsUrl')}

def GetSyllabus(CourseId: str,headers={}):
    try:
        response = requests.get(
                f"{BASE_URL}/public/51/course/details/program/syllabus/{CourseId}",
                headers=headers,
        )
    except Exception as err:
        return {"error":err}

    if not response.ok:
        return {"error":f"Bad status:{response.status_code}"}
    return {'data':response.json()}



def main():
    CourseUrl = inquirer.text(message="Kurs linki:").execute()
    CourseId = GetCourseId(CourseUrl)
    SylabbusData = GetSyllabus(CourseId,headers=headers)

    if SylabbusData.get('error'):
        print(SylabbusData.get('error'))
        sys.exit(1)

    Sylabbus = SylabbusData['data']
    choices = [item["title"] for item in Sylabbus]
    
    response = inquirer.select(
        message="Ders seçin:",
        choices=choices
    ).execute()
    
    section = next(item for item in Sylabbus if item["title"] == response)
    courses = [item["title"] for item in section["courses"]]
    
    response = inquirer.select(
        message="Bölüm seçin:",
        choices=courses
    ).execute()

    lesson = next(item for item in section["courses"] if item["title"] == response)
    LessonId = lesson["id"]
    metadata = GetHlsStream(CourseId,LessonId,headers=headers)
    
    if metadata.get('error'):
        print(metadata.get('error'))
        sys.exit()

    ydl_opts = {
            'outtmpl': os.path.join(VIDEO_PATH,metadata['name']),
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(metadata['hls_url'])

if __name__ == "__main__":
    main()
    
