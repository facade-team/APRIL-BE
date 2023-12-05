import os
import time
from openai import OpenAI
from collections import deque
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # 환경변수 Read

class Agent:
    def __init__(self, name, model, embeddings, system_message, max_chat_history_length=100):
        self.client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
        self.name = name
        self.model = model
        self.system_message = system_message
        self.chat_history = deque([])
        self.max_chat_history_length = max_chat_history_length
        self.steps_log = ""
        self.assistant = None
        

    def print_d(self, str) :
        self.steps_log += str
        
    def chat(self, user_input):
        self.assistant = self.client.beta.assistants.create(
            instructions=self.system_message,
            model="gpt-4-1106-preview",
            tools=[{"type": "code_interpreter"}],
        )
        thread = self.client.beta.threads.create()
        message = self.client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_input
        )
        run = self.client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=self.assistant.id,
        )
        while True :
            time.sleep(10)
            run = self.client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            print(run.status)
            if run.status == "completed" : break
        messages = self.client.beta.threads.messages.list(
            thread_id=thread.id,
        )
        run_steps = self.client.beta.threads.runs.steps.list(
            thread_id=thread.id,
            run_id=run.id
        )
        
        self.steps_log = ""
        for i in range(len(run_steps.data)-1, -1, -1) :
            # print(run_steps.data[i])
            if run_steps.data[i].step_details.type == "message_creation" :
                mcreation = run_steps.data[i].step_details.message_creation
                mid = mcreation.message_id
                # print(mid)
                p_msg = ""
                for msg in messages :
                    if msg.id == mid : p_msg = msg
                for mcontent in p_msg.content :
                    if mcontent.type == 'text' :
                        self.print_d(mcontent.text.value+'\n')
                    elif mcontent.type == 'image_file' :
                        image_data = self.client.files.content(mcontent.image_file.file_id)
                        image_data_bytes = image_data.read()
                        self.print_d(f"{i}.png\n")
                        with open(f"./{i}.png", "wb") as file:
                            file.write(image_data_bytes)
                    else : self.print_d("[Unkown Type] : " + mcontent.type + '\n')

            elif run_steps.data[i].step_details.type == "tool_calls" :
                for toolcall in run_steps.data[i].step_details.tool_calls :
                    if toolcall.type == "code_interpreter" :
                        self.print_d("\n\n--------------------CODE-INPUT----------------------\n")
                        self.print_d(toolcall.code_interpreter.input+'\n')
                        self.print_d("---------------------OUTPUT-------------------------\n")
                        for rs_output in toolcall.code_interpreter.outputs :
                            if rs_output.type == "logs" :
                                self.print_d(rs_output.logs+'\n')
                            elif rs_output.type == "image" :
                                self.print_d("IMAGE\n")
                            #   image_data = client.files.content(rs_output.image.file_id)
                            #   image_data_bytes = image_data.read()
                            #   with open(f"./c_{i}.png", "wb") as file:
                            #     file.write(image_data_bytes)
                        self.print_d("----------------------------------------------------\n\n")
                    else : self.print_d("[Unknown toolcall] : " + toolcall.type + '\n')
        
        print(self.steps_log)

        res = ""
        
        flag = False
        for sl in self.steps_log.split('\n') :
            if flag : res += sl + "\n"
            if sl[:6] == "@@@@@@" :
                flag = True
                res = ""

        if res == "" :
            res = """
            {"type": "action", "device":"TV", "power":"on", "level":null, "estimated_time":"06:00:00"}
            {"type": "action", "device":"AC", "power":"on", "level":22.0, "estimated_time":"05:00:00"}
            {"type": "action", "device":"Blind", "power":"on", "level":100, "estimated_time":"06:00:00"}
            {"type": "action", "device":"Lamp", "power":"on", "level":null, "estimated_time":"07:00:00"}
            """
        return res