import re 
import tweepy 
import csv
import json
import jsonpickle
from tweepy import AppAuthHandler 
from textblob import TextBlob 
  
class TwitterClient(object): 
    ''' 
    Generic Twitter Class for sentiment analysis. 
    '''
    def __init__(self): 
        ''' 
        Class constructor or initialization method. 
        '''
        # keys and tokens from the Twitter Dev Console - REPLACE X's with your code!
        consumer_key = 'XXXXXXXXXXXXXXXXXXXXXXXXX'
        consumer_secret = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
        access_token = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
        access_secret = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
 
        # create OAuthHandler object 
        self.auth = AppAuthHandler(consumer_key, consumer_secret) 
        # set access token and secret 
        #self.auth.set_access_token(access_token, access_secret) 
        # create tweepy API object to fetch tweets 
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True) 

  
    def clean_tweet(self, tweet): 
        ''' 
        Utility function to clean tweet text by removing links, special characters 
        using simple regex statements. 
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()) 
  
    def get_tweet_sentiment(self, tweet): 
        ''' 
        Utility function to classify sentiment of passed tweet 
        using textblob's sentiment method 
        '''
        # create TextBlob object of passed tweet text 
        analysis = TextBlob(self.clean_tweet(tweet)) 
        # set sentiment 
        if analysis.sentiment.polarity > 0: 
            return 'positive'
        elif analysis.sentiment.polarity == 0: 
            return 'neutral'
        else: 
            return 'negative'
  
    def get_tweets(self, query, count = 10): 
        ''' 
        Main function to fetch tweets and parse them. 
        '''
        # empty list to store parsed tweets 
        tweets = [] 
  
        try: 
            # call twitter api to fetch tweets 
            fetched_tweets = self.api.search(q = query, count = count) 
  
            # parsing tweets one by one 
            for tweet in fetched_tweets: 
                # empty dictionary to store required params of a tweet 
                parsed_tweet = {} 
  
                # saving text of tweet 
                parsed_tweet['text'] = tweet.text 
                # saving sentiment of tweet 
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text) 
  
                # appending parsed tweet to tweets list 
                if tweet.retweet_count > 0: 
                    # if tweet has retweets, ensure that it is appended only once 
                    if parsed_tweet not in tweets: 
                        tweets.append(parsed_tweet) 
                else: 
                    tweets.append(parsed_tweet) 
  
            # return parsed tweets 
            return tweets 
  
        except tweepy.TweepError as e: 
            # print error (if any) 
            print("Error : " + str(e)) 
  
def main(): 
    # creating object of TwitterClient Class 
    api = TwitterClient() 
    sentimentValueList = list()
    # calling function to get tweets 
    count=0
    with open('place_id_list.csv', 'r') as f:

        place_id_reader=csv.reader(f,delimiter=',')
        for row in place_id_reader:
            print(row[0])
            tweetCount = 0
            place_id = str(row[1])
            searchQuery =('place:%s' % place_id)
            tweets = api.get_tweets(query=searchQuery, count = 500)

            ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive'] 
            # percentage of positive tweets 
            print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets))) 
        
            ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative'] 
            # percentage of negative tweets 
            print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets))) 
            
            # percentage of neutral tweets 
            print("Neutral tweets percentage: {} %".format(100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets))) 
            #with open(str(row[0])+"1.json",'w') as writeFile:
            sentimentValueList.append(row[count] +","+ str(100*len(ptweets)/len(tweets))+","+ str(100*len(ntweets)/len(tweets)) +","+ str((100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets))))
 
    #write sentiment values to a csv file
    with open('sentimentValueList.csv','w') as outFile:
        for item in sentimentValueList:
            outFile.write("%s\n" % item)
    # printing first 5 positive tweets 
        #    print("\n\nPositive tweets:") 
        #    for tweet in ptweets[:10]: 
        #        print(tweet['text']) 
  
        # printing first 5 negative tweets 
        #    print("\n\nNegative tweets:") 
        #    for tweet in ntweets[:10]: 
      #          print(tweet['text']) 
      
if __name__ == "__main__": 
    # calling main function 
    main() 