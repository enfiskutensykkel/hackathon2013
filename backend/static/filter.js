var speakerDimension, timeDimension, tagDimension, peopleDimension, speaker;

function filterResult(json) {

	var data = crossfilter(json);

	speakerDimension = data.dimension(function(d) {return d.who;});
	timeDimension = data.dimension(function(d) {return new Date(d.date);});
	tagDimension = data.dimension(function(d) {return d.tags;});
	peopleDimension = data.dimension(function(d) {return d.people;});

	speaker = $(".searchField").val();

	filterBySpeaker(true);

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
