from flask import Flask, render_template, request
import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import random



app = Flask(__name__)

# Load the CSV data into a pandas DataFrame
#data = pd.read_csv('chatbot_data.csv', on_bad_lines='skip')
data = pd.read_csv('chatbot_data.csv', delimiter='?', on_bad_lines='skip', names=['question', 'answer'])

@app.route('/')
def home():

    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.form['user_input']

    # Find the matching question in the DataFrame
    matching_question = process.extractOne(user_input, data['question'], scorer=fuzz.token_sort_ratio)


    if matching_question and matching_question[1] >= 0:
        # Get the corresponding answer for the most likely match
         response = str(data.loc[matching_question[2], 'answer'])
    else:
        random_responses = [
            "I'm sorry, I don't have an answer for that.",
            "I'm still learning and don't have information on that.",
            "I'm afraid I can't help with that question.",
            "That's a good question. Unfortunately, I don't have the answer."
        ]
        response = random.choice(random_responses)

    return response



if __name__ == '__main__':
    app.run(debug=True)


