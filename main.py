
from elastic_utils import ElasticUtils
from flask import Flask, render_template, request
import random

UNKNOW_ANS = ['چی میگی؟', 'متوجه نشدم!', 'دیگه چه خبر؟']

app = Flask(__name__)

engine = ElasticUtils('localhost', '9200')

learning_mode = 0
user_teach = {}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    global learning_mode, user_teach
    userText = request.args.get('msg')
    if userText == '/learn':
        learning_mode = 1
        return "حالت یادگیری فعال است. لطفا متن ورودی را بنویسید"
    elif userText == '/stop':
        learning_mode = 0
        return "یادگیری غیرفعال است"

    if learning_mode > 0:
        if learning_mode == 1:
            user_teach['input'] = userText
            learning_mode = 2
            return 'حالا پاسخ را وارد کنید'
        elif learning_mode == 2:
            user_teach['output'] = userText
            learning_mode = 1
            engine.learn(user_teach)
            return 'این سوال و جواب اضافه شد. لطفا سوال و جواب بعدی را وارد کنید'
    else: 
        response = engine.respond(userText)
        if response:
            return random.choice(response['output'])
        else:
            return random.choice(UNKNOW_ANS)

if __name__ == "__main__":
    app.run()