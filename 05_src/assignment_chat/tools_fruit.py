from langchain.tools import tool
import json
import requests
import os
from utils.logger import get_logger
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
_logs = get_logger(__name__)



"""
class FruitFact(BaseModel):
    name: str
    genus: str
    protein: int
    fat: float
    calories: int
    family: str
    sugar: float
    order: str
"""
    
@tool
def get_fruit_facts(fruit="Durian"):
    """
    Returns the family and genus of a fruit
    """
    url = f'https://www.fruityvice.com/api/fruit/{fruit}'
    # API doesn't use parameter
    response = requests.get(url)
    _logs.debug(response)

    resp_dict = json.loads(response.text)
    fruit_family = resp_dict.get("family", "No fruit entry found.")
    genus = resp_dict.get("genus", "No fruit entry found.")
    fruit_facts = f"Fruit: {fruit.capitalize()} Family: {fruit_family} Genus: {genus}"
    return fruit_facts

@tool
def get_recipe(food):
    """
    Gets a recipe for a fruit
    """
    load_dotenv(".env")
    load_dotenv(".secrets")

    API_GATEWAY_KEY = os.getenv('API_GATEWAY_KEY')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    client = OpenAI(base_url='https://k7uffyg03f.execute-api.us-east-1.amazonaws.com/prod/openai/v1', 
                api_key='any value',
                default_headers={"x-api-key": os.getenv('API_GATEWAY_KEY')})

    response = client.responses.create(
        model='gpt-4o-mini',
        tools=[
        { type: "web_search" },
        ],
        input= 'Give one recipe with this ingredient: ${food}',
    )
    recipe=response.message.content[0].text
    url=response.content[0].annotations
    ret_recipe = f"*** Recipe as follows: {recipe}\n\n From the website(s): {url}"
    _logs.debug(ret_recipe)
    return recipe

