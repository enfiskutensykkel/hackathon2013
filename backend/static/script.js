

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
	
	$(".searchField").focus(function ()
	{
		$(this).val("")
	});
}

function doSearch (text)
{
	$("#quotesList").empty();
	$("#progress").show();
	putSerch(text, onSearchResult);
}

function onSearchResult (data)
{
	addQuote(data)
	/*
	for (var i=0; i < data.data.length; i++)
	{
		addQuote(data.data[i]);
	}
	*/
	$("#progress").hide();
}