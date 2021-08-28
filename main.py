import json
import random

import aiohttp
from fastapi import (FastAPI, Request, Response,
                     status)
from fastapi.responses import RedirectResponse
from utils.helpers import random_facts
from utils.helpers import website as web
from utils.loops import cat, dog_fact, panda, useless_fact
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

limiter = Limiter(
    key_func=get_remote_address, headers_enabled=True, retry_after=3
)
app = FastAPI(
    debug=True,
    title="randomness",
    description="An api you can use to generate random facts and websites",
    version="1.0.2",
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.on_event("startup")
async def on_startup():
    """
    Startup event that is triggered when the app is starting to run
    """
    # useless_fact.start()
    # cat.start()
    # dog_fact.start()
    # panda.start()
    print("Server Started Succesfully")
    print("\n\nhttps://randomness-api.herokuapp.com\nhttp://127.0.0.1:8000\n\n")


@app.get("/", include_in_schema=False)
async def home():
    """
    Home page of the API. this will redirect to the /docs page since i dont want to do shit for the home page
    """
    return RedirectResponse("/docs")


@app.get("/fact")
@limiter.limit("3/second")
async def fact(request: Request, response: Response):
    """
    Generate a random fact.
    Ratelimit: 3 requests per second
    """
    fact = random.choice(random_facts)
    index = random_facts.index(fact)
    total = len(random_facts) - 1
    return {"fact": fact, "index": index, "total": total}


@app.get("/website")
@limiter.limit("3/second")
async def website(request: Request, response: Response):
    """
    Generate one random useless but somewhat interesting website from a total of 70+ website links
    Ratelimit: 3 requests per second
    """
    e = random.choice(web)
    a = web.index(e)
    total = len(web) - 1
    return {"website": e, "index": a, "total": total}
