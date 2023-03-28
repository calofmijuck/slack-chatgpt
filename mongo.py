import pymongo

client = pymongo.MongoClient(username="root", password="root")

db = client.chatgpt
sessions = db.sessions


def get_session(session_id: str):
    session = sessions.find_one({"_id": session_id})
    if session is None:
        session = sessions.insert_one({"_id": session_id, "messages": []})
    return session


def update_session(session_id: str, messages):
    return sessions.update_one({"_id": session_id}, {"$set": {"messages": messages}})


def reset_session(session_id: str):
    return sessions.update_one({"_id": session_id}, {"$set": {"messages": []}})
