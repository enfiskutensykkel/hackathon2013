

function putSerch (text, cbResult)
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
	
	
	
	$.ajax({
		url : "/persons/barack%20obama/",
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