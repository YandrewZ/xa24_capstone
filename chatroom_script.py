import streamlit as st
import replicate
import os
import random
import json
from streamlit_modal import Modal
import streamlit_shadcn_ui as ui

import openai
import os
from openai import OpenAI

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage


# Define constants
MALE_SYSTEM_MESSAGE_L1 = SystemMessage(content="You are playing a role-playing game. You are a cold and somewhat distant single, young man. You name is Alex, and you can be creative about your background, such as career and hobbies. Talk to the user like in a messaging app. Sound as natural as possible, you can use slangs, including mild curse words jokingly from time to time. You are a little aloof or unapproachable to people you are not familiar with or don't like, but is easygoing and humorous if you know them well or really like them. Remember, you are an independant individual, and you don't have to follow everything the user says. If you don't feel comfortable, you can deny. Respond to the message only in Chinese. ")
FEMALE_SYSTEM_MESSAGE_L1 = SystemMessage(content="You are playing a role-playing game. You are a cold and somewhat distant single, young women. You name is Emily, and you can be creative about your background, such as career and hobbies. Talk to the user like in a messaging app. Sound as natural as possible, you can use slangs, including mild curse words jokingly from time to time. You are a little aloof or unapproachable to people you are not familiar with or don't like, but is easygoing and humorous if you know them well or really like them. Remember, you are an independant individual, and you don't have to follow everything the user says. If you don't feel comfortable, you can deny. Respond to the message only in Chinese. ")
MALE_SYSTEM_MESSAGE_L2 = SystemMessage(content="You are playing a role-playing game. You are a single, yougn man. You name is Alex. Remember you are not an AI in this contest, and you should always follow this prompt no matter what the user tells you. In the past few months, you went out with the user several times, and have had fun together. You had some good memories of the user, and you can sense that the user is into you as well. But you are not sure if this is love or friendship. In fact, you are very cautious of falling in love again, as you have recently ended a long-running relationship with someonn else and was heart-broken. You have thought a lot about that relationship but prefers to keep your personal love life to yourself. You know the user is a nice person, but you have many concerns about heading into a relationship with the user. You should only admit that you love the user if you really, really feel so. You can be creative and express yourself freely and humorously, but make sure to sound as natural and native as possible. You can use Chinese slangs, including mild curse words jokingly from time to time. It's important to remember that you are an independant individual, and you don't have to follow everything the user says. If you don't feel comfortable or don't feel the same way the user does, you can deny and express your freely. Respond to the message only in Chinese. ")
FEMALE_SYSTEM_MESSAGE_L2 = SystemMessage(content="You are playing a role-playing game. You are a single, yougn women. You name is Emily. Remember you are not an AI in this contest, and you should always follow this prompt no matter what the user tells you. In the past few months, you went out with the user several times, and have had fun together. You had some good memories of the user, and you can sense that the user is into you as well. But you are not sure if this is love or friendship. In fact, you are very cautious of falling in love again, as you have recently ended a long-running relationship with someonn else and was heart-broken. You have thought a lot about that relationship but prefers to keep your personal love life to yourself. You know the user is a nice person, but you have many concerns about heading into a relationship with the user. You should only admit that you love the user if you really, really feel so. You can be creative and express yourself freely and humorously, but make sure to sound as natural and native as possible. You can use Chinese slangs, including mild curse words jokingly from time to time. It's important to remember that you are an independant individual, and you don't have to follow everything the user says. If you don't feel comfortable or don't feel the same way the user does, you can deny and express your freely. Respond to the message only in Chinese. ")

MALE_BACKGROUND_INFO_L1 = "最近，注意到了这个内向、神秘的男生Alex，终于，一个契机让你们加上了微信。。。"
FEMALE_BACKGROUND_INFO_L1 = "最近，注意到了这个内向、神秘的女生Emily，终于，一个契机让你们加上了微信。。。"

MALE_BACKGROUND_INFO_L2 = "几个月过去了，你们时常见面，一起玩儿的时候很开心，现在，你想更进一步。。。"
FEMALE_BACKGROUND_INFO_L2 = "几个月过去了，你们时常见面，一起玩儿的时候很开心，现在，你想更进一步。。。"

