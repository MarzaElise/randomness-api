from fastapi import FastAPI
from Helpers import random_facts
from Helpers import website as web
from fastapi.responses import RedirectResponse
import aiohttp
import random
app = FastAPI(debug=True, title="randomness", description="An api you can use to generate random facts and websites", version="1.0.0")

async def fetch_text():
    async with aiohttp.ClientSession() as ses:
        async with ses.get("https://uselessfacts.jsph.pl/random.json?language=en") as res:
            data = await res.json()
            text = data["text"]
            return text

async def fetch_fact():
    a = []
    for i in range(43):
        async with aiohttp.ClientSession() as ses:
            async with ses.get("https://some-random-api.ml/facts/cat") as res:
                data = await res.json()
                try:
                    fact = data["fact"]
                    a.append(fact)
                except KeyError:
                    return a
    return a

async def get_lis():
    lis = []
    for i in range(30):
        text = await fetch_text()
        facts = await fetch_fact()
        lis.append(text)
        lis.extend(facts)
    for text in lis:
        random_facts.append(text)
    return random_facts

@app.get("/")
async def home():
    '''Home page of the API this will redirect to the /docs page since i dont want to do shit for the home page'''
    return RedirectResponse("/redoc")

@app.get("/fact")
async def fact():
    '''Generate a random fact. More facts will be added very soon'''
    facts = await get_lis()
    fact = random.choice(facts)
    index = facts.index(fact)
    total = len(random_facts) - 1
    return {"fact" : fact, "index" : index, "total" : total}

@app.get("/website")
async def website():
    '''Generate one random useless but somewhat interesting website from a total of 200+ website links'''
    e = random.choice(web)
    a = web.index(e)
    total = len(web) - 1
    return {"website" : e, "index" : a, "total" : total}
