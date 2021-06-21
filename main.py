from fastapi import FastAPI, Request, Response
from Helpers import random_facts
from Helpers import website as web
from fastapi.responses import RedirectResponse
import aiohttp
import random
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(debug=True, title="randomness", description="An api you can use to generate random facts and websites", version="1.0.0")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

async def fetch_text():
    async with aiohttp.ClientSession() as ses:
        async with ses.get("https://uselessfacts.jsph.pl/random.json?language=en") as res:
            data = await res.json()
            text = data["text"]
            return text

async def fetch_fact():
    async with aiohttp.ClientSession() as ses:
        async with ses.get("https://some-random-api.ml/facts/cat") as res:
            data = await res.json()
            try:
                fact = data["fact"]
            except KeyError:
                return None
            else:
                return fact

async def get_lis():
    lis = []
    for i in range(30):
        try:
            text = await fetch_text()
        except:
            continue
        else:
            lis.append(text)
    for i in range(40):
        fact = await fetch_fact()
        if fact:
            lis.append(fact)
    random_facts.extend(lis)
    return random_facts

@app.get("/")
async def home():
    '''Home page of the API this will redirect to the /docs page since i dont want to do shit for the home page'''
    return RedirectResponse("/docs")

@app.get("/fact")
@limiter.limit("180/minute")
async def fact(request : Request):
    '''Generate a random fact. More facts will be added very soon'''
    return {"fact" : "Fun Fact: the fact endpoint is dead until i find a way to not get rate limitted"}
    # facts = await get_lis()
    # fact = random.choice(facts)
    # index = facts.index(fact)
    # total = len(random_facts) - 1
    # return {"fact" : fact, "index" : index, "total" : total}

@app.get("/website")
@limiter.limit("180/minute", error_message="You Have Hit the rate limit of 180 requests per minute. Try again Later")
async def website(request : Request, respone : Response):
    '''Generate one random useless but somewhat interesting website from a total of 200+ website links'''
    e = random.choice(web)
    a = web.index(e)
    total = len(web) - 1
    return {"website" : e, "index" : a, "total" : total}