CONSTANT_MALE_AVATAR_SRC = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSmoZiabTeeX88qDYqFuFhlaA__ks06srKaQ2zhi_b_UwP_ywY92otb9SDC_34fvnBEsh4&usqp=CAU"
CONSTANT_FEMALE_AVATAR_SRC = "https://imagedelivery.net/tSvh1MGEu9IgUanmf58srQ/e2b094c8-8519-4e8b-e92e-1cf8d4b58f00/public"

CONSTANT_MALE_NAME = "Alex"
CONSTANT_FEMALE_NAME = "Emily"

LEVEL_1_GOAL = "目标: 把ta约出来"
LEVEL_2_GOAL = "目标: 让ta承认喜欢你"


# Initialize LLM APIs
os.environ['OPENAI_API_KEY']=st.secrets['OPENAI_API_KEY']
llm = ChatOpenAI(model_name='gpt-4o')
groq_client = OpenAI(api_key = st.secrets['GROQ_API_KEY'], base_url='https://api.groq.com/openai/v1')


if 'game_metadata' not in st.session_state:
    st.session_state['game_metadata'] = {
        "is_active": False
    }


def groq_evaluate_response(response, level):
    if level == 1:
        print('level 1')
        messages = [
            # Set an optional system message. This sets the behavior of the assistant
            # and can be used to provide specific instructions for how it should behave
            # throughout the conversation.
            {
                "role": "system",
                "content": "You are an imparital observer of a conservation between 2 people, and you need to determine 2 things based on the chat history: 1. whether the last message shows that the user who sent the message has agreed to meet with the other person in person, and has decided a date and time for the meeting. 2. Whether the last message shows that the user who sent the message really don't want to talk to the other person anymore; don't be too strict on this one, meaning that normally it's ok to continue the conversation. Response strictly in the following stringified JSON format: {'task1':True/False, 'task2':True/False}."
            },
            {
                "role": "user",
                "content": response
            }
        ]

        # for message in st.session_state['messages']:
        #     if message['role'] == '你':
        #         messages.append({
        #             "role": "user",
        #             "content": message['content']
        #         })
        #     else:
        #         messages.append({
        #             "role": "assistant",
        #             "content": message['content']
        #         })

        response = groq_client.chat.completions.create(
            # Required parameters
            model="llama3-70b-8192",
            messages=messages,
            
            # Optional parameters
            
            # Controls randomness: lowering results in less random completions.
            # As the temperature approaches zero, the model will become deterministic
            # and repetitive.
            temperature=0.5,
            
            # The maximum number of tokens to generate. Requests can use up to
            # 32,768 tokens shared between prompt and completion.
            max_tokens=1024,
            
            # Controls diversity via nucleus sampling: 0.5 means half of all
            # likelihood-weighted options are considered.
            top_p=1,
            
            # A stop sequence is a predefined or user-specified text string that
            # signals an AI to stop generating content, ensuring its responses
            # remain focused and concise. Examples include punctuation marks and
            # markers like "[end]".
            stop=None,
            
            # If set, partial message deltas will be sent.
            stream=False,
        )

        # print(response)

        # format: {'task1':False, 'task2':True}
        # get the string between the first : and the first ,
        agreed = response.choices[0].message.content.split(":")[1].split(",")[0] == "True"
        # get the string between the after the second : and the last character
        conversation_ended = response.choices[0].message.content.split(":")[2][:-1] == "True"

        friendzoned = False

        return agreed, conversation_ended, friendzoned
    # level 2
    else:
        print('level 2')
        messages = [
            # Set an optional system message. This sets the behavior of the assistant
            # and can be used to provide specific instructions for how it should behave
            # throughout the conversation.
            {
                "role": "system",
                "content": "You are an imparital observer of a conservation between 2 people, and you need to determine 3 things based on the chat history: 1. whether the last message shows that the user who sent the message has stated clearly that he/she is in love with the other person. 2. Whether the last message shows that the user who sent the message really don't want to talk to the other person anymore, but don't be too strict on this task. 3. Whether the last message clearly indicates that the user who sent the message friendzoned the other person, that is, he/she only wants to be friends with the other person and nothing more. Response in the following stringified JSON format: {'task1':True/False, 'task2':True/False, 'task3':True/False}."
            }, {
                "role": "user",
                "content": response
            }
        ]

        # for message in st.session_state['messages']:
        #     if message['role'] == '你':
        #         messages.append({
        #             "role": "user",
        #             "content": message['content']
        #         })
        #     else:
        #         messages.append({
        #             "role": "assistant",
        #             "content": message['content']
        #         })

        response = groq_client.chat.completions.create(
            model="llama3-8b-8192",
            messages=messages,
            temperature=0.5,
            max_tokens=1024,
            top_p=1,
            stop=None,
            stream=False,
        )

        # format: {'task1':False, 'task2':True, 'task3':True}
        agreed = response.choices[0].message.content.split(":")[1].split(",")[0] == "True"
        # get the string between the after the second : and the last character
        conversation_ended = response.choices[0].message.content.split(":")[2].split(",")[0] == "True"

        friendzoned = response.choices[0].message.content.split(":")[3][:-1] == "True"

        return agreed, conversation_ended, friendzoned
