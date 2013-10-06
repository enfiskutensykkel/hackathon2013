# -*- coding: utf-8 -*-

from flask import Flask
from flask import jsonify
import datetime as dt
from calendar import timegm as timestamp

from calais import get_semantic_data
from generator import PeekableGenerator

from storyful import search_storyful
from afp import search_afp
from guardian import search_guardian

app = Flask(__name__)


# Generator for searching in storyful API
def storyful(name):
    for story in search_storyful(name):
        if 'summary' in story:
            yield {
                'title': story['title_clean'],
                'summary': story['summary'],
                'text': story['summary'],
                'metadata': None,
                'href': story['html_resource_url'],
                'source': 'storyful',
                'thumbnail': None,
                'published_at': dt.datetime.strptime(story['published_at'], '%Y-%m-%dT%H:%M:%SZ')
            }


# Generator for searching in AFP API
def afp(name):
    for url, date, title, summary, paragraphs, metadata, image in search_afp(name):
        yield {
            'title': title,
            'summary': summary,
            'text': '\n'.join(paragraphs),
            'metadata': metadata,
            'href': url,
            'source': 'afp',
            'thumbnail': image,
            'published_at': date
        }


# Generator for searching in guardian API
def guardian(name):
    for story in search_guardian(name):
        yield {
            'title': story['fields']['headline'],
            'summary': story['snippets']['body'] if 'body' in story['snippets'] else None,
            'text': story['fields']['body'],
            'metadata': None,
            'href': story['webUrl'],
            'source': 'guardian',
            'thumbnail': None,
            'published_at': dt.datetime.strptime(story['webPublicationDate'], '%Y-%m-%dT%H:%M:%SZ')
        }


# Aggregate the generators
def search_name(name):

    # Merges one or more peekable generators
    # does a merge sort on most recent date
    def aggregator(*generators):
        latest = 0

        # initial state
        for i in xrange(0, len(generators)):
            if generators[i].hasMore():
                latest = i
                break

        while 1:
            # merge sort
            for i in xrange(1, len(generators)):
                if generators[i].hasMore() and generators[i].peek()['published_at'] > generators[latest].peek()['published_at']:
                    latest = i

            yield generators[latest].next()

    return aggregator(
        PeekableGenerator(afp(name)),
        PeekableGenerator(guardian(name)),
        PeekableGenerator(storyful(name))
    )


def search_for_person(name, page):
    context_list = []

    max_calais_request_size = 32768
    max_results = 10

    for story in search_name(name):
        if max_results <= 0:
            break
        max_results -= 1

        story_text = story['text'][0:max_calais_request_size]

        context = {
            'title': story['title'],
            'source': story['source'],
            'url': story['href'],
            'thumb': story['thumbnail'],
            'date': story['published_at']
        }

        context_list.append(context)

        semantics = get_semantic_data(story_text)

        for context in context_list: # This iterates over articles
            persons = []
            for name in semantics['persons']:
                persons.append(name)

            topics = []
            for name in semantics['topics']:
                topics.append(name)

            for name, quote in semantics['quotes']:
                yield {
                    'who': name,
                    'quote': quote,
                    'headline': context['title'],
                    'source': context['source'],
                    'url': context['url'],
                    'date': timestamp(context['date'].utctimetuple()),
                    'people': persons,
                    'thumbnail': context['thumb'],
                    'tags': topics
                }


def get_person_page(name, page):
    return {
        'data': [x for x in search_for_person(name, page)],
        'next': None
    }

@app.route("/persons/<name>/")
def persons_first_page(name):
    return jsonify(get_person_page(name, 0))


@app.route("/persons/<name>/<int:page>")
def persons_page(name, page):
    return jsonify(get_person_page(name, page))


if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True)
