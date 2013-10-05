import urllib2
from urllib import quote
import re
import xml.etree.ElementTree as ET

base_url = 'http://www.ipadafp.afp.com/afp-wanifra'


def get_entities(data):
    tree = ET.fromstring(data)
    metadata = tree.findall('NewsItem/NewsComponent/NewsComponent/Metadata')

    metadataMap = {}
    for m in metadata:
        for field in m.findall('Property'):
            mtype = field.get('FormalName')
            value = field.get('Value')

            if not mtype in metadataMap:
                metadataMap[mtype] = []

            metadataMap[mtype].append(value)

    return metadataMap


def get_content(data):
    tree = ET.fromstring(data)
    content = tree.findall('NewsItem/NewsComponent/NewsComponent/ContentItem/DataContent/p')
    return [p.text for p in content]


def get_relevant_data(who, max_results=30):
    data = urllib2.urlopen(base_url + '?%s=%s&rows=%d' % ('who_pers', quote(who), max_results)).read()
    refs = re.findall(r'<NewsItemRef\s+Duid="([^"]*)"\s+NewsItem="([^"]*)"\s*/>', data)

    for ref, url in refs:
        data = urllib2.urlopen(url).read()

        metadata = get_entities(data)
        content = get_content(data)

        yield content, metadata


if __name__ == '__main__':
    # Example how to use this module
    for paragraphs, metadata in get_relevant_data("Barack Obama"):
        print paragraphs
        print metadata