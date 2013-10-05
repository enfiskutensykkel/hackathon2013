# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
from flask import jsonify

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
                'published_at': story['published_at']
            }


# Generator for searching in AFP API
def afp(name):
    for url, title, summary, paragraphs, metadata in search_afp(name):
        yield {
            'title': title,
            'summary': summary,
            'text': '\n'.join(paragraphs),
            'metadata': metadata,
            'href': url,
            'source': 'afp',
            'published_at': None
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
            'published_at': story['webPublicationDate']
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

    return aggregator([afp(name), guardian(name), storyful(name)])


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
