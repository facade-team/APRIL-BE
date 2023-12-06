import os
from openai import OpenAI
from collections import deque
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # 환경변수 Read

class Agent:
    def __init__(self, name, model, embeddings, system_message, max_chat_history_length=100):
        self.client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
        self.name = name
        self.model = model
        self.embeddings = embeddings
        self.system_message = system_message
        self.chat_history = deque([])
        self.max_chat_history_length = max_chat_history_length

    def get_embedding(self, text, model="text-embedding-ada-002"):
        text = text.replace("\n", " ")
        return self.client.embeddings.create(input=[text], model=model)["data"][0]["embedding"]

    def chat(self, user_input):
        system_message = self.system_message
        messages = [{"role": "system", "content": system_message}]
        for message in self.chat_history:
            messages.append(message)
        messages.append({"role": "user", "content": user_input})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        assistant_message = response.choices[0].message.content
        if len(self.chat_history) > self.max_chat_history_length:
            self.chat_history.popleft()
            self.chat_history.popleft()
        self.chat_history.append({"role": "user", "content": user_input})
        self.chat_history.append({"role": "assistant", "content": assistant_message})

        return assistant_message