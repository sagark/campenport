/* 
 *  Scripts for statistical calculations for campenport buildingpages 
 */


/*
 * @params: actual - actual incoming array of data, in reverse-time order
 *          baseline - baseline data, incoming array in reverse-time order
 *          avgArr - array of average values used to calculate deviation percent
 * @returns: nothing, sets innerHTML of divs with rms dev and rms dev percent
 */
function runStats(actual, baseline, avgArr){
	if((typeof baseline)=='undefined'){
		return;
	}
	actualData = actual.slice(0);
    predData = baseline.slice(0);
	bucketsize = 5*60*1000;

	starttime = predData[0][0];
	endtime = predData[predData.length-1][0];
	cleaned = cleanEdges(buildAverages(predData, endtime, starttime), buildAverages(actualData, endtime, starttime));
	predBucketed = cleaned[0];
	actBucketed = cleaned[1];
	rms = Math.round(rmsDev(actBucketed, predBucketed)*100)/100;
	$('.stats1').html("<strong>" + rms + " kW</strong>");
	if(avgArr!=0){
		rmsPercent = Math.round((rms/avgArr[0][1])*10000)/100
		$('.stats2').html("<strong>" + rmsPercent + "%</strong>");
	}
}

function buildAverages(inputdata, endtime, starttime){
		//build up aligned average buckets
        // this function takes in a saveddata associated array of the format
		var avgbucketSize = 15*60000; /*WARNING: the quantity preceding *60000 must be greater than the time between data for the set of data with the largest time between reports*/
        var averaged = [];
        newendtime = endtime - endtime%avgbucketSize; //rounds endtime down
        newstarttime = starttime + (avgbucketSize - starttime%avgbucketSize); //rounds starttime up
                var thisUUIDoutput = [];
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
        return averaged;
}

function cleanEdges(averaged1, averaged2){
		//FOR FUTURE REFERENCE: Incoming Timeseries data will be in reverse-time order.!!!!

		while(averaged1[0][0]<averaged2[0][0]){
			//case where averaged1 starts after averaged2
			//prune start pieces off of averaged2
			averaged2.shift();
		} 
		while(averaged1[0][0]>averaged2[0][0]){
			//case where averaged1 starts before averaged2
			//prune start pieces off of averaged1
			averaged1.shift();
		}
		while(averaged1[averaged1.length-1][0]<averaged2[averaged2.length-1][0]){
			//case where averaged2 ends before averaged1
			//prune end off of averaged 1
			averaged1.pop();
		} 
		while (averaged1[averaged1.length-1][0]>averaged2[averaged2.length-1][0]){
			//case where averaged1 ends before averaged2
			//prune end off of averaged 2
			averaged2.pop();
		}
		return[averaged1, averaged2];  
		
}

function rmsDev(actual, predicted){
	//calculates RMS deviation for two arrays that are matched/aligned
	var sum = 0;
	for(x = 0; x<actual.length; x++){
		sum += Math.pow((predicted[x][1]-actual[x][1]), 2);	
	}
	sum = sum/actual.length;
	return Math.pow(sum, 0.5);
}
