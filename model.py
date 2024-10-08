import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
import os
import json
import keyboard
import streamlit_lottie as st_lottie
import psutil
import time

global progress


def load_lottiefile(filepath: str):
    '''
    to load a Lottie animation file.
    Takes a file path as input and reads the JSON content of the Lottie file.
    Returns the JSON data for the Lottie animation.
    '''
    with open(filepath, 'rb') as f:
        return json.load(f)


if "session_started" not in st.session_state:
    st.session_state.session_started = False

load_dotenv(find_dotenv(), override=True)
# Set OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI model via LangChain
llm = OpenAI(openai_api_key=openai_api_key, temperature=0.7)


# Progress Tracking Chain
def track_progress_chain(current_weight, goal_weight):
    prompt_template = """
    You are a fitness assistant.
    At the end of the content write your Fitness Trainer:  Optimize U
    A user currently weighs {current_weight} kg and their goal is to reach {goal_weight} kg. 
    Provide an update on their fitness progress, including an estimate of how far along they are towards their goal and some motivating words.
    """

    prompt = PromptTemplate(template=prompt_template, input_variables=["current_weight", "goal_weight"])
    progress_chain = LLMChain(llm=llm, prompt=prompt)

    result = progress_chain.run(current_weight=current_weight, goal_weight=goal_weight)
    return result


# Meal Plan Chain
def generate_meal_plan_chain(calories):
    prompt_template = """
You are a nutritionist. A user has a goal of consuming {calories} calories per day. Your task is to generate an affordable and healthy meal plan for 7 days that meets this requirement. Ensure that the meals include breakfast, lunch, dinner, and snacks, while focusing on budget-friendly ingredients.

Meal Plan Overview:

Use common, accessible ingredients that are inexpensive yet nutritious.
Incorporate a variety of foods to ensure a balanced diet.
Aim for meals that can be prepared in bulk or use leftovers creatively to minimize waste and cost.
Weekly Meal Plan:

Week 1:
Day 1:
Breakfast:
Lunch:
Dinner:
Snacks:
Day 2:
Breakfast:
Lunch:
Dinner:
Snacks:
(Continue for all 7 days...)
Week 2:
Day 1:
Breakfast:
Lunch:
Dinner:
Snacks:
Day 2:
Breakfast:
Lunch:
Dinner:
Snacks:
(Continue for all 7 days...)
"""

    prompt = PromptTemplate(template=prompt_template, input_variables=["calories"])
    meal_plan_chain = LLMChain(llm=llm, prompt=prompt)

    result = meal_plan_chain.run(calories=calories)
    return result


# Workout Plan Chain
def generate_workout_plan_chain(fitness_level):
    prompt_template = """
    You are a fitness trainer. A user with a {fitness_level} fitness level needs a workout plan. 
    Create a workout plan for them that includes exercises for strength, flexibility, and endurance.
    """

    prompt = PromptTemplate(template=prompt_template, input_variables=["fitness_level"])
    workout_plan_chain = LLMChain(llm=llm, prompt=prompt)

    result = workout_plan_chain.run(fitness_level=fitness_level)
    return result


# Streamlit App
# start session
# Streamlit App
# start session
st.session_state.started = True

if st.session_state.started:

    cover_pic = load_lottiefile('./lottie/workout.json')
    st.lottie(cover_pic, speed=0.5, reverse=False, loop=True, quality='low', height=200, key='first_animate')

    st.title('OptimizeU')

    # User Input
    goal_weight = st.number_input('Enter your goal weight (kg)', min_value=40.0, max_value=200.0, value=50.0)
    current_weight = st.number_input('Enter your current weight (kg)', min_value=40.0, max_value=200.0, value=75.0)
    calories = st.number_input('Enter your daily calorie intake goal', min_value=1200, max_value=4000, value=2000)
    fitness_level = st.selectbox('Select your fitness level', ['Beginner', 'Intermediate', 'Advanced'])

    # Generate Plans using LangChain
    if st.button('Generate AI Plans'):
        # Progress Tracking with LangChain
        progress = track_progress_chain(current_weight, goal_weight)
        st.header(f'AI Progress Tracking: {progress}')

        # Meal Plan using LangChain
        st.subheader('AI Meal Plan')
        meal_plan = generate_meal_plan_chain(calories)
        st.write(meal_plan)

        # Workout Plan using LangChain
        st.subheader('AI Workout Plan')
        workout_plan = generate_workout_plan_chain(fitness_level)
        st.write(workout_plan)

        # Save the generated progress in session state
        st.session_state.progress = progress

    # Save Progress
    progress_date = datetime.now().strftime('%Y-%m-%d')

    if 'progress' in st.session_state:
        if st.button('Save Progress'):
            with open('progress_tracking.txt', 'a') as f:
                f.write(f"{progress_date}: {current_weight} kg - {st.session_state.progress}\n")
            st.success('Progress saved successfully!')
            with open('progress_tracking.txt', 'r') as file:
                st.markdown('#Your saved Progress: ')
                st.write(file.read())
    else:
        st.warning('Please generate your plans before saving progress.')

    if st.button('Stop'):
        st.markdown('🏃‍♂️Stay Healthly and Fit !!!😊👟')
        st.session_state.started = False