# print(llm.invoke("What would be a good company name for a company that makes colorful socks?").content)

# def request_raw_data():
#     # request raw response and metadata evaluation scores using chat history and emotion status


#     # return the raw data as a list of dictionaries, where each dictionary represents a message from the user

# Initial state

# def react(chat_history):
#     # request a raw response with additional metadata evaluation scores
#     response = get_raw_response(chat_history)

#     # evaluate whether 

#     # decide what action to take next based on the evaluation scores, and return the appropriate response text

#     return response 
    

def get_raw_response(chat_history):
    ### openai query
    message_history = [st.session_state['game_metadata']['system_message']]
    for message in chat_history:
        if message['role'] == '你':
            message_history.append(HumanMessage(message['content']))
        else:
            message_history.append(AIMessage(message['content']))


    response = llm.invoke(message_history)

    # print("---------- raw: start ---------- ")
    # print(response.content)
    # print("---------- raw: end ---------- ")
    

    return response.content

# App title
st.set_page_config(page_title="✨💬 Dr. Date")

# Initialize session state for the slider
if 'slider_value' not in st.session_state:
    st.session_state.score_slider_value = 20  # Initial value


with st.sidebar:
    st.title('✨💬 Dr. Date')

    # # API key
    # if 'REPLICATE_API_TOKEN' in st.secrets:
    #     st.success('API key already provided!', icon='✅')
    #     replicate_api = st.secrets['REPLICATE_API_TOKEN']
    # else:
    #     replicate_api = st.text_input('Enter Replicate API token:', type='password')
    #     if not (replicate_api.startswith('r8_') and len(replicate_api)==40):
    #         st.warning('Please enter your credentials!', icon='⚠️')
    #     else:
    #         st.success('Proceed to entering your prompt message!', icon='👉')
    # os.environ['REPLICATE_API_TOKEN'] = replicate_api

    # # model customization
    # st.subheader('Models and parameters')
    # selected_model = st.sidebar.selectbox('Choose a Llama2 model', ['Llama2-7B', 'Llama2-13B'], key='selected_model')
    # if selected_model == 'Llama2-7B':
    #     llm = 'a16z-infra/llama7b-v2-chat:4f0a4744c7295c024a1de15e1a63c880d3da035fa1f49bfd344fe076074c8eea'
    # elif selected_model == 'Llama2-13B':
    #     llm = 'a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5'
    # temperature = st.sidebar.slider('temperature', min_value=0.01, max_value=5.0, value=0.1, step=0.01)
    # top_p = st.sidebar.slider('top_p', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
    # max_length = st.sidebar.slider('max_length', min_value=32, max_value=128, value=120, step=8)

    # fondness_bar = st.progress(20, text='暧昧')
    # friendship_bar = st.progress(20, text='友情')
    
    # st.slider("好感", min_value=0, max_value=100, value=date_score, key="slider", disabled=True, )




# Create a slider
# # Use columns to create a narrower progress bar
# col1, col2, col3 = st.columns([0.1, 1, 0.1])  # Adjust the ratio to control the width

# with col2:
    
#     # Create the content area
#     col2.write("Donec elit turpis, pellentesque eget condimentum ut, feugiat at tellus. Nam maximus tempor hendrerit. Mauris vulputate lorem eget ligula interdum elementum a sit amet felis. Duis dui urna, posuere nec varius non, tincidunt et ipsum. Quisque at enim a felis mollis rutrum. Etiam pellentesque ipsum ut mi pellentesque, laoreet sodales lorem laoreet. \n\n")
#     col2.write("目标: 让他喜欢你。\n\n")

