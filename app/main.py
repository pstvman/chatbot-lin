import os
from flask import Flask, request, jsonify, render_template, session
from flask_cors import CORS
from openai import AsyncOpenAI
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SESSION_SECRET_KEY')
CORS(app)

# 创建一个异步的 OpenAI 客户端
client = AsyncOpenAI()

# 内置系统消息
def init_chat_history():
    return [
        {"role": "system", "content": "You are a helpful assistant. Your name is Lin."},
        {"role": "user", "content": "Hello, how are you?"},
        {"role": "assistant", "content": "I'm great! How can I help you today?"}
    ]

# 默认使用 gpt-4o-mini 模型
async def get_completion(messages, response_format="text", model="gpt-4o-mini"):
    response = await client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7,                                  # 模型输出的随机性，0 表示随机性最小
        # 返回消息的格式，text 或 json_object
        response_format={"type": response_format},
    )
    return response.choices[0].message.content          # 返回模型生成的文本
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
async def chat():
    user_message = request.json.get('message')
    # print(f"User message: {user_message}")
    if not user_message:
        return jsonify({'response': '请输入您的问题。'})
    
    try:
        chat_history = session.get('chat_history', [])
        if not chat_history:
            chat_history = init_chat_history()
        chat_history.append({"role": "user", "content": user_message})
        # 调用 get_completion 函数获取 AI 的响应
        ai_response = await get_completion(chat_history)
        chat_history.append({"role": "assistant", "content": ai_response})
        # 将聊天历史记录保存到 session 中
        session['chat_history'] = chat_history
        return jsonify({'response': ai_response})
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'response': '对不起，我遇到了一些问题。'})


if __name__ == '__main__':
    app.run(debug=True)
