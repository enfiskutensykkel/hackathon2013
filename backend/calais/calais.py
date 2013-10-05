# -*- coding: utf-8 -*-

import urllib2
import json

_api_key='x57tjyenbds4489ffjmcgdx3'


def find_quotations_in_text(text, html=False):
    """Finds all quotations in the given raw text.
    Usage: See example code at the bottom of the file
    """

    request = urllib2.Request('http://api.opencalais.com/tag/rs/enrich', headers={
        'x-calais-licenseID': _api_key,
        'content-type': 'text/html' if html else 'text/raw',
        'accept': 'application/json'
    })
    result = urllib2.urlopen(request, text.encode('utf8')).read()

    data = json.loads(result)

    def iter_groups(data):
        for key, group in data.iteritems():
            if not '_type' in group: continue
            yield group

    def iter_quotations(data):
        for group in iter_groups(data):
            if group['_type'] == 'Quotation':
                person = group['person']
                quote = group['quote']

                name = data[person]['commonname']

                yield name, quote

    return iter_quotations(data)


if __name__ == '__main__':
    # Example
    text = """
Foreign military forces appear to have carried out a pre-dawn raid on a southern Somalian coastal town, apparently in pursuit of "a high-profile target" linked to the militant al-Shabaab group that was behind last month's Kenyan mall shootings.

The pre-dawn raid – which initial but unconfirmed reports suggested may have involved US troops – took place in Barawe, in the lower Shabelle region 240km south of Mogadishu. It is the same town where US navy commandos killed a senior al-Qaida member four years ago.

The raid comes as Kenya's military confirmed the names of four al-Shabaab fighters implicated in the Westgate attack. Major Emmanuel Chirchir said the men were Abu Baara al-Sudani, Omar Nabhan, Khattab al-Kene and Umayr – names that were first broadcast by a local Kenyan television station.

"I confirm those are the names of the terrorist," he said, in a tweet sent to the Associated Press.

The publication of the identities supports CCTV footage from the Nairobi mall published by a private TV station that shows no more than four attackers, contradicting earlier government statements that between 10 to 15 attackers were involved.
"""

    for i in range(1, 100):
        for name, quote in find_quotations_in_text(text):
            print "%s: %s" % (name, quote)
