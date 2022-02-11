from datetime import timedelta
import flask
from flask import *
import requests
import os
import random
import mysql.connector
from mysql.connector import Error
from flask_cors import CORS
import speech_recognition

app = flask.Flask(__name__, static_url_path='/static')
app.secret_key = 'unity_web'  # secret_key存session到cookie所需
app.permanent_session_lifetime = timedelta(minutes=270)  # 設定使用者使用時間
CORS(app)
app.config["DEBUG"] = True  # 開啟debug讓我們可以隨時因為程式的變動而更新

@app.route("/", methods=['POST', 'GET'])
def login():
    try:
        mydb = mysql.connector.connect(
            host="localhost",       # 数据库主机地址
            user="root",    # 数据库用户名
            passwd="",   # 数据库密码
            database="unity"
        )
        
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM account")
        myresult = mycursor.fetchall()

        # for x in myresult:
        #     print(x)
            
    except Error as e:
        print("資料庫連接失敗：", e)

    finally:
        if (mydb.is_connected()):
            mycursor.close()
            mydb.close()
            print("資料庫關閉")
    return  "connect success"

@app.route("/login", methods=['POST', 'GET'])
def dataprocess():
    try:
        mydb = mysql.connector.connect(
            host="localhost",       # 数据库主机地址
            user="root",    # 数据库用户名
            passwd="",   # 数据库密码
            database="unity"
        )
        mycursor = mydb.cursor()
        school = request.form['loginSchool']
        account = request.form['loginUser']
        password = request.form['loginPassword']
        
        mycursor.execute("SELECT school,password FROM account WHERE account ='"+account+"'")
        myresult = mycursor.fetchall()
        print("result:",myresult)
        for x,pwd in myresult:
            print(x,pwd)
            print(school,password)
            if str(x) == school and str(pwd)==password:
                return "login success"

            else:
                return "login error"
            
    except Error as e:
        print("資料庫連接失敗：", e)

    finally:
        if (mydb.is_connected()):
            mycursor.close()
            mydb.close()
            print("資料庫關閉")
    return  str(myresult)

@app.route("/Speech", methods=['POST', 'GET'])
def speechTotext():
    try:
        text = request.form['Text']
        print("result:",text)

        r = speech_recognition.Recognizer()
        with speech_recognition.Microphone() as source:
            r.adjust_for_ambient_noise(source,duration=0.5)
            print("say")
            audio = r.record(source,duration=4)
        try:
            print("recognition")
            rec = r.recognize_google(audio,language="en-US")
            text = rec.replace("台","臺")
            print(text)
            return text
        except speech_recognition.UnknownValueError:
            print("can't recognition")
        except speech_recognition.RequestError as e:
            print("no response:{0}".format(e))

        return "1"
            
    except Error as e:
        print("失敗：", e)

    # finally:
    #     if (mydb.is_connected()):
    #         mycursor.close()
    #         mydb.close()
    #         print("資料庫關閉")
    return  str("2")

if __name__ == "__main__":
    r_animal = random.randint(0, 19)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port,ssl_context=('server.crt', 'server.key'))