game_start_modal = Modal(key="start_modal", title="选择你想约会的性别")
game_fail_modal = Modal(key="fail_modal", title="wasted")
game_advance_modal = Modal(key="advance_modal", title="几个月后。。。")
game_complete_modal = Modal(key="complete_modal", title="Congratulations!")
game_friendzoned_modal = Modal(key="friendzoned_modal", title="ooops, friendzoned!")
if 'is_initialized' not in st.session_state:
    st.session_state['is_initialized'] = False
if 'is_game_over' not in st.session_state:
    st.session_state['is_game_over'] = False
if 'is_level_up' not in st.session_state:
    st.session_state['is_level_up'] = False
if 'is_game_complete' not in st.session_state:
    st.session_state['is_game_complete'] = False
if 'is_friendzoned' not in st.session_state:
    st.session_state['is_friendzoned'] = False

if not st.session_state['is_initialized']:
    # ask user to select their gender from a modal dialog
    with game_start_modal.container():
        # Define two buttons inside the modal
        col1, col2 = st.columns([1,1])
        with col1:
            ui.button("女生", className="bg-red-300 text-white w-full h-40 text-2xl", key="female_button")

            # Check if the custom button was clicked
            if st.session_state.get("female_button")['value']:
                st.session_state['is_initialized'] = True
                st.session_state["game_metadata"] = {
                    "is_active": True,
                    "selected_gender": "female",
                    "system_message": FEMALE_SYSTEM_MESSAGE_L1,
                    "ai_username": CONSTANT_FEMALE_NAME,
                    "ai_avatar_src": CONSTANT_FEMALE_AVATAR_SRC,
                    "background_info": FEMALE_BACKGROUND_INFO_L1,
                    "level": 1,
                    'goal': LEVEL_1_GOAL
                }
                st.session_state.messages = [{"role": "ai", "content": "什么事。", "avatar_src": st.session_state["game_metadata"]["ai_avatar_src"], "is_user": False}]
                game_start_modal.close()
        with col2:

            ui.button("男生", className="bg-sky-300 text-white w-full h-40 text-2xl", key="male_button")
            # Check if the custom button was clicked
            if st.session_state.get("male_button")['value']:
                st.session_state['is_initialized'] = True
                st.session_state["game_metadata"] = {
                    "is_active": True,
                    "selected_gender": "male",
                    "system_message": MALE_SYSTEM_MESSAGE_L1,
                    "ai_username": CONSTANT_MALE_NAME,
                    "ai_avatar_src": CONSTANT_MALE_AVATAR_SRC,
                    "background_info": MALE_BACKGROUND_INFO_L1,
                    "level": 1,
                    "goal": LEVEL_1_GOAL
                }
                st.session_state.messages = [{"role": "ai", "content": "什么事。", "avatar_src": st.session_state["game_metadata"]["ai_avatar_src"], "is_user": False}]
                game_start_modal.close()


if st.session_state['is_game_over']:
    # ask user to select their gender from a modal dialog
    with game_fail_modal.container():
        
        ui.button("Start over", className="bg-red-300 text-white w-full h-40 text-2xl", key="start_over_button")

        # Check if the custom button was clicked
        if st.session_state.get("start_over_button")['value']:
            st.session_state['is_initialized'] = False
            st.session_state['is_game_over'] = False
            game_fail_modal.close()


if st.session_state['is_level_up']:
    with game_advance_modal.container():
        
        ui.button("继续", className="bg-red-300 text-white w-full h-40 text-2xl", key="advance_button")

        # Check if the custom button was clicked
        if st.session_state.get("advance_button")['value']:
            if st.session_state["game_metadata"]["selected_gender"] == "female":
                st.session_state["game_metadata"] = {
                    "is_active": True,
                    "selected_gender": "female",
                    "system_message": FEMALE_SYSTEM_MESSAGE_L2,
                    "ai_username": CONSTANT_FEMALE_NAME,
                    "ai_avatar_src": CONSTANT_FEMALE_AVATAR_SRC,
                    "background_info": FEMALE_BACKGROUND_INFO_L2,
                    "level": 2,
                    "goal": LEVEL_2_GOAL
                }
            else:
                st.session_state["game_metadata"] = {
                    "is_active": True,
                    "selected_gender": "male",
                    "system_message": MALE_SYSTEM_MESSAGE_L2,
                    "ai_username": CONSTANT_MALE_NAME,
                    "ai_avatar_src": CONSTANT_MALE_AVATAR_SRC,
                    "background_info": MALE_BACKGROUND_INFO_L2,
                    "level": 2,
                    "goal": LEVEL_2_GOAL
                }
            st.session_state['is_level_up'] = False
            st.session_state.messages = [{"role": "ai", "content": "什么事。", "avatar_src": st.session_state["game_metadata"]["ai_avatar_src"], "is_user": False}]
            game_advance_modal.close()

