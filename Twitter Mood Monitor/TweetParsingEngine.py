from TweetManipulator import TweetManipulator
from SQLDBConnector import SQLDBConnector
import time
import pprint
import logging
import sys
pp = pprint.PrettyPrinter(indent=4)

DBC = SQLDBConnector()
TM = TweetManipulator("TOBECHANGED")
radius = "10mi" #search radius
Locations = {
	"boston" : "42.3581,-71.0636", #Boston
	"nyc" : "40.700,-74.00"

}

#main logic loop
def main():
#for location in Locations.keys():
#	defaultRecords += "("+location+", 0, 0, 0 ),"
	
#DBC.__queryDB__("INSERT OR IGNORE `location_mood_data` ('location', 'total_parsed', 'num_happy', 'num_unhappy') VALUES "+defaultRecords[:-1]+";")

	for location in Locations:
		TM.__reinit__(Locations[location]+","+radius)
		TM.gatherTweetData()
		
		LocationMoodDataList = None
		SampleTweet = None
		totalHappy = totalUnhappy =0
		
		for tweetData in TM.tweetDataList:
			numEmoticonsInTweet = tweetData[2][0] + tweetData[2][1]
			
			if numEmoticonsInTweet != 0:	# we only care about tweets with emoticons
				totalHappy += tweetData[2][0]
				totalUnhappy += tweetData[2][1]
				
				
				if SampleTweet is None:	#just take the first tweet as a sample for the area
					SampleTweet = (tweetData[0], location,  tweetData[1], tweetData[2][0], tweetData[2][1])
		
		currentNumHappy = currentNumUnhappy = 0
		currentLocationMoodData = DBC.__queryDB__("SELECT num_happy, num_unhappy FROM `location_mood_data` WHERE location='"+location+"'")
		if currentLocationMoodData != []:
			currentNumHappy, currentNumUnhappy = currentLocationMoodData[0]
			
		
		if SampleTweet is not None:
			pp.pprint(SampleTweet)
			DBC.insertAll('sample_tweets', [SampleTweet])
		
		DBC.insertAll('location_mood_data', [(
			location,
			totalHappy+currentNumHappy+totalUnhappy+currentNumUnhappy,
			totalHappy+currentNumHappy,
			totalUnhappy+currentNumUnhappy
		)])
	time.sleep(5)

# safely close the DB connection upon exit
try:
	while True:
		main()
except (KeyboardInterrupt):
	DBC.__closeDB__()
	sys.exit()
except :
	#logging.exception(sys.exc_info()[0])
	print sys.exec_info()[0]
	DBC.__closeDB__()
	sys.exit()
	#DBC.__init__()
	#main()