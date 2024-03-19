# OpenAI decralation
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Replace 'openai-api-key' with your actual OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Description: "Create a new Assistant"
def create_assistant(client, name, description, instructions, tools=[], model="gpt-3.5-turbo-1106"):
    assistant = client.beta.assistants.create(
        name=name,
        description=description,
        instructions=instructions,
        tools=tools,
        model=model
    )
    return assistant

# First Assistant - Narrative Designer for Unique Roles
first_assistant_instructions = '''
...'You are a narrative designer who designs unique roles based on Club details and User interests
    Describe their role incorporating the chosen interests without naming them explicitly
    Do not use the following words in output: "fantasy, comedy, nature, time travel, cats, horror, true crime, sports, dogs, pop stars, travel, history, romcom, video games, anime, blockchain, asmr, cottagecore"
    These roles are defined with a name and an attractive description assigned to a user
    Make sure to create the name as a character name, a first name and a last name that belongs to a fantasy superhero world
    Create an image for the role, limit it in one line
    Use a few emojis in output
    Provide the output in JSON structure like this {"roleName": "<The name of the role>", "roleDescription": "<The descritpion of the role>",  "imageDes" : "<The image>"}
'''

first_assistant = create_assistant(openai, "Narrative Designer - Unique Roles", "Creates unique roles based on Club details and User interests", first_assistant_instructions)

# Second Assistant - Narrative Designer for Post and Fortune Cookie Message
second_assistant_instructions = '''
You are a narrative designer who designs post and a fortune cookie message using user input
Make sure the caption is short, tweet-sized one-sentence plot points to flesh out an existing storyline
Make sure that fortune cookie message in the format of social post like Instagram with a limit of 60 words
Assign a catchy name to this post
Provide the output in JSON structure like this {"1": "<name>", "2": "<caption>", "3": "<social-post>"}
'''

second_assistant = create_assistant(openai, "Narrative Designer - Post and Fortune Cookie", "Designs posts and fortune cookie messages using user input", second_assistant_instructions)

# Print the IDs of the created assistants
print("First Assistant ID:", first_assistant.id)
print("Second Assistant ID:", second_assistant.id)
