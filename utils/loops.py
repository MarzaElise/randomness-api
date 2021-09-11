"""
discord.ext.tasks stuff that loop through API_URLS and add it to the random_facts list
"""

from discord.ext import tasks
import asyncio
import aiohttp
from .helpers import random_facts

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


@tasks.loop(minutes=1)
async def useless_fact():
    """Get some facts and append it to the random_facts list"""
    f = await fetch_from(
        "https://uselessfacts.jsph.pl/random.json?language=en", "text"
    )
    random_facts.append(f)
    print(f"Appended to list - useless : total -> {len(random_facts)}")
    return None


@tasks.loop(minutes=1)
async def cat():
    """Extend the random_facts list using some-random-api cat endpoint"""
    f = await fetch_from("https://some-random-api.ml/facts/cat", "fact")
    random_facts.append(f)
    print(f"Appended to list - cat : total -> {len(random_facts)}")
    return None


@tasks.loop(minutes=1)
async def dog_fact():
    """Dog facts from some-random-api.ml dog endpoint"""
    f = await fetch_from("https://some-random-api.ml/facts/dog", "fact")
    random_facts.append(f)
    print(f"Appended to list - dog : total -> {len(random_facts)}")
    return None


@tasks.loop(minutes=1)
async def panda():
    """https://some-random-api.ml/facts Panda endpoint"""
    f = await fetch_from("https://some-random-api.ml/facts/panda", "fact")
    random_facts.append(f)
    print(f"Appended to list - panda : total -> {len(random_facts)}")
    return None


async def hourly():
    for URL, KEY in API_URLS:
        f = await fetch_from(URL, KEY)
        random_facts.append(f)
    print(f"Hourly appending - all : total -> {len(random_facts)}")
    return None


@tasks.loop(hours=1)
async def every_hour():
    """The task that is looped every hour"""
    for _ in range(30):
        try:
            await hourly()
        except:
            await asyncio.sleep(60 * 10)


@tasks.loop(hours=24)
async def daily():
    for _ in range(30):
        try:
            await hourly()
        except:
            await asyncio.sleep(60 * 10)
