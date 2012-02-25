function httpGetTags(callback, querystring) {
	$.ajax({
		async: true,
		type: 'POST',
		url: '/ARDgetData/api/query?',
		data: querystring,
		success: function(response) {
			callback(response);
		}
	});
}

function httpGetData(callback, latest, inputUUID, starttime, endtime, output, typeInput) {
	$.ajax({ 
			async: true,
			type: 'GET',
			url: "/ARDgetData/api/data/uuid/" + escape(inputUUID) + "?starttime=" + escape(starttime) + "&endtime=" + escape(endtime),
			success: function(resp) {
				callback(resp, typeInput);
			}
	});
}

