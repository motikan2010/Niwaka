import datetime
import os
import random
import string
import subprocess
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
load_dotenv()

WORK_DIR = "work"
REQEST_TEXT_SUFFIX = "_request.txt"
RESPONSE_TEXT_SUFFIX = "_response.txt"
SLACK_TEXT_SUFFIX = "_slack.txt"

slack_token = os.getenv('BOT_TOKEN')
app_token = os.getenv('APP_TOKEN')

app = App(token=slack_token)

def store_request(input_text: str):
    """
    依頼内容をテキストファイルに保存する。
    """
    req_id = datetime.datetime.now().strftime("%Y%m%d%H%M%S")+ "_" + ''.join([random.choice(string.ascii_letters + string.digits) for i in range(12)])
    open(f"{WORK_DIR}/{req_id}{REQEST_TEXT_SUFFIX}", mode="w").write(input_text)
    return req_id

def request_gpt(req_id: str) -> None:
    """
    依頼内容をMCPに入力する。回答内容はテキストファイルに保存する。
    """
    res = subprocess.run(f"cat {WORK_DIR}/{req_id}{REQEST_TEXT_SUFFIX} | llm --no-intermediates", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    open(f"{WORK_DIR}/{req_id}{RESPONSE_TEXT_SUFFIX}", mode="w").write(res.stdout.decode("utf8"))

def generate_slack_response(req_id: str) -> str:
    """
    Slackへ返信するテキストを作成する。
    """
    prompt = f"""テキストファイル /usr/app/{WORK_DIR}/{req_id}{RESPONSE_TEXT_SUFFIX} を要約してください。
    プログラムコードが含まれる場合はMarkDown形式で出力してください。回答は本文のみを出力してください。"""
    res = subprocess.run(["llm", "--no-intermediates", prompt], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    slack_response: str = res.stdout.decode("utf8")
    open(f"{WORK_DIR}/{req_id}{SLACK_TEXT_SUFFIX}", mode="w").write(slack_response)
    return "\n".join(slack_response.split("\n")[2:])


@app.event("app_mention")
def response(event, say):
    # 1. Slackからメッセージを取得
    input_text: str = event["text"]
    thread_ts: str = event.get("thread_ts")
    print(input_text)

    # 2. 依頼内容をテキストファイルに保存
    req_id = store_request(input_text)
    say(text="ご依頼受領しました。考え中・・・")

    # 3. 依頼内容をMCPに入力
    request_gpt(req_id)
    say(text="回答作成中・・・")

    # 4. Slackへ返信するテキストを作成
    slack_response = generate_slack_response(req_id)

    # 5. Slackに返信
    if thread_ts:
        say(text=slack_response, thread_ts=thread_ts)
    else:
        say(text=slack_response)

def test_store_request():
    store_request("TEST")

def test_request_gpt():
    request_gpt("20250418080032_XpW9paSGGZWi")

def test_generate_slack_response():
    slack_response = generate_slack_response("20250418080032_XpW9paSGGZWi")
    print(slack_response)

if __name__ == "__main__":
    #test_store_request()
    #test_request_gpt()
    #test_generate_slack_response()

    print("Run slackbot.py")
    SocketModeHandler(app, app_token).start()
