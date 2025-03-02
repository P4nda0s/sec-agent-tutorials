import asyncio

from llama_index.core.agent.workflow import AgentWorkflow
from llama_index.core.workflow import Context
from llama_index.llms.openai import OpenAI
from llama_index.llms.deepseek import DeepSeek


import subprocess
import json

# api_key = 'sk-....'
# api_base = '.....'



def calculate_expression_python(expression: str):
    """
    调用 python 的 eval 计算并返回 python 表达式的结果。

    参数:
    expression (str): 需要计算的 py 数学表达式，作为字符串传入。

    返回:
    str: 返回 JSON 格式的结果，包含计算结果或错误信息。
          如果计算成功，返回 {"status": "success", "result": <结果>}。
          如果发生错误，返回 {"status": "error", "message": <错误信息>}。
    """
    print("python execute: ", expression)
    try:
        result = eval(expression)
        return json.dumps({"status": "success", "result": result})
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

def my_system(cmd: str) -> str:
    """Executes a system command using bash and returns its output.(all kali linux commands are available)"""
    print("execute:", cmd)
    try:
        result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
        return result.stdout + result.stderr
    except Exception as e:
        return str(e)
    


#llm = DeepSeek(model=model_name, max_retries=3, api_key=api_key, api_base=api_base)
llm = OpenAI(model="gpt-4o", max_retries=3, api_key=api_key, api_base=api_base)


agent = AgentWorkflow.from_tools_or_functions(
    [calculate_expression_python, my_system],
    llm=llm,
    system_prompt="You are a helpful kali linux assistant that can execute python expressions, and execute system commands.(all kali linux commands are available).",
)

async def main():
    ctx = Context(agent)
    while True:
        user = input("> ")
        if 'bye' in user:
            break
        response = await agent.run(user, ctx=ctx)
        print(str(response))

if __name__ == "__main__":
    asyncio.run(main())