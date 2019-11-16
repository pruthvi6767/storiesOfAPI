
#!/usr/bin/env python3
import time
import sys
import urllib3
from http.client import HTTPSConnection
import json
from concurrent.futures import ThreadPoolExecutor
import logging


# logs = logging.getLogger()
# logs.level = logging.DEBUG
# logs.addHandler(logging.StreamHandler(stream=sys.stdout))


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
people = []
# connection pool
# Timeouts been discarded and  wait for complete responses
conn = urllib3.PoolManager(20)


def get_ships_and_planets_for_person(person):
    """
    performs almost same  to synchronous version on my device = 34 sec
    """
    with ThreadPoolExecutor(max_workers=10) as executor:
        try:
            if person["starships"]:
                person["starships"] = [starship["name"] for starship in list(
                    executor.map(get_starwars_data, person['starships']))]
            if person["homeworld"]:
                # person["home"] = get_starwars_data(person["homeworld"])

                future_response = executor.submit(
                    get_starwars_data, person["homeworld"])
                person["homeworld"] = future_response.result()["name"]
        except Exception as e:
            print(e)
            #logs.log(logging.INFO, e)
        executor.shutdown(wait=True)
        return {"name": person["name"], "homeworld": person["homeworld"],
                "starships": person["starships"]
                }


def get_starwars_data(url):
    try:
        response = conn.request('GET', url, headers={
            "Content-Type": "Application/JSON"}, timeout=60)
        if response.status == 200:
            data = json.loads(response.data.decode('utf-8'))
            return data
    except Exception as e:
        print("Error reading from {} ".format(url))
        #logs.log(logging.INFO, e)


def main(start_url):
    while start_url:
        people_response = get_starwars_data(start_url)
        # with ThreadPoolExecutor here was not performing well = 0.55 sec
        # with ThreadPoolExecutor(max_workers=10) as executor:
        people.extend(
            list(map(get_ships_and_planets_for_person,
                     people_response['results'])))
        if people_response['next'] is not None:
            start_url = people_response['next']
        else:
            print(time.process_time())
            print(people)
            print(len(people))
            print(f"end at {time.strftime('%X')}")
            sys.exit(0)


if __name__ == '__main__':
    start_url = 'https://swapi.co/api/people/'
    print(f"started at {time.strftime('%X')}")
    main(start_url)
