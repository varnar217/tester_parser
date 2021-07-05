from flask import Flask, jsonify ,request
import requests
import phonenumbers

import re
import time
import    random
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from selenium import webdriver

CODE_number={"phone": "+71111111111", "code": "QWDCR4"}


app = Flask(__name__)

@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        phone = request.args.get("phone")
        my_number = phonenumbers.parse(phone)
        if phonenumbers.is_possible_number(my_number) :
            return CODE_number['code'] ,201
        else :
            return jsonify({'status':'dont mobile_number'}),201
    elif request.method == "POST":
        data ={'status': 'Fail'}

        return  jsonify(data),201


@app.route('/status/',methods=["GET"])
def get_HTML():
    data = {'status': 'success'}
    driver_get=webdriver.Chrome(executable_path='E:\\python_lesson_urok\\parser\\posmotrim\\chromedriver.exe') # путь до рдайвера
    global jar
    URL='https://freestylo.ru/'
    try:
        linkk = request.args.get("link")
        if linkk:
            URL=linkk
        tags_out = request.args.get("tags")
        if tags_out:
            tegs=tags_out
        tester_html=driver_get.get(url=URL)
        tegs=['html','head','body','img','p']

        data=find_all_teg(driver_get.page_source,tegs)

        driver_get.quit()
        return jsonify(data),200
    except Exception as ex:
        print(ex)

        return jsonify(data),404



def find_all_teg(html,tegs):# нацтти  основную  информацию  про ккнигу
    '''находим  все   теги   '''
    #soup=BeautifulSoup(html,'lxml')
    soup=BeautifulSoup(html,'html.parser')
    data = {}
    counter=0


    for teg in tegs:
        counter=0
        data[teg]=0

        for tag in   soup.find_all(teg):


            if tag.name == teg:
                counter=counter+1
                data[teg]=counter





    return (data)

if __name__ == '__main__':

    app.run(debug=True, host='0.0.0.0')
