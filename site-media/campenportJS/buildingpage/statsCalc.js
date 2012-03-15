function runStats(data, tags){
	//do stuff
	//console.log(data);
//	console.log(tags);

	if(tags[0]=="Actual Usage"){
		actualData = data[0][0]['Readings'];
		predData = data[1][0]['Readings'];
	}
	else{
		actualData = data[1][0]['Readings'];
		predData = data[0][0]['Readings'];
	}
	
	bucketsize = 5*60*1000;

	starttime = predData[0][0];
	endtime = predData[predData.length-1][0];
	cleaned = cleanEdges(buildAverages(predData, endtime, starttime), buildAverages(actualData, endtime, starttime));
	predBucketed = cleaned[0];
	actBucketed = cleaned[1];
	rms = Math.round(rmsDev(actBucketed, predBucketed)*100)/100;
	$('.stats1').html("<strong>" + rms + " kW</strong>");

	
}

function buildAverages(inputdata, endtime, starttime){
		//build up aligned average buckets
        // this function takes in a saveddata associated array of the format
		var avgbucketSize = 15*60000; /*WARNING: the quantity preceding *60000 must be greater than the time between data for the set of data with the largest time between reports*/
        var averaged = [];
        newendtime = endtime - endtime%avgbucketSize; //rounds endtime down
        newstarttime = starttime + (avgbucketSize - starttime%avgbucketSize); //rounds starttime up
       // for (var nums2 = 0; nums2<Object.customlen(saveddata); nums2++){ //for each UUID
                var thisUUIDoutput = [];
                //var currentUUID = dcent_uuids[nums2];
                var thisUUIDdata = inputdata;
                var upperbound = newendtime;
                var lowerbound = newendtime - avgbucketSize;
                while(thisUUIDdata.length != 0){ //goes through the thisUUIDdata list
                        var avgtopTracker = 0;
                        var counter = 0;
                        while(thisUUIDdata.length != 0 && thisUUIDdata[thisUUIDdata.length-1][0]>lowerbound ){
                                counter++;
                                avgtopTracker += thisUUIDdata.pop()[1];
                        }
                        theCalcdAvg = avgtopTracker/counter;
                        if (!isNaN(theCalcdAvg)){
                                //Prevents NaNs in raw seconds output
                                thisUUIDoutput.push([upperbound, theCalcdAvg]);
                        }
                        upperbound = lowerbound;
                        lowerbound = upperbound - avgbucketSize;
                }
                averaged = thisUUIDoutput;
        //}
        //console.log(averaged);
        return averaged;
}

function cleanEdges(averaged1, averaged2){
		//cut off extras from either array
		if(averaged1.length>averaged2.length){
			//do nothing
			flipped = false;
		}
		else{
			avgtemp = averaged1;
			averaged1 = averaged2;
			averaged2 = avgtemp;
			flipped = true;
		}
		while(averaged1[0][0]!=averaged2[0][0]){
			averaged1.shift();
		}
		while(averaged1[averaged1.length-1][0]!=averaged2[averaged2.length-1][0]){
			averaged1.pop();
		}
		if(flipped){
			return [averaged2, averaged1];
		}
		else{
			return [averaged1, averaged2];
		}
}

function rmsDev(actual, predicted){
	//calculates RMS deviation for two arrays that are matched/aligned
	var sum = 0;
	for(x = 0; x<actual.length; x++){
//err=sqrt(sum((regVals-y)**2)/len(y))
		sum += Math.pow((predicted[x][1]-actual[x][1]), 2);	
	}
	sum = sum/actual.length;
	return Math.pow(sum, 0.5);
}
