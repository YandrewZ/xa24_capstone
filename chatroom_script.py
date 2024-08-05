import streamlit as st
import replicate
import os
# import streamlit_shadcn_ui as ui

import openai
import os
from openai import OpenAI

client = OpenAI(api_key = st.secrets['GROQ_API_KEY'], base_url='https://api.groq.com/openai/v1')

def get_groq_response(chat_history):
    messages = [
        # Set an optional system message. This sets the behavior of the assistant
        # and can be used to provide specific instructions for how it should behave
        # throughout the conversation.
        {
            "role": "system",
            "content": "Let's play a role-playing game! You are a cold and somewhat distant single, young man. You name is 陈青山, and you can be creative about your background, such as career and hobbies. Talk to the user like in a messaging app. Sound as natural as possible. Respond only in Chinese"
            # "content": "act cool, always respond in Chinese, and sound as natural as possible"
        },
    ]
    for message in chat_history:
        if message['role'] == '你':
            messages.append({
                "role": "user",
                "content": message['content']
            })
        else:
            messages.append({
                "role": "assistant",
                "content": message['content']
            })
    response = client.chat.completions.create(
        # Required parameters
        model="llama3-8b-8192",
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

    return response.choices[0].message.content

CONSTANT_MALE_AVATAR_SRC = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSmoZiabTeeX88qDYqFuFhlaA__ks06srKaQ2zhi_b_UwP_ywY92otb9SDC_34fvnBEsh4&usqp=CAU"
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

    fondness_bar = st.progress(20, text='暧昧')
    friendship_bar = st.progress(20, text='友情')
    
    # st.slider("好感", min_value=0, max_value=100, value=date_score, key="slider", disabled=True, )




# Create a slider
# # Use columns to create a narrower progress bar
# col1, col2, col3 = st.columns([0.1, 1, 0.1])  # Adjust the ratio to control the width

# with col2:
    
#     # Create the content area
#     col2.write("Donec elit turpis, pellentesque eget condimentum ut, feugiat at tellus. Nam maximus tempor hendrerit. Mauris vulputate lorem eget ligula interdum elementum a sit amet felis. Duis dui urna, posuere nec varius non, tincidunt et ipsum. Quisque at enim a felis mollis rutrum. Etiam pellentesque ipsum ut mi pellentesque, laoreet sodales lorem laoreet. \n\n")
#     col2.write("目标: 让他喜欢你。\n\n")



# background info box
background_info_code = """
<div style="border: 2px solid #020047; border-radius: 10px; padding: 20px;">
    <p style="">
        最近，你注意到了这个特别内向、神秘和才华横溢的男孩/女孩，你希望和他....
    </p>
    <div style="margin-bottom: 40px;"></div>
    <p style="color: #F06D6D; font-weight: bold;">
        目标: 让ta喜欢你
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
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "陈青山", "content": "什么事。", "avatar_src": CONSTANT_MALE_AVATAR_SRC, "is_user": False}]


# Display or clear chat messages
for message in st.session_state.messages:
    add_chat_message(message["role"], message["content"], message["avatar_src"], is_user=message["is_user"])
    # with st.chat_message(message["role"]):
    #     st.write(message["content"])

# Function to update the slider values
def update_fondness_slider(value):
    fondness_bar.progress(value, text='好感')
def update_friendship_slider(value):
    friendship_bar.progress(value, text='友情')

def clear_chat_history():
    st.session_state.messages = [{"role": "陈青山", "content": "什么事。", "avatar_src": CONSTANT_MALE_AVATAR_SRC, "is_user": False}]
st.sidebar.button('Reset', on_click=clear_chat_history)

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
#                            input={"prompt": f"{string_dialogue} {prompt_input} Assistant: ",
#                                   "temperature":temperature, "top_p":top_p, "max_length":max_length, "repetition_penalty":1})
#     return output

# User-provided prompt
if prompt := st.chat_input(disabled=False):
    st.session_state.messages.append({"role": "你", "content": prompt, "avatar_src": "https://imagedelivery.net/tSvh1MGEu9IgUanmf58srQ/e2b094c8-8519-4e8b-e92e-1cf8d4b58f00/public", "is_user": True})
    add_chat_message("你", prompt, "https://imagedelivery.net/tSvh1MGEu9IgUanmf58srQ/e2b094c8-8519-4e8b-e92e-1cf8d4b58f00/public", is_user=True)
    # with st.chat_message("user"):
    #     st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "陈青山":
    # response = generate_llama2_response(prompt)
    # full_response = ''
    # for item in response:
    #     full_response += item

    response = get_groq_response(st.session_state.messages)
    
    # with st.spinner("Thinking..."):
    #     # response = generate_llama2_response(prompt)
    #     placeholder = st.empty()
    #     full_response = ''
    #     for item in response:
    #         full_response += item
    #         placeholder.markdown(full_response)
    #     placeholder.markdown(full_response)
    message = {"role": "陈青山", "content": response, "avatar_src": CONSTANT_MALE_AVATAR_SRC, "is_user": False}
    st.session_state.messages.append(message)
    add_chat_message("陈青山", response, CONSTANT_MALE_AVATAR_SRC, is_user=False)    

    # with st.chat_message("assistant"):
    #     with st.spinner("Thinking..."):
    #         response = generate_llama2_response(prompt)
    #         placeholder = st.empty()
    #         full_response = ''
    #         for item in response:
    #             full_response += item
    #             placeholder.markdown(full_response)
    #         placeholder.markdown(full_response)
    # message = {"role": "assistant", "content": full_response}
    # st.session_state.messages.append(message)