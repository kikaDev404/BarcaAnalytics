
def make_user_message(message : str):
    return [{'role' : 'user' , 'content' : message}]

def make_system_message(message : str):
    return [{'role' : 'system', 'content' : message}]

def chat_ollama(agent, user_message, history):
    history.append({"role": "user", "content": user_message})

    response = agent.chat.completions.create(
        model='qwen3:8b',
        messages=history
    )

    assistant_reply = response.choices[0].message.content
    
    history.append({"role": "assistant", "content": assistant_reply})

    return assistant_reply, history