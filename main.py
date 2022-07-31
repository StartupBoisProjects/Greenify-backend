
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import script
import os

app = FastAPI()

origins = ["*"]

f = open("ENV.txt", 'r')
api_key_gmaps = f.read()
print(api_key_gmaps)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def home(start_location = "Brno Bystrc", end_location="Brno International Airport"):

    response = script.script(start_location, end_location, api_key_gmaps)

    with open('search.json', 'w') as f:
        json.dump(response, f, indent=2)

    return response



