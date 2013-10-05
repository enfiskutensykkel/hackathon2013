

$(document).ready (function ()
{
	addEvents();
});


function addQuote (item)
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
}

function doSearch (text)
{
	putSerch(text, onSearchResult);
}

function onSearchResult (data)
{
	for (var i=0; i < data.length; i++)
	{
		addQuote(data[i]);
	}
}