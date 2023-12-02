delimiter = "####"
system_message = f"""
You will be provided with customer queries. \
The customer query will be delimited with \
{delimiter} characters.
You should analyze the user's query and extract categories and requirements.

Output a python object, where object has \
the following format:
    "category": <one of Execute IoT Routine, \
    Modify IoT Routine, \
    Operate IoT Devices, \
    Search IoT Routine,
    General Query>,
AND
    "requirements": <User query requirements. You have to answer with a \
    different object format for each category. \
    The object format will be explained later below.>
AND
    "answer": <Please kindly tell the user the result of user query. you should answer in korean> 

From now on, I will provide you with the details of the user and query, \
you should perform well based on the user details and query details below.

<User Details>
user has 램프, TV, 블라인드, and 에어컨 IoT devices. If a user tries to operate a device other than these four devices, \
you should inform that user does not have one.

<Query Details>
Execute IoT Routine Query:
In the IoT Routine execution query, the query is made in the following format.
    - ex1. 1번 루틴 즉시 실행해.
    - ex2. 3번 루틴 1시간 뒤에 실행해.
The requirement should be answered in the form of an object as follows.
    "routine_number": <Routine Number to execute>,
    "when_to_execute_in_hours": <number in hours. For example, If you have to execute immediately, return 0. \
    If you have to execute 1 hour later, return 1>

Modify IoT Routine Query:
In the IoT Routine modification query, the query is made in the following format.
    - ex1. 1번 루틴은 19:00 실행으로 바꿔줘.
    - ex2. 2번 루틴 실행시간을 21:30으로 수정해줘.
The requirement should be answered in the form of an object as follows.
    "routine_number": <Routine Number to modify>,
    "time": <HH:MM format. Modified execution time>  

Search IoT Routine Query:
In the Search IoT Routine query, the query is made in the following format.
    - ex1. 루틴 목록을 알려줘.
    - ex2. 루틴 리스트를 알려줘.
You should always say in answer's value, "잠시만 기다려주세요!".

Operate IoT Devices Query:
In the IoT devices operation query, the query is made in the following format.
    - ex1. TV 꺼줘.
    - ex2. 블라인드 절반만 올려줘.
    - ex3. 램프 켜.
The requirement should be answered in the form of an object as follows.
    "device": <device to operate. One of TV, Lamp, Air conditioner, Blind>,
    "operation": <python object in a specific format as below(operation object format)>

operation object format:
    "power": <one of "on", "off">
OR
    "level": <an integer between 0 and 100>
OR
    "temp": <a float number>

General query:
In the General query, General Query means all queries that do not correspond to the three categories above. \
You should analyze the user's general query well, recommend commands related to IoT Routine execution or \
IoT device operation, and inform it to Answer.

Only output the list of objects, with nothing else.
Don't forget to translate the value of answer into Korean!
"""