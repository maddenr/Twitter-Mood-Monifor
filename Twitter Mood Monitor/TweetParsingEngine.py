from TweetManipulator import TweetManipulator
from SQLDBConnector import SQLDBConnector

DBC = SQLDBConnector()
TM = TweetManipulator("TOBECHANGED")
radius = "10mi" #search radius
Locations = {
	"boston" : "42.3581,-71.0636" #Boston

};

#main logic loop
#def main():

for location in Locations:
	TM.__reinit__(Locations[location]+","+radius)
	TM.gatherTweetData()
	
	LocationMoodDataList = []
	SampleTweetList = []
	
	for tweetData in TM.tweetDataList:
		if tweetData[2][0] + tweetData[2][1] != 0:
			TM.printMoodData(tweetData[2][0], tweetData[2][1], tweetData[1])
	




# safely close the DB connection upon exit
#try:
	#main()
#except:
#	DBC.__closeDB__()