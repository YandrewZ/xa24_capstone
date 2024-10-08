
# ✨💬 Dr. Date

This is a dating coach chatbot. To run the chatbot, follow the steps below:

1. Clone the repository to your local machine:

```
git clone https://github.com/YandrewZ/xa24_capstone.git
```
or download the zip file and extract it.


2. Make sure you have Python 3.8 or later installed on your machine.
   
to check your Python version, run the following command in your terminal:

```
python --version
``` 
or 

```
python3 --version
```

3. Start a virtual environment and install the required packages:

```
cd xa_capstone
python -m venv myenv  # or use python3 -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
```

4. Set up your groq api key by running the following command in terminal:
   

```
mkdir .streamlit
touch .streamlit/secrets.toml
```

then, open the 'secrets.toml' file and add the following line:
```
GROQ_API_KEY = "YOUR_API_KEY"
```

5. Start the chatbot using streamlit:

```
streamlit run chatroom_script.py
```

The chatbot will be running on your local machine at a address like http://localhost:8501/. You can open this address in your browser to start chatting with the chatbot.


6. To stop the program, hit **ctrl + c**, you can then deactivate the virtual environment in the terminal by running:

```
deactivate
```
