var cxData, speakerDimension, timeDimension, tagDimension, peopleDimension, speaker;

function filterResult(json) {

	cxData = crossfilter(json);

	speakerDimension = cxData.dimension(function(d) {return d.who;});
	timeDimension = cxData.dimension(function(d) {return new Date(d.date);});
	tagDimension = cxData.dimension(function(d) {return d.tags;});
	peopleDimension = cxData.dimension(function(d) {return d.people;});

	speaker = $(".searchField").val().replace(/(\b)([a-zA-Z])/g,
           function(firstLetter){
              return   firstLetter.toUpperCase();
           });

	filterBySpeaker(true);

	return returnFilteredDataObj();

}

function removeFilters()
{
	if (cxData)
	{
		speakerDimension.remove();
		timeDimension.remove();
		tagDimension.remove();
		peopleDimension.remove();
	}
}

function filterAdd (json)
{
	cxData.add(json);
	return returnFilteredDataObj();
}

function filterByTag(tag) {
	if (!tag) {
		return tagDimension.filterAll();
	}
	return tagDimension.filterFunction(function(d) { return d.indexOf(tag) >= 0; });
}

function filterBySpeaker(useSpeaker) {
	return speakerDimension.filterFunction(function(d) { return useSpeaker ? d == speaker : d != speaker;});
}

function returnFilteredDataObj() {
	return {data: timeDimension.top(Infinity), next: null};
}
