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

project_root = config.DIR_NAMES.project_root
log_folder = join(project_root, config.DIR_NAMES.log_folder) 

log_obj = config_log('mod_side_bar', join(log_folder, 'mod_side_bar.log'), logging.INFO)
log = log_obj.get_logger()

log.info('Lodding Chat tab')

agent_prompt = "you are an helpful assistant. you are integrated to a dashboard named Barca Analytics. you help the user to navigate the dashboards, get insights about the data and do changes to the dashboard on user behalf."
memory = [] + make_system_message(agent_prompt)

ollama = OpenAI(
    api_key = 'ollama',
    base_url = "http://127.0.0.1:11434/v1"
)


@module.ui
def chat_ui():
        return ui.card(
            ui.chat_ui("agent_chat", messages= ['Hi there, This is your Barca Analytics agent at your service. '])
    )

@module.server
def chat_server(input,output,session, filter_state):
    chat = ui.Chat("agent_chat")

    def update_filter(new_value):
         # Instead of updating UI directly, we update the Shared State
         filter_state.set(new_value)

    @chat.on_user_submit
    async def handle_user_input(user_input: str):
        global memory
        agent_response, memory = chat_ollama(ollama,user_input,memory)
        update_filter('Home')

        await chat.append_message(agent_response)
