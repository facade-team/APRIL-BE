from common.prompts import InterfaceAgentPrompt
from common.prompts import RoutineManagementAgentPrompt
from common.prompts import AnalysisAgentPrompt

# Agent's Info
InterfaceAgentConfig = {
    "port": 5001,
    "name": "InterfaceAgent",
    "model": "gpt-3.5-turbo",
    "sys_msg": InterfaceAgentPrompt.system_message,
    "delimiter": InterfaceAgentPrompt.delimiter
}

RoutineManagementAgentConfig = {
    "port": 5002,
    "name": "RoutineManagementAgent",
    "model": "gpt-3.5-turbo",
    "sys_msg": RoutineManagementAgentPrompt.system_message,
    "delimiter": RoutineManagementAgentPrompt.delimiter
}

AnalysisAgentConfig = {
    "port": 5003,
    "name": "AnalysisAgent",
    "model": "gpt-4-1106-preview",
    "sys_msg": AnalysisAgentPrompt.system_message,
    "delimiter": AnalysisAgentPrompt.delimiter
}

# Smart Home IoT API
SMART_HOME_API_BASE = "http://172.20.10.8:5555" # production
# SMART_HOME_API_BASE = "http://127.0.0.1:5555" # local