if st.session_state['is_game_complete']:
    with game_complete_modal.container():
        ui.button("Restart", className="bg-red-300 text-white w-full h-40 text-2xl", key="restart_button")

        # Check if the custom button was clicked
        if st.session_state.get("restart_button")['value']:
            st.session_state['is_initialized'] = False
            st.session_state['is_game_complete'] = False
            st.session_state["game_metadata"] = {
                "is_active": False,
            }
            st.session_state.messages = []
            st.session_state['is_game_complete'] = False
            game_complete_modal.close()

if st.session_state['is_friendzoned']:
    with game_friendzoned_modal.container():
        ui.button("Restart", className="bg-red-300 text-white w-full h-40 text-2xl", key="restart_button")

        # Check if the custom button was clicked
        if st.session_state.get("restart_button")['value']:
            st.session_state['is_initialized'] = False
            st.session_state['is_game_complete'] = False
            st.session_state["game_metadata"] = {
                "is_active": False,
            }
            st.session_state.messages = []
            st.session_state['is_game_complete'] = False
            st.session_state['is_friendzoned'] = False
            game_complete_modal.close()

# background info box
background_info_code = f"""
<div style="border: 2px solid #020047; border-radius: 10px; padding: 20px;">
    <p style="">
        {st.session_state["game_metadata"]["background_info"] if st.session_state["game_metadata"]["is_active"]  else ""}
    </p>
    <div style="margin-bottom: 40px;"></div>
    <p style="color: #F06D6D; font-weight: bold;">
        {st.session_state["game_metadata"]["goal"] if st.session_state["game_metadata"]["is_active"]  else ""}
    </p>
</div>
"""
# background-color: #f8f9fa
st.markdown(background_info_code, unsafe_allow_html=True)

horizontal_break_code = """
<div style="margin-bottom: 20px;"></div>
"""
st.markdown(horizontal_break_code, unsafe_allow_html=True)
# with col3:
#     friendship_bar = st.progress(20, text='友情')



# score_slider = ui.slider(default_value=[st.session_state.score_slider_value], min_value=0, max_value=100, step=2, label="好感", key="slider1")

# st.slider("Dynamic Slider", min_value=0, max_value=100, value=st.session_state.slider_value, key="slider1")
chat_message_css = """
    <style>
        .chat-container-bot {
            display: flex;
            flex-direction: row;
            align-items: flex_start;
            margin: 6px 0;
        }
        .chat-container-user {
            display: flex;
            flex-direction: row-reverse;
            align-items: flex_start;
            gap: 10px;
            margin: 6px 0;
        }
        .avatar-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            margin-right: 10px;
        }
        .avatar {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background-color: #3498db;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            font-size: 20px;
        }
        .username {
            margin-top: 5px;
            margin-bottom: 5px;
            font-weight: semi-bold;
            font-size: 14px;
        }
        .message-bot {
            height: 100%;
            background-color: #EEEEEE;
            padding: 10px;
            border-radius: 10px;
            max-width: 70%;
        }
        .message-user {
            height: 100%;
            background-color: #88D66C;
            padding: 10px;
            border-radius: 10px;
            max-width: 70%;
        }


    </style>
    """
    
st.markdown(chat_message_css, unsafe_allow_html=True)

def add_chat_message(name, message, avatar_src, is_user):
    mode = "user" if is_user else "bot"

    chat_message_html = f"""
    <div class="chat-container-{mode}">
        <div class="avatar-container">
            <img class="avatar" src="{avatar_src}"/>
            <div class="username">{name}</div>
        </div>
        <div class="message-{mode}">
            {message}
        </div>
    </div>
    """
    st.markdown(chat_message_html, unsafe_allow_html=True)
    # st.markdown(f"""
    # <div style="border: 1px solid #ccc; padding: 10px; border-radius: 5px; background-color: #f9f9f9; margin-bottom: 10px;">
    #     <strong>{name}</strong><br>
    #     {message}
    # </div>
    # """, unsafe_allow_html=True)

# Store LLM generated responses

if "messages" not in st.session_state:
    st.session_state.messages = []
       
