# APRIL Backend Server

## 실행방법
1. 가상환경 생성 및 활성화
```bash
python -m venv venv
source venv/bin/activate
```

2. 패키지 설치
```bash
pip install -r requirements.txt
```

3. .env 파일 추가
```
# .env 파일 구조
OPENAI_API_KEY=openai_api_key_입력
```

4. RabbitMQ server 실행 (도커)
```bash
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15682:15672 rabbitmq:3.8-management

# 아래는 백그라운드 실행
docker run -d -it --rm --name rabbitmq -p 5672:5672 -p 15682:15672 rabbitmq:3.8-management
```

4. Agent 서버 실행
```bash
# Run InterfaceAgent agent on PORT:5001
python agents/InterfaceAgent/app.py

# Run RoutineManagementAgent agent on PORT:5002
python agents/RoutineManagementAgent/app.py

# Run AnalysisAgent agent on PORT:5003
python agents/AnalysisAgent/app.py
```