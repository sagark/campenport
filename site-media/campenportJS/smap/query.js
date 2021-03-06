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

function getBuildingNansum(callback, query_id, starttime, endtime, fieldsize, inc){
	$.ajax({
		async: true,
		type: 'POST',
		url: '/ARDgetData/api/query?',
		data: "apply nansum(axis=1) < paste < window(first, field='" + fieldsize
+ "', width=" + inc + ") < units to data in (" + starttime + ", " + endtime + ") streamlimit 10000 where (Metadata/Extra/System = 'total' or Metadata/Extra/System = 'electric') and ((Properties/UnitofMeasure = 'kW' or Properties/UnitofMeasure = 'Watts') or Properties/UnitofMeasure = 'W') and Metadata/Location/Building like '" + query_id + "%' and not Metadata/Extra/Operator like 'sum%' and not Path like '%demand'",
		success: function(response) {
			callback(response);
		},
		error: function(response) {
			///process stream and call callback here
			//start hacky fix for streaming
			a = response.responseText.split("}}}]");
			//console.log(a);
			for(x = 0; x<a.length; x++){
				a[x] += "}}}]";
			}
			a.pop();
			for(x = 0; x<a.length; x++){
				a[x] = $.parseJSON(a[x]);
			}
			for(x = 1; x<a.length; x++){
				a[0][0]['Readings'] = a[0][0]['Readings'].concat(a[x][0]['Readings']);
			}
			//end hacky fix for streaming
			respMod =  a[0] ;
			callback(respMod);
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



function httpGetTagsStreamHandler(callback, querystring, inp, inptype, numMod) {
	$.ajax({
		async: true,
		type: 'POST',
		url: '/ARDgetData/api/query?',
		data: querystring,
		success: function(response) {
			callback(response, inp, inptype, numMod);
		},
		error: function(response) {
			///process stream and call callback here
			//start hacky fix for streaming
			a = response.responseText.split("}}}]");
			//console.log(a);
			for(x = 0; x<a.length; x++){
				a[x] += "}}}]";
			}
			a.pop();
			for(x = 0; x<a.length; x++){
				a[x] = $.parseJSON(a[x]);
				//This shift fixes the 1 point overlap
				a[x][0]['Readings'].shift();
			}
			for(x = a.length-2; x>=0; x--){
				a[a.length-1][0]['Readings'] = a[x][0]['Readings'].concat(a[a.length-1][0]['Readings']);
			}
			//end hacky fix for streaming
			respMod =  a[a.length-1] ;
			callback(respMod, inp, inptype, numMod);
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

//unused, not sure what the issue is with fetching baselines this way
function httpGetDataQuick(callback, latest, inputUUID, starttime, endtime, output, typeInput) {
	$.ajax({ 
		async: true,
		type: 'POST',
		url: '/ARDgetData/api/query?',
		timeout: 10000,
		data: "apply nansum(axis=1) < paste < window(first, field='hour', width=1) < units to data in (" + starttime + " ," + endtime + ") streamlimit 1000000 where uuid = '" + inputUUID + "'",
		success: function(resp){
			console.log("NORMAL");
			console.log(resp);
			callback(resp, typeInput);
		},
		error: function(response) {
			///process stream and call callback here
			//start hacky fix for streaming
			//console.log(a);
			a = response.responseText.split("}}}]");
			//console.log(a);
			for(x = 0; x<a.length; x++){
				a[x] += "}}}]";
			}
			//a.pop();
			for(x = 0; x<a.length; x++){
				a[x] = $.parseJSON(a[x]);
				//Shift required to fix 1 point overlap
				a[x][0]['Readings'].shift();
			}
			for(x = 1; x<a.length; x++){
				a[0][0]['Readings'] = a[0][0]['Readings'].concat(a[x][0]['Readings']);
			}
			//end hacky fix for streaming
			respMod =  a[0] ;
			callback(respMod, typeInput);
		}

	});
}

