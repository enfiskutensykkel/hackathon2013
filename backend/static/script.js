

$(document).ready (function ()
{
	addEvents();

	searchWord = getURLParameter("search");
	if (searchWord != "null" && searchWord != "")
	{
		$(".searchField").val(searchWord);
		search(searchWord);
	}
});


var text = "";
var counterMax = 10;
var counter = 0;
var quotes = [];
var nextUrl = "";
var loading = false;


function addEvents ()
{
	var self = this;
	$(".searchField").keyup(function (event)
	{
		if (event.which == 13)
		{
			var text = $(this).val();

			// If we still have filterobjekt, redirect to a search url instead
			/*
			if (cxData)
			{
				var url = window.location.protocol+"//"+window.location.hostname+":"+window.location.port+window.location.pathname;
				url += "?search="+text;
				window.location.href = url;
			}
			*/

			self.search(text);
		}
	});

	$(".searchField").focus(function ()
	{
		if ($(this).val() === "Find quotes by person or topic")
			$(this).val("");
	});

	$(document).scroll(function ()
	{
		self.loadMore();
	});
}

function search (value)
{
	removeFilters();

	$(".linkWrapper").empty();
	$("#quotesList").empty();
	$("#quotesList").append("<div id='searchInfo' class='quotePart'>Searching...</div>");
	quotes = [];
	this.doSearch(value);
	counter = 0;
}

function doSearch (value, nextUrl)
{
	loading = true;
	text = value;
	putSerch(text, onSearchResult, nextUrl);
}

function addQuotes (quotes)
{
	$.tmpl( "quoteItemTmpl", quotes ).appendTo("#quotesList");
	$(".tagList .tag").on("click", function() {
		return $(this).hasClass('selected') ?  onTagFilter("") : onTagFilter(this.innerHTML);
	})
}

function onSearchResult (result)
{
	$("#progress").hide();
	$("#searchInfo").remove();

	nextUrl = result.next;
	var addedQuote = false;

	for (var i=0; i < result.data.length; i++)
	{
		// Convert unix timestamp to locale date string
		result.data[i].date = new Date(result.data[i].date*1000).toLocaleDateString();

		//quotes.push(result.data[i]);

		if (!cxData)
		{
			$("#searchInfo").remove();
			$("#progress").hide();

			data = filterResult([result.data[i]]);
		}
		else
		{
			$("#searchInfo").remove();
			$("#progress").hide();

			data = filterAdd([result.data[i]]);
		}

		if (data.data.length > 0)
		{
			addLinkWrapper();

			//$("#quotesList").empty();
			if (result.data[i].who == text)
			{
				addQuotes({data :[result.data[i]]});
				addedQuote = true;
			}
		}
	}

	if (result.next && (counter < counterMax || !addedQuote) )
	{
		doSearch(text, result.next);
		counter++;
	}
	else
	{
		loading = false;
	}

}

function addLinkWrapper ()
{
	if ($(".linkWrapper").children().length == 0)
	{
		$(".linkWrapper").empty();
		$(".linkWrapper").append("<a class='filterLinkSpeaker selected' href='javascript:onRelatedLinks(true);'>Quotes from this person</a>");
		$(".linkWrapper").append("<a class='filterLinkOthers' href='javascript:onRelatedLinks(false);'>Related quotes in same articles</a>");
	}
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


function getURLParameter(name) {
    return decodeURI(
        (RegExp(name + '=' + '(.+?)(&|$)').exec(location.search)||[,null])[1]
    );
}


function loadMore ()
{
	var contentHeight = $(".contentWrapper").height();
	var scrollTop = $(window).scrollTop();

	var contentScrollHeight = contentHeight - ($(".mainWrapper").height() - contentHeight);
	var diff = $(".mainWrapper").height() - scrollTop - $(window).height();

	if (diff < 200 && !loading)
	{
		doSearch(text, nextUrl);
		console.log(diff);
	}
}