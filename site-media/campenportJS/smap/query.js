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

function getBaselineTags(callback, query_id){
	$.ajax({
		async: true,
		type: 'POST',
		url: '/ARDgetData/api/query?',
		data: "select * where Metadata/Location/Building = '" + query_id +"' and (Metadata/Extra/Operator like 'baseline-%') and not (Metadata/Path like '1-hr') and not (Metadata/Extra/Resample like 'subsample-mean-3600') and not (Metadata/Extra/Type like 'steam baseline')",
		success: function(response) {
			callback(response);
		}
	});
}

function getBuildingNansum(callback, query_id, starttime, endtime){
	$.ajax({
		async: true,
		type: 'POST',
		url: '/ARDgetData/api/query?',
		data: "apply nansum(axis=1) < paste < window(first, field='minute', increment=15) < units to data in (" + starttime + ", " + endtime + ") streamlimit 10000 where Metadata/Extra/System = 'electric'  and ((Properties/UnitofMeasure = 'kW' or Properties/UnitofMeasure = 'Watts') or Properties/UnitofMeasure = 'W') and Metadata/Location/Building like '" + query_id + "%' and not Metadata/Extra/Operator like 'sum%' and not Path like '%demand'",
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
