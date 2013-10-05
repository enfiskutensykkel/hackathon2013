# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
from flask import jsonify

from calais import find_quotations_in_text

from storyful import search_storyful
from afp import search_afp_after_person

app = Flask(__name__)


text = """
Foreign military forces appear to have carried out a pre-dawn raid on a southern Somalian coastal town, apparently in pursuit of "a high-profile target" linked to the militant al-Shabaab group that was behind last month's Kenyan mall shootings.

The pre-dawn raid – which initial but unconfirmed reports suggested may have involved US troops – took place in Barawe, in the lower Shabelle region 240km south of Mogadishu. It is the same town where US navy commandos killed a senior al-Qaida member four years ago.

The raid comes as Kenya's military confirmed the names of four al-Shabaab fighters implicated in the Westgate attack. Major Emmanuel Chirchir said the men were Abu Baara al-Sudani, Omar Nabhan, Khattab al-Kene and Umayr – names that were first broadcast by a local Kenyan television station.

"I confirm those are the names of the terrorist," he said, in a tweet sent to the Associated Press.

The publication of the identities supports CCTV footage from the Nairobi mall published by a private TV station that shows no more than four attackers, contradicting earlier government statements that between 10 to 15 attackers were involved.
"""


# Generator for searching in storyful API
def storyful(name):
    for story in search_storyful(name):
        if 'summary' in story:
            yield {
                'title': None,
                'summary': story['summary'],
                'text': story['summary'],
                'metadata': None,
                'href': story['html_resource_url'],
                'source': 'storyful'
            }


# Generator for searching in AFP API
def afp(name):
    for paragraphs, metadata in search_afp_after_person(name):
        yield {
            'title': None,
            'summary': None,
            'text': '\n'.join(paragraphs),
            'metadata': metadata,
            'href': None,
            'source': 'afp'
        }


# Aggregate the generators
def search_name(name):
    def aggregator(generators):
        i = 0
        max_results = 30
        while max_results:
            max_results -= 1
            try:
                i = (i + 1) % len(generators)
                yield generators[i].next()
            except StopIteration:
                del generators[i]
                if len(generators) == 0:
                    break

    return aggregator([afp(name), storyful(name)])


def search_for_person(name, page):
    data = []

    context_list = []

    max_calais_request_size = 32768
    max_results = 20

    def send_to_calais():
        for name, quote, offset in find_quotations_in_text(text, html=True):
            for context in context_list:
                if context['begin'] <= offset < context['end']:
                    data.append({
                        'who': name,
                        'quote': quote,
                        'headline': context['title'],
                        'source': context['source'],
                        'url': context['url'],
                        'date': "2013-10-05",
                        'people': "John Kerry; Liu Xiaobo",
                        'tags': "Asia;US;shutdown"
                    })
                    break
            else:
                print "No match found!"

    text = ""
    for story in search_name(name):
        if max_results <= 0: break
        max_results -= 1

        old_length = len(text)
        new_length = old_length + len(story['text'])

        if new_length > max_calais_request_size:
            send_to_calais()

            text = ""
            old_length = 0
            new_length = len(story['text'])

        context = {
            'title': story['title'],
            'source': story['source'],
            'url': story['href'],
            'begin': old_length,
            'end': new_length
        }

        text += story['text']
        context['end'] = len(text)
        context_list.append(context)

    if text:
        send_to_calais()

    return dict(
        data=data,
        next=None
    )


@app.route("/persons/<name>/")
def persons_first_page(name):
    return jsonify(search_for_person(name, 0))
    #return jsonify(get_storyful_data(name))


@app.route("/persons/<name>/<int:page>")
def persons_page(name, page):
    return jsonify(search_for_person(name, page))


if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True)
