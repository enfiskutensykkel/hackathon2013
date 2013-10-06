

function putSerch (text, cbResult, nextUrl)
{
	/*
	var data = 
	[
		{
			who: "Barack Obama",
			quote: "For as reckless as a government shutdown is, an economic shutdown that comes with default would be dramatically worse"
		},
		{
			who: "Barack Obama",
			quote: "For as reckless as a government shutdown is, an economic shutdown that comes with default would be dramatically worse"
		}
	];
	
	cbResult(data);
	*/
	
	var url = "/persons/"+text+"/";
	
	if (nextUrl)
		url = nextUrl;
	
	$.ajax({
		url : url,
		type: 'get',
		success : function(data, textStatus, jqXHR)
		{
			if (cbResult)
				cbResult(data);
		},
		error : function(data, textStatus, jqXHR)
		{
			throw new Error("An error occured. "+textStatus +" - "+data.status);
		}
	});
	
}