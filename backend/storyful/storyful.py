import urllib2
import json
import datetime as dt

#api_key='d8e893d2958d15c7807b412f72f30ce8'

def get_storyful_data(tag, per_page=10):
    #url = "http://api.storyful.com/tags/" + tag + "/stories?access_token=" + api_key
    url = "http://api.storyful.com/tags/" + urllib2.quote(tag) + "/stories?per_page=" + str(per_page)

    data = json.loads(urllib2.urlopen(url).read())

    return data


def get_total_stories(data):
    # find out how many stories in total were found for this tag
    return data['total_items']


def get_stories(data):
    # return array of stories
    return data['tag']['stories']


def get_story_summmary(story):
    return story['summary']


def get_story_url(story):
    return story['html_resource_url']


def get_story_title(story):
    return story['title_clean']


def get_story_title_date(story):
    return story['title_date']


def get_story_published_datetime(story):
    return story['published_at']


def get_story_tags(story):
    return story['tags']


def search_storyful(tag, max_results=30):
    per_page = 10

    url = "http://api.storyful.com/tags/" + urllib2.quote(tag) + "/stories?per_page=" + str(per_page)
    while url is not None:
        request = urllib2.Request(url)
        try:
            data = json.loads(urllib2.urlopen(request).read())
        except urllib2.HTTPError:
            return

        url = data['next']
        stories = data['tag']['stories']

        for item in stories:
            yield item


if __name__ == '__main__':
    # example
    tag = "barack%20obama"

    data = get_storyful_data(tag)
    print data