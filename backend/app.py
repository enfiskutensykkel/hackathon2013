# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
from flask import jsonify
import datetime as dt

from generator import PeekableGenerator
from calais import find_quotations_in_text

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
                'published_at': dt.datetime.strptime(story['published_at'], '%Y-%m-%dT%H:%M:%SZ')
            }


# Generator for searching in AFP API
def afp(name):
    for url, date, title, summary, paragraphs, metadata in search_afp(name):
        yield {
            'title': title,
            'summary': summary,
            'text': '\n'.join(paragraphs),
            'metadata': metadata,
            'href': url,
            'source': 'afp',
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
            'published_at': dt.datetime.strptime(story['webPublicationDate'], '%Y-%m-%dT%H:%M:%SZ')
        }


# Aggregate the generators
def search_name(name):
    def aggregator(generators):
        lowest = 0

        # initial state
        for i in xrange(0, len(generators)):
            if generators[i].hasMore():
                lowest = i
                break

        while 1:
            # merge sort
            for i in xrange(1, len(generators)):
                if generators[i].hasMore() and generators[i].peek()['published_at'] > generators[lowest].peek()['published_at']:
                    lowest = i

            yield generators[lowest].next()

    return aggregator([
        PeekableGenerator(afp(name)),
        PeekableGenerator(guardian(name)),
        PeekableGenerator(storyful(name))
    ])


def search_for_person(name, page):
    data = []

    context_list = []

    max_calais_request_size = 32768
    max_results = 40

    def send_to_calais():
        for name, quote, offset in find_quotations_in_text(text, html=False):
            for context in context_list:
                if context['begin'] <= offset < context['end']:
                    data.append({
                        'who': name,
                        'quote': quote,
                        'headline': context['title'],
                        'source': context['source'],
                        'url': context['url'],
                        'date': context['date'].strftime('%Y-%m-%dT%H:%M:%SZ'),
                        'people': "John Kerry; Liu Xiaobo",
                        'tags': "Asia;US;shutdown"
                    })
                    break
            else:
                print "No match found!"

    text = ""
    for story in search_name(name):
        if max_results <= 0:
            break
        max_results -= 1

        story_text = story['text'][0:max_calais_request_size]

        old_length = len(text)
        new_length = old_length + len(story_text)

        if new_length > max_calais_request_size:
            send_to_calais()

            text = ""
            old_length = 0
            new_length = len(story_text)
            context_list = []

        context = {
            'title': story['title'],
            'source': story['source'],
            'url': story['href'],
            'date': story['published_at'],
            'begin': old_length,
            'end': new_length
        }
        text += story_text
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


@app.route("/persons/<name>/<int:page>")
def persons_page(name, page):
    return jsonify(search_for_person(name, page))


if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True)
