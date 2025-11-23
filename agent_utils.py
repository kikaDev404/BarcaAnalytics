
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

def process_ai_response(response):
    if "<think>" in response and "</think>" in response:
        before_think, rest = response.split("<think>", 1)
        think_content, after_think = rest.split("</think>", 1)

        # Wrap think block in a light yellow background
        formatted_think = (
            f"<div style='background-color:#e0e0e0;"
            f"border-left:4px solid #f4c430;padding:10px;margin:10px 0;'>"
            f"<strong>🧠 Agent Thinking:</strong><br>{think_content.strip()}</div>"
        )

        return (before_think + formatted_think + after_think).strip()

    return response