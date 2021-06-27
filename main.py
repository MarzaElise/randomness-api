import asyncio
import random
import traceback

import aiohttp
import uvicorn
from discord.ext import tasks
from fastapi import (Depends, FastAPI, HTTPException, Request, Response,
                     Security, status)
from fastapi.responses import RedirectResponse
from fastapi.security import APIKeyHeader
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from helpers import random_facts
from helpers import website as web
from loops import cat, dog_fact, panda, useless_fact

limiter = Limiter(key_func=get_remote_address,
                  headers_enabled=True, retry_after=3)
app = FastAPI(debug=True, title="randomness",
              description="An api you can use to generate random facts and websites", version="1.0.0a")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

X_API_KEY = APIKeyHeader(name="x-api-key")

async def is_key_valid(api_key : str = Depends(X_API_KEY)):
    if api_key == "123":
        return True
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")

API_URLS = [
    ("https://uselessfacts.jsph.pl/random.json?language=en", "text"),
    ("https://some-random-api.ml/facts/cat", "fact"),
    ("https://some-random-api.ml/facts/dog", "fact"),
    ("https://some-random-api.ml/facts/panda", "fact"),
]


async def fetch_from(url: str, key: str):
    async with aiohttp.ClientSession() as ses:
        async with ses.get(url) as res:
            try:
                await res.json()
            except:
                await asyncio.sleep(60 * 10)
            else:
                try:
                    data = await res.json()
                    data[key]
                except Exception as e:
                    await asyncio.sleep(60 * 10)
                else:
                    data = await res.json()
                    fact = data[key]
    return fact


@app.on_event("startup")
async def on_startup():
    '''Startup event that is triggered when the app is starting to run'''
    # useless_fact.start()
    # cat.start()
    # dog_fact.start()
    # panda.start()
    print("Server Started Succesfully")
    print("\n\nhttps://randomness-api.herokuapp.com\nhttp://127.0.0.1:8000\n")


@app.get("/")
async def home():
    '''
    Home page of the API. this will redirect to the /docs page since i dont want to do shit for the home page
    '''
    return RedirectResponse("/docs")


@app.get("/fact", dependencies=[Security(is_key_valid)])
@limiter.limit("3/minute")
async def fact(request: Request, response: Response):
    '''
    Generate a random fact. More facts will be added very soon
    Ratelimit: 3 requests per second
    '''
    # return {"fact" : "Fun Fact: the fact endpoint is dead until i find a way to not get rate limitted"}
    fact = random.choice(random_facts)
    index = random_facts.index(fact)
    total = len(random_facts) - 1
    return {"fact": fact, "index": index, "total": total}


@app.get("/website", dependencies=[Security(is_key_valid)])
@limiter.limit("3/second")
async def website(request: Request, response: Response):
    '''
    Generate one random useless but somewhat interesting website from a total of 70+ website links
    Ratelimit: 3 requests per second
    '''
    e = random.choice(web)
    a = web.index(e)
    total = len(web) - 1
    return {"website": e, "index": a, "total": total}
