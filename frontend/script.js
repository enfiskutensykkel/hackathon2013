

$(document).ready (function ()
{
	addEvents();
});


function addQuote ()
{
	$("#quotesList").append(element);
}

function addEvents ()
{
	var self = this;
	$("searchField").click(function (e)
	{
		self.doSearch();
	});
}

function doSearch (text)
{

}