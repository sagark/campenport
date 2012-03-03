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

function httpGetTagsWINP(callback, querystring, inp, inptype, numMod) {
	$.ajax({
		async: true,
		type: 'POST',
		url: '/ARDgetData/api/query?',
		data: querystring,
		success: function(response) {
			callback(response, inp, inptype, numMod);
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

function httpGetLatestData(callback, querystring, x, endat) {
    //IMPORTANT NOTE: you can only get 10 UUIDs of data in one call
	$.ajax({ 
		async: false,
		type: 'POST',
		url: '/ARDgetData/api/query?',
		data: "select data before now limit 1 where " + querystring,
		success: function(response) {
			callback(response, x, endat);
		}
	});
}

