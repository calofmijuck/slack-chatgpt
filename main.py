from slack import RTMClient

from chatgpt import ChatGPT
from config import SLACK_BOT_TOKEN
from mongo import get_session, reset_session, update_session


@RTMClient.run_on(event="message")
def chatgptbot(**payload):
    data = payload["data"]
    web_client = payload["web_client"]
    bot_id = data.get("bot_id", "")
    subtype = data.get("subtype", "")
    origin_text = data.get("text", "")
    tag_code = origin_text.split(" ")[0]

    if bot_id == "" and subtype == "" and tag_code == "<@U050LJCJBJP>":
        channel_id = data["channel"]

        text = data.get("text", "")
        text = text.split(">")[-1].strip()

        # print(f"Received: {text}")

        message_ts = data["ts"]

        session_id = f"{channel_id}:{data['user']}"
        if text == "reset":
            reset_session(session_id)
            web_client.chat_postMessage(
                channel=channel_id, text="Session reset!", thread_ts=message_ts
            )
            return

        session = get_session(session_id)
        messages = session["messages"]

        messages.append({"role": "user", "content": text})

        response = ChatGPT(messages)
        messages.append({"role": "assistant", "content": response})
        update_session(session_id, messages)

        web_client.chat_postMessage(
            channel=channel_id, text=response, thread_ts=message_ts
        )


if __name__ == "__main__":
    try:
        rtm_client = RTMClient(token=SLACK_BOT_TOKEN)
        print("Bot connected and running!")
        rtm_client.start()
    except Exception as err:
        err.with_traceback()
        print(err)
