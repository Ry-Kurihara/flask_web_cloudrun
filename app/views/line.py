import pandas as pd 
from app import engine
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../lib/'))
from google_sm import SecretManagerUtil
import textwrap 

LINE_CHANNEL_ACCESS_TOKEN = "LINE_CHANNEL_ACCESS_TOKEN"
LINE_CHANNEL_SECRET = "LINE_CHANNEL_SECRET"

import logging
logger = logging.getLogger('app.flask').getChild(__name__)

"""
LINEメッセージ処理
"""

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

sm_utl = SecretManagerUtil()
line_cat = sm_utl.get_secret(LINE_CHANNEL_ACCESS_TOKEN)
line_cs = sm_utl.get_secret(LINE_CHANNEL_SECRET)

line_bot_api = LineBotApi(line_cat)
handler = WebhookHandler(line_cs)

from flask import Blueprint
from flask import request, abort
from flask import current_app as app
line = Blueprint('line', __name__)

"""
年齢は？メッセージ対応のパッケージ
"""
import datetime
from dateutil.relativedelta import relativedelta 

"""
処理記述
"""

@line.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    # TODO: Loggerを変えた時の出力を検証する
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    user_id = str(event.source.user_id)
    timestamp = str(event.timestamp)
    message = event.message.text 

    # メッセージをデータベースに保存する
    df = pd.DataFrame(data=[[user_id, timestamp, message]], columns=['user_id', 'timestamp', 'message'])
    df.to_sql('line_message_history', con=engine, if_exists='append', index=False)

    if 'github' in message:
        send_text1 = TextSendMessage(text='拝承')
        send_text2 = TextSendMessage(text='https://github.com/Ry-Kurihara?tab=repositories')
        line_bot_api.reply_message(
            event.reply_token, [
                send_text1,
                send_text2
            ]
        )
    elif '年齢' in message:
        age_obj = get_age_obj(1995, 12, 27)
        send_text1 = TextSendMessage(f"{age_obj.years}歳と{age_obj.months}ヶ月と{age_obj.days}日ニナリマス")
        line_bot_api.reply_message(
            event.reply_token, [
                send_text1
            ]
        )
    elif 'ガクチカ' in message:
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text=textwrap.dedent("""
                    学生時代では、講義や研究以外でもプログラム言語やマークアップ言語に出来るだけ触れるように意識していました。最近では、多くのサービスがインターネット上で展開されているため、自分から何かを発信したいと思った時にプログラミング力やデザイン技術は、必ず自分の役に立つと思っています。 
                    具体的にしたこととして、WordPressの独自デザインテンプレートを作成した経験があります。これにはHTMLやCSS、少しのPHP知識を必要とするため、それらを勉強しながらデザインを構築していくことで実践的な技術が身につきました。 
                    その経験を活かして、研究室の同期と共同で地域の歯科医院の公式ホームページの作成を担当しています。院長から、こういったサイトにしたいという要望を聞き、その要望に近づけるようにサイトを制作していくという、企業に勤める上で必要となる能力を鍛える貴重な機会にもなっています。 
                """))
            ]
        )
    else:
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text='想定シテイナイメッセージデス')
            ]
        )
        


def get_age_obj(year, month, day) -> relativedelta:
    today = datetime.date.today()
    birthday = datetime.date(year, month, day)
    diff = relativedelta(today, birthday)
    return diff

if __name__ == '__main__':
    sm_utl = SecretManagerUtil()
    line_cat = sm_utl.get_secret(PROJECT_ID, LINE_CHANNEL_ACCESS_TOKEN)
    line_cs = sm_utl.get_secret(PROJECT_ID, LINE_CHANNEL_SECRET)
    print(f"{line_cat}だよ")