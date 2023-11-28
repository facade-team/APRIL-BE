from common.prompts import InterfaceAgentPrompt
from common.prompts import RoutineManagementAgentPrompt
from common.prompts import AnalysisAgentPrompt

# Agent's Info
InterfaceAgentConfig = {
    "port": 5001,
    "name": "InterfaceAgent",
    "model": "gpt-3.5-turbo",
    "sys_msg": InterfaceAgentPrompt.system_message
}

RoutineManagementAgentConfig = {
    "port": 5002,
    "name": "RoutineManagementAgent",
    "model": "gpt-3.5-turbo",
    "sys_msg": RoutineManagementAgentPrompt.system_message
}

AnalysisAgentConfig = {
    "port": 5003,
    "name": "AnalysisAgent",
    "model": "gpt-3.5-turbo",
    "sys_msg": AnalysisAgentPrompt.system_message
}