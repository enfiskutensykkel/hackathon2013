var speakerDimension, timeDimension, groupByTime;

function filterResult(json) {

	var data = crossfilter(json);

	var search_term = $(".searchField").val();

	speakerDimension = data.dimension(function(d) {return d.who;});
	timeDimension = data.dimension(function(d) {return new Date(d.published_at);});
	tagDimension = data.dimension(function(d) {return d.tags;});

	speakerDimension.filter(search_term);

	return timeDimension.top(Infinity);

}

function filterByTag(tag) {
	tagDimension.filter(function(d) {return d.indexOf(tag) > 0;})
}
