from flask import Flask, jsonify ,request
import requests
import phonenumbers

import re
import time
import    random
from bs4 import BeautifulSoup
from selenium import webdriver

CODE_number={"phone": "+71111111111", "code": "QWDCR4"}
librari_CODE=[
{"phone": "+71111111111", "code": "QWDCR4"},
{"phone": "+71218111191", "code": "QWDCA8"},
{"phone": "+71318111191", "code": "AWDCA8"}
]

app = Flask(__name__)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        phone =request.query_string.decode() # из за +
        phof=phone.split('=')
        if phof[0] == 'phone' :
            try:
                my_number = phonenumbers.parse(phof[1])
                if phonenumbers.is_possible_number(my_number) :
                    return jsonify({'code':CODE_number['code']})  ,200

            except Exception as ex:
                pass
                return jsonify({'status':'dont mobile_number'}),200

    elif request.method == "POST":
        data ={'status': 'Fail'}
        data_post  = request.json
        for iter in librari_CODE:

            if data_post.get('phone') ==  iter['phone'] and  data_post.get('code') ==  iter['code'] :
                data ={'status': 'OK'}
                break



        return  jsonify(data),201


@app.route('/status/',methods=["GET"])
def get_HTML():
    # пока работает запрос /status/
    data = {'status': 'success'}
    driver_get=webdriver.Chrome(executable_path='E:\\python_lesson_urok\\parser\\posmotrim\\chromedriver.exe') # путь до рдайвера
    global jar
    URL='https://freestylo.ru/'
    tegs=['html','head','body','img','p']
    try:
        linkk = request.args.get("link")
        if linkk:
            URL=linkk
        tags_out = request.args.get("tags")
        tegs_bufer=''
        if tags_out:
            tegs_bufer=tags_out
            tegs = tuple((item) for item in tegs_bufer.split(','))

        tester_html=driver_get.get(url=URL)


        data=find_all_teg(driver_get.page_source,tegs)

        driver_get.quit()
        return jsonify(data),200
    except Exception as ex:
        print(ex)

        return jsonify(data),404



def find_all_teg(html,tegs):# найти информацию
    '''находим  все   теги   '''

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


@app.route('/check_structure/',methods=["POST"])
def get_check_structure():
    data_post  = request.json

    data2 ={'is_correct': 'False','difference':''} #{'is_correct': 'False'}
    driver_get=webdriver.Chrome(executable_path='E:\\python_lesson_urok\\parser\\posmotrim\\chromedriver.exe') # путь до рдайвера
    URL= 'https://'+data_post['link']+'/'
    tegs=data_post['structure']

    tester_html=driver_get.get(url=URL)
    tk=list(tegs.keys())

    data=[]
    data=find_all_teg(driver_get.page_source,tk) ;


    driver_get.quit()
    flag=True

    data3=[]
    for key, value in data.items():

        for key_set, value_set in tegs.items():


            if key == key_set and value != value_set:

                flag=False
                data3.append({key_set:value_set})


    if flag :
        return jsonify({'is_correct': 'True'}),201
    data2['difference']=data3

    return jsonify(data2),201


if __name__ == '__main__':

    app.run(debug=True, host='0.0.0.0')
