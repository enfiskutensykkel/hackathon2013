

$(document).ready (function ()
{
	addEvents();
});


function addQuotes (item)
{
	$.tmpl( "quoteItemTmpl", item ).appendTo("#quotesList");
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
	
	addQuotes(data);	
	filterResult(data);
	
}