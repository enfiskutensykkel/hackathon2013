

$(document).ready (function ()
{
	addEvents();
});


function addQuotes (item)
{
	$.tmpl( "quoteItemTmpl", item ).appendTo("#quotesList");
	$(".tag").on("click", function() { 
		return $(this).hasClass('selected') ?  onTagFilter("") : onTagFilter(this.innerHTML); 
	})
}

function addEvents ()
{
	var self = this;
	$(".searchField").keyup(function (e)
	{
		if (event.which == 13)
			self.doSearch();
	});
	
	$(".searchField").focus(function ()
	{
		$(this).val("");
	});
}

function doSearch (text)
{
	$("#quotesList").empty();
	$("#quotesList").append("<div id='searchInfo' class='quotePart'>Searching...</div>");
	$("#progress").show();
	putSerch(text, onSearchResult);
}

function onSearchResult (data)
{
	$("#searchInfo").remove();
	$("#progress").hide();

	data = filterResult(data.data);
	addQuotes(data);	
	
	$(".linkWrapper").empty();
	$(".linkWrapper").append("<a class='filterLinkSpeaker selected' href='javascript:onRelatedLinks(true);'>Quotes from this person</a>");
	$(".linkWrapper").append("<a class='filterLinkOthers' href='javascript:onRelatedLinks(false);'>Quotes from other people in articles related to this person</a>");		

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