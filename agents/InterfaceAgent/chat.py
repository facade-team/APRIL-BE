import json
def build_chat(subject, message):
    return {
        "from": subject,
        "message": message
    }

def parse_agent_answer(answer):
    return json.loads(answer)