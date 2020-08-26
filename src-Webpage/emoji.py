# Written by Max Flander, adapted by Peter Amerkhanian
# This file uses the pre-existing council jsons

import json
import re
import datetime
from typing import Tuple, List, Union

def parse_timestamp(ts: str) -> str:
    # Used to parse the timestamp for each meeting
    year, month, day = ts[:10].split('-')
    return f"{month}/{day}/{year}"


def read_topics(filename: str) -> dict:
    # Used to turn the topics.tsv into a dict object
    with open(filename, encoding ='utf-8') as f:
        data = f.read()

    rows = data.split('\n')[1:-1]
    keyword_map = {}
    for row in rows:
        topic, keywords, emoji = row.split('\t')
        for keyword in keywords.split(','):
            keyword_map[keyword] = {'topic': topic, 'emoji': emoji}

    return keyword_map


def get_topics(meeting: dict, keyword_map: dict) -> Tuple[str, str]:
    # Returns a tuple (topics, emojis) for a given meeting
    topics = set()   # Tells this is an Oakland meeting
    topics.add("#oakmtg ")
    emojis = set()
    print(meeting['EventDate'])
    agenda = meeting['EventBodyName'] + " " +  " ".join(a['EventItemTitle'] or '' for a in meeting['EventAgenda'])
    for k, v in keyword_map.items():
        if re.search('\\b' + k + '\\b', agenda, re.IGNORECASE):
            # topics.add("#" + v['topic'].replace(' ', ''))
            topics.add("#" + v['topic'].replace(' ', '') + " ")  # HSM adding a space afterwards
            emojis.add(v['emoji'])

    return ''.join(topics), ''.join(emojis)


def twitter_read_json(file: Union[List[dict], str], printit: bool=False) -> List[dict]:
    # Puts it all together to read either a list or str object
    # If str obj, then 
    if type(file) == str:
        with open(file) as f:
            meetings = json.load(f)
    else:
        meetings = file
    topics = read_topics(r'C:\Users\Peter\Documents\Projects\councilmatic\src-Tweeter\topics.tsv')

    # print(type(meetings))
    csv = [[m['EventBodyName'],
            parse_timestamp(m['EventDate']),
            m['EventTime'],
            m['EventAgendaFile'] or ''] + list(get_topics(m, topics))
         for m in meetings]

    if printit:
        for m in csv:
            print('\n'.join(m))
    
    return csv


def test() -> None:
    filename = r"C:\Users\Peter\Documents\Projects\Councilmatic\councilmatic\WebPage\website\scraped\Scraper2020.json"
    schedule = twitter_read_json(filename, False)
    print(schedule)

# If you run this file you are just running a test
if __name__ == "__main__":
    test()