import tweepy 
import csv

# keys and tokens from the Twitter Dev Console - REPLACE X's with your code!
consumer_key = 'XXXXXXXXXXXXXXXXXXXXXXXXX'
consumer_secret = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
access_token = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
access_secret = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
 
  
#Pass our consumer key and consumer secret to Tweepy's user authentication handler
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

#Pass our access token and access secret to Tweepy's user authentication handler
auth.set_access_token(access_token, access_secret)

#Creating a twitter API wrapper using tweepy
api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

#Check Rate Limit
print(api.rate_limit_status()['resources']['search'])

#Error handling for API errors
if (not api):
	print ("Problem connecting to API")

lat_long_list = (["Rochester","43.155708","-77.612545"],["Manhattan","40.753250","-74.003807"],["Buffalo","42.887691","-78.879372"],["Syracuse","43.047939","-76.147453"],
["Albany","42.651720","-73.755090"],["Hempstead","40.706900","-73.620350"],["Yonkers","40.930790","-73.898293"],["Brentwood","40.781212","-73.246147"],["Schenectady","42.814220","-73.944099"],["Utica","43.102039","-75.230003"],["Niagara Falls","43.094460","-79.056427"])


place_id_list = list()
count=0

#Getting Geo IDs
with open('place_id_list.csv', 'w') as f:
	for latlong in lat_long_list:
		places = api.geo_search(lat=lat_long_list[count][1], long=lat_long_list[count][2], granularity="neighborhood")
		try:
			place_id_list.append((lat_long_list[count][0],places[0].id))
			count+=1
			print('Rochester id is: ',places[0].id)
		except BaseException as e:
			print("Error on_data: %s" % str(e)+"at " + str(count))
		
	writer = csv.writer(f,delimiter=',')
	writer.writerows(place_id_list)


