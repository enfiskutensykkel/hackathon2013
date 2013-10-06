import urllib2
from urllib import quote
import datetime
import xml.etree.ElementTree as ET

base_url = 'http://www.ipadafp.afp.com/afp-wanifra'

# TODO: Geolocation as part of metadata


def get_published_at(data):
    tree = ET.fromstring(data)
    return datetime.datetime.strptime(tree.find('NewsItem/NewsManagement/ThisRevisionCreated').text, '%Y%m%dT%H%M%SZ')


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

    summary = None
    for node in tree.findall('NewsItem/NewsComponent/NewsLines/NewsLine'):
        if not node.find('NewsLineType[@FormalName="CatchLine"]') is None:
            summary = node.find('NewsLineText').text
            break

    content = tree.findall('NewsItem/NewsComponent/NewsComponent/ContentItem/DataContent/p')
    return summary, [p.text for p in content]


def get_images(data):
    imgroot = ET.fromstring(data).find('NewsItem/NewsComponent/NewsComponent[@Duid="photo0"]')

    images = []

    for imgnode in imgroot.findall('NewsComponent'):
        if imgnode.find('Role[@FormalName="Thumbnail"]') is not None:
            images.append(imgnode.find('ContentItem').get('Href'))

    return images



def get_relevant_data(who, max_results=30):
    try:
        data = urllib2.urlopen(base_url + '?%s=%s&rows=%d' % ('who_pers', quote(who), max_results)).read()
    except urllib2.HTTPError:
        return

    tree = ET.fromstring(data)
    refs = tree.findall('NewsItem/NewsComponent/NewsComponent')

    for ref in refs:
        url = ref.find('NewsItemRef').get('NewsItem')
        title = ref.find('NewsLines/HeadLine').text
        data = urllib2.urlopen(url).read()

        date = get_published_at(data)
        metadata = get_entities(data)
        summary, content = get_content(data)
        images = [url.rsplit('/', 1)[0] + '/' + img for img in get_images(data)]

        yield url.rsplit('.xml', 1)[0], date, title, summary, content, metadata, images[0]


if __name__ == '__main__':
    # Example how to use this module
    for url, date, title, summary, paragraphs, metadata, images in get_relevant_data("Barack Obama"):
        print images