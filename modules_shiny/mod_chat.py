import logging
from shiny import module, ui, render, reactive
from common import*
import config
from os.path import join
from shinywidgets import output_widget, render_widget
from charts import*
import ba_colors_collection.ba_colors as colors
from pre_process import*
from openai import OpenAI
from agent_utils import*
import re
import json
from dotenv import load_dotenv

load_dotenv(override=True)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_KEY")

project_root = config.DIR_NAMES.project_root
log_folder = join(project_root, config.DIR_NAMES.log_folder) 

log_obj = config_log('mod_side_bar', join(log_folder, 'mod_side_bar.log'), logging.INFO)
log = log_obj.get_logger()

log.info('Lodding Chat tab')

system_instruction = """
You are a helpful assistant integrated into the Barca Analytics dashboard. you help the user to get the insights about the data, modify the filters and helps them with dashboard navigation.
The dashboard show the historical data of barcelona match from 2000 to 2025.
there are many things in the dashboard. 
You can update the 'Match Played' filter which is there in the dashboard. 

To change the filter, you MUST output a JSON block at the end of your response. The tool or the function which I have to help you to update the filter is clled update_filter(value).
The valid values for 'value' are: "Home", "Away", "Home & Away". 

Example format:
{
"tool": "update_filter",
"parameters": {
"value": "Home"
}
}

text
Only use this JSON when the user explicitly asks to change the filter or view.
"""

memory = [] + make_system_message(system_instruction)

openrouter = OpenAI(
    api_key = OPENROUTER_API_KEY,
    base_url = "https://openrouter.ai/api/v1"
)


@module.ui
def chat_ui():
        return ui.card(
            ui.chat_ui("agent_chat", messages= ['Hi there, This is your Barca Analytics agent at your service. '])
    )

@module.server
def chat_server(input, output, session, filter_state): # Ensure filter_state is passed here
    chat = ui.Chat("agent_chat")

    # Helper function to update the shared state
    def update_filter(new_val):
        valid_options = ['Home', 'Away', 'Home & Away']
        if new_val in valid_options:
            filter_state.set(new_val) 
            
            return True
        return False

    @chat.on_user_submit
    async def handle_user_input(user_input: str):
        global memory
        
        # 1. Get response from Ollama
        agent_response, memory = chat_openrouter(openrouter, user_input, memory)
        
        # 2. Regex to find JSON block (looks for `````` or just { ... })
        json_pattern = r"``````|(\{.*\})"
        match = re.search(json_pattern, agent_response, re.DOTALL)
        
        cleaned_response = agent_response

        if match:
            try:
                # Extract the JSON string (group 1 or group 2)
                json_str = match.group(1) if match.group(1) else match.group(2)
                command_data = json.loads(json_str)
                
                # 3. Check tool name and execute
                if command_data.get("tool") == "update_filter":
                    val = command_data.get("parameters", {}).get("value")
                    if update_filter(val):
                        # Optional: Add a system note that it worked
                        agent_response, memory = chat_openrouter(openrouter, 'I have sucessfully updated the filter', memory)
                        print(f"Agent updated filter to: {val}")
                
                # 4. Remove the JSON code block from the chat display
                # This keeps the UI clean for the user
                cleaned_response = agent_response.replace(match.group(0), "").strip()
                
            except json.JSONDecodeError:
                pass # JSON was malformed, just show the text

        # 5. Append only the text part to the chat
        if cleaned_response:
            await chat.append_message(process_ai_response(cleaned_response))