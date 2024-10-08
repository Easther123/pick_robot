import requests

# 提供的Kimi API密钥
from openai import OpenAI

API_KEY = 'sk-rXnCXckoXy1v67VmMOZFfff4Bl2kypzv7PGoYx0PqStsHPLj'

# Kimi API的基础URL
API_BASE = "https://api.moonshot.cn/v1"

def llm_kimi(prompt):
    '''
    Kimi大模型API
    '''
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "moonshot-v1-8k",  # 可以根据需要选择不同的模型
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,  # 根据需要调整
        "top_p": 0.8,  # 根据需要调整
        "penalty_score": 1.0  # 根据需要调整
    }
    response = requests.post(f"{API_BASE}/chat/completions", headers=headers, json=data)
    if response.status_code == 200:
        response_json = response.json()
        return response_json['choices'][0]['message']['content']  # 根据实际返回结构调整
    else:
        raise Exception(f"Error calling Kimi API: {response.status_code} - {response.text}")

# 示例调用
if __name__ == "__main__":
    prompt = "我想要写一个Python代码"

    response = llm_kimi(prompt)
    print(response)