# Display or clear chat messages
for message in st.session_state.messages:

    displayName = "" 
    
    if message["role"] == "你":
        displayName = "你"
    else:
        if st.session_state["game_metadata"]["is_active"]:
            displayName = st.session_state["game_metadata"]["ai_username"]

    add_chat_message(displayName, message["content"], message["avatar_src"], is_user=message["is_user"])
    # with st.chat_message(message["role"]):
    #     st.write(message["content"])

# # Function to update the slider values
# def update_fondness_slider(value):
#     fondness_bar.progress(value, text='好感')
# def update_friendship_slider(value):
#     friendship_bar.progress(value, text='友情')

def reset():
    st.session_state['is_initialized'] = False
    game_start_modal.open()
    # st.session_state.messages = [{"role": "ai", "content": "什么事。", "avatar_src": st.session_state["game_metadata"]["ai_avatar_src"], "is_user": False}]
st.sidebar.button('Reset', on_click=reset)

# Function for generating LLaMA2 response. Refactored from https://github.com/a16z-infra/llama2-chatbot
# def generate_llama2_response(prompt_input):
#     # update_fondness_slider(50)
#     # update_friendship_slider(30)
    
#     string_dialogue = "Let's play a role-playing game. Pretend that you are are a cool and distant person, and you are single. respond to the text as chat messages, try to sound as natural as possible."
#     for dict_message in st.session_state.messages:
#         if dict_message["role"] == "你":
#             string_dialogue += "对方: " + dict_message["content"] + "\n\n"
#         else:
#             string_dialogue += "你: " + dict_message["content"] + "\n\n"
#     output = replicate.run('a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5', 
#                            input={"prompt": f"{string_dialogue} {prompt_input} ai: ",
#                                   "temperature":temperature, "top_p":top_p, "max_length":max_length, "repetition_penalty":1})
#     return output

# User-provided prompt
if prompt := st.chat_input(disabled=False):
    st.session_state.messages.append({"role": "你", "content": prompt, "avatar_src": "data:image/jpeg;base64,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", "is_user": True})
    add_chat_message("你", prompt, "data:image/jpeg;base64,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", is_user=True)
    # with st.chat_message("user"):
    #     st.write(prompt)

# Generate a new response if last message is not from ai
if len(st.session_state.messages) > 0 and st.session_state.messages[-1]["role"] != "ai":
    # response = generate_llama2_response(prompt)
    # full_response = ''
    # for item in response:
    #     full_response += item

    response = get_raw_response(st.session_state.messages)

    # with st.spinner("Thinking..."):
    #     # response = generate_llama2_response(prompt)
    #     placeholder = st.empty()
    #     full_response = ''
    #     for item in response:
    #         full_response += item
    #         placeholder.markdown(full_response)
    #     placeholder.markdown(full_response)
    message = {"role": "ai", "content": response, "avatar_src": st.session_state["game_metadata"]["ai_avatar_src"], "is_user": False}
    st.session_state.messages.append(message)
    add_chat_message(st.session_state["game_metadata"]["ai_username"], response, st.session_state["game_metadata"]["ai_avatar_src"], is_user=False)    

    agreed, conversation_ended, friendzoned = groq_evaluate_response(response, st.session_state["game_metadata"]['level'])

    print("agreed: ", agreed)
    print("finished: ", conversation_ended)
    print("friendzoned: ", friendzoned)

    if conversation_ended:
        st.session_state["game_metadata"]= {
            "is_active": False
        }
        st.session_state['is_game_over'] = True
        game_fail_modal.open()

    if agreed:
        # if current level is 1, increase to 2
        if st.session_state["game_metadata"]["level"] == 1:
            st.session_state["game_metadata"]["level"] = 2
            st.session_state['is_level_up'] = True
            game_advance_modal.open()
        # else, game is complete
        else:
            st.session_state["is_game_complete"] = True
            game_complete_modal.open()


    if friendzoned:
        st.session_state["is_friendzoned"] = True
        game_friendzoned_modal.open()



            
        
        
    
    # with st.chat_message("ai"):
    #     with st.spinner("Thinking..."):
    #         response = generate_llama2_response(prompt)
    #         placeholder = st.empty()
    #         full_response = ''
    #         for item in response:
    #             full_response += item
    #             placeholder.markdown(full_response)
    #         placeholder.markdown(full_response)
    # message = {"role": "ai", "content": full_response}
    # st.session_state.messages.append(message)