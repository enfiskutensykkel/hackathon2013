Can I quote you on that?
========================

An application to extract quotes from citations and sources and map them to who said it, when it was said and in the context it was said based on the articles and sources the quote appears in.

This is a project done for the [hackathon](https://www.hackerleague.org/hackathons/wan-ifra-media-hack-day) @ [Media Hack Day 2013](http://www.mediahackday.com/ "#mdh2013").
Contributors are
  * Katherine Mccurdy (k-means, kmccurdy)
  * Florian Winter (fwinter, fwinter555)
  * Martin Halvorsen (marty, shadowano)
  * Jonas Markussen (enfiskutensykkel)

APIs
----

We read data from the 
[AFP](http://www.ipadafp.afp.com/mediahackdays/index.php?p=doc),
[theguardian](http://explorer.content.guardianapis.com/#/)
and the [storyful](http://github.com/storyful/StoryfulApiDoc) APIs.
We make use of the [OpenCalais](http://www.opencalais.com/) to extract semantic data from the data delivered by the APIs.

Libraries
---------
Libraries we use:
  * jQuery and jQuery template for pretty front-end stuff
  * crossfilter for managing large data objects in JavaScript
  * Flask for Python back-end


Hosting
-------
The application is hosted on [heroku](http://www.heroku.com).

The application is running here:
http://peaceful-waters-6158.herokuapp.com/static/index.html
