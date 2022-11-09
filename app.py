#載入LineBot所需要的套件
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import re
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
cred = credentials.Certificate("serviceAccountKey.json")

firebase_admin.initialize_app(cred)
db= firestore.client()

app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('AYTGJqrvRKnASK+e7V+rmlK/SGWDVeQZvuYVupBTYHvvODuLrLbmiYvKV0UbNY9HEgRspoqS4/cY3fgIf3rLaYGnTkIr8IbZ89LJv0LPtKOmssXcD9umGMseVIyue8YyUIKMET4IJCxZpxi0eg9H1QdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('32a386a3e47d9b4a6ecb03fd05249bf0')
# 必須放上自己的ID
line_bot_api.push_message('U6fb87062d1aa60abdf0eb1656e1fbbb5', TextSendMessage(text='你可以開始了'))


# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

 
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

 
#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = text=event.message.text

    emoji = [
    {
        "index": 0,
        "productId": "5ac1bfd5040ab15980c9b435",
        "emojiId": "001"
    },
    {
        "index": 2,
        "productId": "5ac1bfd5040ab15980c9b435",
        "emojiId": "002"
    },
    {
        "index": 15,
        "productId": "5ac1bfd5040ab15980c9b435",
        "emojiId": "002"
    }
    ]

    
    
    if re.match('拍照',message):
        flex_message = TextSendMessage(text='以下有雷，請小心',
        quick_reply=QuickReply(items=[
        QuickReplyButton(action=CameraAction(label="拍照")),
        QuickReplyButton(action=MessageAction(label="按我", text="按！")),
        QuickReplyButton(action=MessageAction(label="別按我", text="你按屁喔！爆炸了拉！！"))]))
        line_bot_api.reply_message(event.reply_token, flex_message)
    if re.match('連結',message):
        text_message = TextSendMessage(text="連結 : https://cruelshare.com/")
        line_bot_api.reply_message(event.reply_token, text_message)
    if re.match('emoji',message):
        text_message = TextSendMessage(text='$ $ LINE emoji $', emojis=emoji)
        line_bot_api.reply_message(event.reply_token, text_message)
    if re.match('老師', message):
        # db.collection("Teacher").add({'Name':"Kevin", "Number": "0000000000", 'Subject':"all"})
        Teachers = db.collection("Teacher").get()
        teacherList = []
        for teacher in Teachers:
            teacherList.append(teacher.to_dict())
    
        carousel_template_message = TemplateSendMessage(
             alt_text='免費教學影片',
             template=CarouselTemplate(
                 columns=[
                    for teacher in teacherList:
                        CarouselColumn(
                         thumbnail_image_url=teacher["Picture"],
                         title=teacher['Name'],
                         text="Subject : " + for sub in teacher['Subject'],
                         actions=[
                             MessageAction(
                                 label='預約試教',
                                 text='Still in progress'
                             )
                         ]
                     )
                 ]
             )
         )
        line_bot_api.reply_message(event.reply_token, carousel_template_message)
    # Line QuckReply for Subject selection, Get subjects from existing teachers
    if re.match("我要找老師",message):
        Teachers = db.collection("Teacher").get()
        SubjectSet =set()
        for teacher in Teachers:
            teacher = teacher.to_dict()
            for sub in teacher["Subject"]:
                SubjectSet.add(sub)


        flex_message = TextSendMessage(text='請選擇你想加強的科目',
            quick_reply=QuickReply(items=[
                for subject in SubjectSet:
                    QuickReplyButton(action=MessageAction(label=subject, text="I am Looking For a {sub} Teacher".format(sub=subject)))
            ])
        )
        line_bot_api.reply_message(event.reply_token, flex_message)

    """
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message))
    """

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)