import urllib2
import json

api_key='hackday2013'

def get_guardian_data(search_term, per_page=10, page_index=1):
	#url = "http://api.storyful.com/tags/" + tag + "/stories?access_token=" + api_key
	url = "http://content.guardianapis.com/search?q=" + str(search_term) + "&page=" + str(page_index) + \
			"&page-size=" + str(per_page) +  "&show-fields=all&show-snippets=all&api-key=" + api_key

	data = json.loads(urllib2.urlopen(url).read())

	return data['response']

def get_total_stories(data):
	# find out how many stories in total were found for this search term
	return data['total']

def get_total_pages(data):
	# find out how many pages in total were found for this search term
	return data['pages']

def get_current_page(data):
	# index of current page
	return data['currentPage']

def get_stories(data):
	# return array of stories
	return data['results']

def get_story_summmary(story):
	return story['snippets']['body']

def get_story_text(story):
	return story['fields']['body']

def get_story_url(story):
	return story['webUrl']

def get_story_title(story):
	return story['fields']['headline']

def get_story_published_datetime(story):
	return story['webPublicationDate']

if __name__ == '__main__':

	# example
	search_term = "Obama"

	data = get_guardian_data(search_term)
	print get_total_stories(data)