from fastapi import FastAPI, Request, Response
import traceback
import asyncio
from discord.ext import tasks
from helpers import website as web
from helpers import random_facts
# from ..helpers import website as web
# from ..helpers import random_facts
from fastapi.responses import RedirectResponse
import aiohttp
import random
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address, headers_enabled=True)
app = FastAPI(debug=True, title="randomness", description="An api you can use to generate random facts and websites", version="1.0.0a")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
# web = helpers.website
# random_facts = helpers.random_facts

@app.on_event("startup")
async def on_startup():
    '''Startup event that is triggered when the app is starting to run'''
    extend_facts_useless.start()
    extend_facts_some.start()
    dog_fact.start()
    panda.start()
    print("Server Started Succesfully")

@app.get("/")
async def home():
    '''Home page of the API this will redirect to the /docs page since i dont want to do shit for the home page'''
    return RedirectResponse("/docs")

@app.get("/fact")
# @limiter.limit("3/second")
async def fact():
    '''Generate a random fact. More facts will be added very soon'''
    # return {"fact" : "Fun Fact: the fact endpoint is dead until i find a way to not get rate limitted"}
    fact = random.choice(random_facts)
    index = random_facts.index(fact)
    total = len(random_facts) - 1
    return {"fact" : fact, "index" : index, "total" : total}

@app.get("/website")
@limiter.limit("3/minute")
async def website(request : Request, response : Response):
    '''Generate one random useless but somewhat interesting website from a total of 70+ website links'''
    e = random.choice(web)
    a = web.index(e)
    total = len(web) - 1
    return {"website" : e, "index" : a, "total" : total}


@tasks.loop(minutes=1)
async def extend_facts_useless():
    '''Get some facts and append it to the random_facts list'''
    async with aiohttp.ClientSession() as ses:
        async with ses.get("https://uselessfacts.jsph.pl/random.json?language=en") as res:
            try:
                await res.json()
            except Exception as e:
                # traceback.print_exception(type(e), e, e.__traceback__)
                await asyncio.sleep(60 * 10)
            else:
                data = await res.json()
                text = data["text"]
                random_facts.append(text)
                print("Appended to list - useless")
                await ses.close()
                # extend_facts_some.start()
    return None

@tasks.loop(minutes=1)
async def extend_facts_some():
    '''Extend the random_facts list using some-random-api cat endpoint'''
    async with aiohttp.ClientSession() as ses:
        async with ses.get("https://some-random-api.ml/facts/cat") as res:
            try:
                await res.json()
            except Exception as e:
                # traceback.print_exception(type(e), e, e.__traceback__)
                await asyncio.sleep(60 * 10)
            else:
                data = await res.json()
                _fact = data["fact"]
                random_facts.append(_fact)
                print("Appended to list - cat")
                await ses.close()
                # dog_fact.start()
    return None

@tasks.loop(minutes=1)
async def dog_fact():
    '''Dog facts from some-random-api.ml dog endpoint'''
    async with aiohttp.ClientSession() as ses:
        async with ses.get("https://some-random-api.ml/facts/dog") as res:
            try:
                await res.json()
            except Exception as e:
                # traceback.print_exception(type(e), e, e.__traceback__)
                await asyncio.sleep(60 * 10)
            else:
                data = await res.json()
                dog = data["fact"]
                random_facts.append(dog)
                print("Appended to list - dog")
                await ses.close()
                # panda.start()
    return None

@tasks.loop(minutes=1)
async def panda():
    '''https://some-random-api.ml/facts Panda endpoint'''
    async with aiohttp.ClientSession() as ses:
        async with ses.get("https://some-random-api.ml/facts/panda") as res:
            try:
                await res.json()
            except Exception as e:
                # traceback.print_exception(type(e), e, e.__traceback__)
                await asyncio.sleep(60 * 10)
            else:
                data = await res.json()
                _fact = data["fact"]
                random_facts.append(_fact)
                print("Appended to list - panda")
                await ses.close()
                # extend_facts_useless.start()
    return None