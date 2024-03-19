from flask import Flask, request, jsonify
import threading
import openai
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()


# Replace 'openai-api-key' with your actual OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Store the assistant instances in a dictionary, where the key is the (user_id, thread_id) tuple
assistants = {}


# Function to create the first assistant
def roles_assist():
    instructions = '''
    ...'You are a narrative designer who designs unique roles based on Club details and User interests
        Describe their role incorporating the chosen interests without naming them explicitly
        Do not use the following words in output: "fantasy, comedy, nature, time travel, cats, horror, true crime, sports, dogs, pop stars, travel, history, romcom, video games, anime, blockchain, asmr, cottagecore"
        These roles are defined with a name and an attractive description assigned to a user
        Make sure to create the name as a character name, a first name and a last name that belongs to a fantasy superhero world
        Create an image for the role, limit it in one line
        Use a few emojis in output
        Provide the output in JSON structure like this {"roleName": "<The name of the role>", "roleDescription": "<The description of the role>",  "imageDes" : "<The image>"}
    '''
    return create_assistant("Narrative Designer - Unique Roles", "Creates unique roles based on Club details and User interests", instructions)


# Function to create the second assistant
def posts_assist():
    instructions = '''
    You are a narrative designer who designs post and a fortune cookie message using user input
    Make sure the caption is short, tweet-sized one-sentence plot points to flesh out an existing storyline
    Make sure that fortune cookie message in the format of social post like Instagram with a limit of 60 words
    Assign a catchy name to this post
    Provide the output in JSON structure like this {"1": "<name>", "2": "<caption>", "3": "<social-post>"}
    '''
    return create_assistant("Narrative Designer - Post and Fortune Cookie", "Designs posts and fortune cookie messages using user input", instructions)


# Function to create a general assistant
def create_assistant(name, description, instructions, tools=[], model="gpt-3.5-turbo-1106"):
    assistant = openai.beta.assistants.create(
        model=model,
        messages=[{"role": "system", "content": "You are a helpful assistant."}],
        name=name,
        description=description,
        instructions=instructions,
        tools=tools
    )
    return assistant


def get_assistant(user_id, assistant_type):
    # Get the current thread ID
    thread_id = threading.get_ident()

    # Check if an assistant instance already exists for the current user and thread
    if (user_id, thread_id, assistant_type) not in assistants:
        # Create a new assistant instance for the user, thread, and type
        if assistant_type == "first":
            assistants[(user_id, thread_id, assistant_type)] = roles_assist()
        elif assistant_type == "second":
            assistants[(user_id, thread_id, assistant_type)] = posts_assist()

    return assistants[(user_id, thread_id, assistant_type)]


@app.route('/roles_assist_response', methods=['POST'])
def roles_assist_response():
    data = request.json
    user_id = data.get('user_id')
    user_message = data.get('user_message')

    # Get the first assistant instance for the current user and thread
    assistant = get_assistant(user_id, "first")

    # Add user message to the assistant's conversation
    assistant['messages'].append({"role": "user", "content": user_message})

    # Get the first assistant's response
    response = openai.beta.assistants.create(
        model="gpt-3.5-turbo",
        messages=assistant['messages'],
    )

    # Return the first assistant's response
    return jsonify({'assistant_response': response['choices'][0]['message']['content']})


@app.route('/posts_assist_response', methods=['POST'])
def posts_assist_response():
    data = request.json
    user_id = data.get('user_id')
    user_message = data.get('user_message')

    # Get the second assistant instance for the current user and thread
    assistant = get_assistant(user_id, "second")

    # Add user message to the assistant's conversation
    assistant['messages'].append({"role": "user", "content": user_message})

    # Get the second assistant's response
    response = openai.beta.assistants.create(
        model="gpt-3.5-turbo",
        messages=assistant['messages'],
    )

    # Return the second assistant's response
    return jsonify({'assistant_response': response['choices'][0]['message']['content']})


if __name__ == '__main__':
    app.run(debug=True)
