import json
def build_chat(subject, message, finish=True):
    return {
        "from": subject,
        "message": message,
        "finish": finish
    }

def parse_agent_answer(answer):
    return json.loads(answer)