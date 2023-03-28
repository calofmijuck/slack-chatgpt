from slack import RTMClient

from chatgpt import ChatGPT
from config import SLACK_BOT_TOKEN

DATA: dict[str, list[dict[str, str]]] = {}

@RTMClient.run_on(event="message")
def chatgptbot(**payload):
    data = payload["data"]
    web_client = payload["web_client"]
    bot_id = data.get("bot_id", "")
    subtype = data.get("subtype", "")
    origin_text = data.get("text", "")
    tag_code = origin_text.split(" ")[0]

    # print(data)

    if bot_id == "" and subtype == "" and tag_code == "<@U050LJCJBJP>":
        channel_id = data["channel"]
    
        text = data.get("text", "")
        text = text.split(">")[-1].strip()
    
        message_ts = data["ts"]

        key = f"{channel_id}:{data['user']}"
        if key not in DATA:
            DATA[key] = []

        if text == "reset":
            DATA[key] = []
            web_client.chat_postMessage(channel=channel_id, text="Session reset!", thread_ts=message_ts)
            return

        DATA[key].append(
            {"role": "user", "content": text}
        )

        response = ChatGPT(DATA[key])
        
        DATA[key].append(
            {"role": "assistant", "content": response}
        )
        
        web_client.chat_postMessage(channel=channel_id, text=response, thread_ts=message_ts)


if __name__ == "__main__":
    try:
        rtm_client = RTMClient(token=SLACK_BOT_TOKEN)
        print("Bot connected and running!")
        rtm_client.start()
    except Exception as err:
        print(err)
