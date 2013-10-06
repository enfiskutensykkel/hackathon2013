var speakerDimension, timeDimension, tagDimension, peopleDimension;

function filterResult(json) {

	var data = crossfilter(json);

	var search_term = $(".searchField").val();

	speakerDimension = data.dimension(function(d) {return d.who;});
	timeDimension = data.dimension(function(d) {return new Date(d.date);});
	tagDimension = data.dimension(function(d) {return d.tags;});
	peopleDimension = data.dimension(function(d) {return d.people;});

	speakerDimension.filter(search_term);

	return timeDimension.top(Infinity);

}

function filterByTag(tag) {
	tagDimension.filter(function(d) {return d.indexOf(tag) > 0;})
}

function filterByPeople(person) {
	peopleDimension.filter(function(d) {return d.indexOf(person) > 0;})
}
