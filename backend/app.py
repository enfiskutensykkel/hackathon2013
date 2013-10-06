# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
from flask import jsonify

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
                'published_at': story['published_at']
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
            'published_at': date.isoformat()
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
        semantics = get_semantic_data(text)

        for context in context_list: # This iterates over articles
            persons = []
            for name, offsets in semantics['persons']:
                for offset in offsets:
                    if context['begin'] <= offset < context['end']:
                        persons.append(name)
                        break

            topics = []
            for name, offsets in semantics['topics']:
                for offset in offsets:
                    if context['begin'] <= offset < context['end']:
                        topics.append(name)
                        break

            for name, quote, offsets in semantics['quotes']:
                for offset in offsets:
                    if context['begin'] <= offset < context['end']:
                        data.append({
                            'who': name,
                            'quote': quote,
                            'headline': context['title'],
                            'source': context['source'],
                            'url': context['url'],
                            'date': "2013-10-05",
                            'people': persons,
                            'tags': topics
                        })
                        break

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
