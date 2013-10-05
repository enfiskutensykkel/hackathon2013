# -*- coding: utf-8 -*-

import urllib2

api_key='x57tjyenbds4489ffjmcgdx3'

data = """
Foreign military forces appear to have carried out a pre-dawn raid on a southern Somalian coastal town, apparently in pursuit of "a high-profile target" linked to the militant al-Shabaab group that was behind last month's Kenyan mall shootings.

The pre-dawn raid – which initial but unconfirmed reports suggested may have involved US troops – took place in Barawe, in the lower Shabelle region 240km south of Mogadishu. It is the same town where US navy commandos killed a senior al-Qaida member four years ago.

The raid comes as Kenya's military confirmed the names of four al-Shabaab fighters implicated in the Westgate attack. Major Emmanuel Chirchir said the men were Abu Baara al-Sudani, Omar Nabhan, Khattab al-Kene and Umayr – names that were first broadcast by a local Kenyan television station.

"I confirm those are the names of the terrorist," he said, in a tweet sent to the Associated Press.

The publication of the identities supports CCTV footage from the Nairobi mall published by a private TV station that shows no more than four attackers, contradicting earlier government statements that between 10 to 15 attackers were involved.
"""

request = urllib2.Request('http://api.opencalais.com/tag/rs/enrich', headers={
    'x-calais-licenseID': api_key,
    'content-type': 'text/raw',
    'accept': 'application/json'
})
result = urllib2.urlopen(request, data).read()

#Web service URL for improved REST API is located at http://api.opencalais.com/tag/rs/enrich
#Clients should create an HTTP POST request.
#Document content should be passed as the body of the HTTP request.
#Submitted content should be UTF-8 encoded.
#Your Calais license, different processing and user options are specified as HTTP headers (key-value pairs) of the request. Following headers are mandatory:
#x-calais-licenseID: value of this header is your license key
#content-type: value of this parameter is the content type of submitted content, whether its text/raw, text/html, etc., as documented here
#accept or outputformat: possible values are the expected MIME types of response, e.g., xml/rdf, application/json, etc., as documented here
#Specification of all other processing and user options is optional.
