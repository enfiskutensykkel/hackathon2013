

$(document).ready (function ()
{
	addEvents();
});


var text = "";
var counterMax = 10;
var counter = 0;
var quotes = [];

function addQuotes (item)
{
	$.tmpl( "quoteItemTmpl", item ).appendTo("#quotesList");
	$(".tagList .tag").on("click", function() {
		return $(this).hasClass('selected') ?  onTagFilter("") : onTagFilter(this.innerHTML);
	})
}

function addEvents ()
{
	var self = this;
	$(".searchField").keyup(function (event)
	{
		if (event.which == 13)
		{
			$("#quotesList").empty();
			$("#quotesList").append("<div id='searchInfo' class='quotePart'>Searching...</div>");
			quotes = [];
			self.doSearch($(this).val());
			counter = 0;
		}
	});

	$(".searchField").focus(function ()
	{
		if ($(this).val() === "Find quotes by person or topic")
			$(this).val("");
	});
}

function doSearch (value, nextUrl)
{
	text = value;
	putSerch(text, onSearchResult, nextUrl);
}

function onSearchResult (result)
{
	$("#progress").hide();
	$("#searchInfo").remove();

	for (var i=0; i < result.data.length; i++)
	{
		// Convert unix timestamp to locale date string
		result.data[i].date = new Date(result.data[i].date*1000).toLocaleDateString();
		quotes.push(result.data[i]);
		if (!cxData) {
			$("#searchInfo").remove();
			$("#progress").hide();
			$("#quotesList").empty();

			data = filterResult(quotes);
			addQuotes(data);

		} else {

			$("#searchInfo").remove();
			$("#progress").hide();
			$("#quotesList").empty();

			data = filterAdd([result.data[i]]);
			addQuotes(data);

			addLinkWrapper();
		}
	}

	if (result.next && counter < counterMax)
	{
		doSearch(text, result.next);
		counter++;
	}
	else
	{

		$("#quotesList").empty();

		//data = filterResult(quotes);
		addQuotes(data);

		addLinkWrapper();

	}

}

function addLinkWrapper ()
{
	$(".linkWrapper").empty();
	$(".linkWrapper").append("<a class='filterLinkSpeaker selected' href='javascript:onRelatedLinks(true);'>Quotes from this person</a>");
	$(".linkWrapper").append("<a class='filterLinkOthers' href='javascript:onRelatedLinks(false);'>Related quotes in same articles</a>");
}

function onRelatedLinks (useSpeaker)
{
	$("#quotesList").empty();
	filterBySpeaker(useSpeaker);

	var data = returnFilteredDataObj();
	addQuotes(data);

	if (useSpeaker) {
		$(".filterLinkOthers").removeClass('selected');
		$(".filterLinkSpeaker").addClass('selected');
	} else {
		$(".filterLinkSpeaker").removeClass('selected');
		$(".filterLinkOthers").addClass('selected');
	}

}

function onTagFilter (tag)
{
	$("#quotesList").empty();
	filterByTag(tag);
	var data = returnFilteredDataObj();
	addQuotes(data);
	if (!tag) {
		$(".tag").removeClass('selected')
	} else {
		$(".tag." + tag).addClass('selected');
	}
}