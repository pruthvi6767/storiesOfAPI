#!/usr/bin/env python3
import sys
import json
import asyncio
import time
import logging
import aiohttp.client as async_http_client


# logs = logging.getLogger()
# logs.level = logging.DEBUG
# logs.addHandler(logging.StreamHandler(stream=sys.stdout))


class MyError(Exception):
    def __init__(self, msg):
        self.msg = msg
        super()


people = []
tasks = []


async def get_ships_and_planets_for_person(people_res):
    """
     perform async person dict processing
    """
    for person in people_res:
        starships, homeworld = [], ''
        #print("before strship")
        if person["starships"]:
            starships = await get_urls_name(person["starships"])
            starships = [starship["name"] for starship in starships]
        #print("awaited starship")
        # print(person["starships"])
        if person["homeworld"]:
            homeworld = await get_urls_name(person["homeworld"])
        #print("awaited homewrold")
        # print(person)
        people.append({"name": person["name"], "homeworld":  homeworld["name"],
                       "starships":  starships
                       })


async def get_starwars_data(url):
    try:

        async with async_http_client.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise MyError(msg="error-custom")
    except Exception as e:
        print("Error reading from {} ".format(url))
        #logs.log(logging.INFO, e)


async def main(start_url):
    while start_url:

        people_res = await get_starwars_data(start_url)

        person = asyncio.create_task(
            get_ships_and_planets_for_person(people_res['results']))
        tasks.append(person)

        if people_res['next'] is not None:
            start_url = people_res['next']
        else:
            await asyncio.gather(*tasks)
            print(time.process_time())
            print(people)
            print(len(people))
            print(f"end at {time.strftime('%X')}")
            sys.exit(0)


def extend_people_result(person):
    people.extend(person)


async def get_urls_name(urls) -> list:
    # urls = ['https://swapi.co/api/people/1', 'https://swapi.co/api/people/2',
    #         'https://swapi.co/api/people/3', 'https://swapi.co/api/people/4', 'https://swapi.co/api/people/5']
    if isinstance(urls, list):
        for i, uri in enumerate(urls):
            uri = await get_starwars_data(uri)
            urls[i] = uri
        # urls = [uri["name"] for uri in urls]
    else:
        urls = await get_starwars_data(urls)

    return urls


if __name__ == '__main__':
    start_url = 'https://swapi.co/api/people/'
    print(f"started at {time.strftime('%X')}")
    main = asyncio.run(main(start_url))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main)
