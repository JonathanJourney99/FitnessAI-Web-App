import os
import json
from flask import Flask, render_template, request, redirect, url_for
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv, find_dotenv
from datetime import datetime

app = Flask(__name__)

load_dotenv(find_dotenv(), override=True)
openai_api_key = os.getenv("OPENAI_API_KEY")

llm = OpenAI(openai_api_key=openai_api_key, temperature=0.7)

def track_progress_chain(current_weight, goal_weight):
    prompt_template = """
    You are a fitness assistant. A user currently weighs {current_weight} kg and their goal is to reach {goal_weight} kg.
    Provide an update on their fitness progress. Include an estimate of how far along they are towards their goal, 
    any relevant advice for speeding up progress, and some motivating words to encourage the user.
    Be specific and include percentages where possible.
    """
    prompt = PromptTemplate(template=prompt_template, input_variables=["current_weight", "goal_weight"])
    progress_chain = LLMChain(llm=llm, prompt=prompt)
    return progress_chain.run(current_weight=current_weight, goal_weight=goal_weight)


def generate_meal_plan_chain(calories):
    prompt_template = """
    You are a nutritionist. A user has a goal of consuming {calories} calories per day. 
    Generate a detailed 1-day meal plan that is affordable, healthy, and balanced.
    Include 3 meals and 2 snacks per day. For each meal and snack, list the ingredients and approximate portion sizes.
    Also, ensure that the meals are easy to prepare, and take into consideration a balance of macronutrients (proteins, fats, and carbohydrates).
    """
    prompt = PromptTemplate(template=prompt_template, input_variables=["calories"])
    meal_plan_chain = LLMChain(llm=llm, prompt=prompt)
    return meal_plan_chain.run(calories=calories)


def generate_workout_plan_chain(fitness_level, height):
    prompt_template = """
    You are a fitness trainer.Create a plan for 1 whole day. A user with a {fitness_level} fitness level and height of {height} cm needs a full 7-day workout plan.
    The plan should include strength, flexibility, and endurance exercises for each day, with detailed instructions for each exercise (sets, reps, and duration).
    Make sure to include rest days and mention the type of workouts suitable for the user's fitness level.
    Also, include variations for users who may not have access to gym equipment.
    """
    prompt = PromptTemplate(template=prompt_template, input_variables=["fitness_level", "height"])
    workout_plan_chain = LLMChain(llm=llm, prompt=prompt)
    return workout_plan_chain.run(fitness_level=fitness_level, height=height)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ai', methods=['GET', 'POST'])
def ai():
    if request.method == 'POST':
        current_weight = float(request.form['currentWeight'])
        goal_weight = float(request.form['goalWeight'])
        calories = int(request.form['calorieGoal'])
        fitness_level = request.form['fitnessLevel']
        height = float(request.form['height'])  # New field for height

        progress = track_progress_chain(current_weight, goal_weight)
        meal_plan = generate_meal_plan_chain(calories)
        workout_plan = generate_workout_plan_chain(fitness_level, height)

        progress_date = datetime.now().strftime('%Y-%m-%d')
        with open('progress_tracking.txt', 'a') as f:
            f.write(f"{progress_date}: {current_weight} kg - {progress}\n")

        return render_template('result.html', progress=progress, meal_plan=meal_plan, workout_plan=workout_plan)

    return render_template('model.html')

if __name__ == "__main__":
    app.run(debug=True)
