import json
import requests
import os
import tweepy
import re
import emoji

class twitterBot:
    def __init__(self):
        self.bearer = "Bearer AAAAAAAAAAAAAAAAAAAAAJXpGgEAAAAA6H%2F1Yrym2IixdK0reD1nDRQvDe4%3DxX1nDLsJ7dSNQsvlVCHRvbdHCBkhVKCtFGw2rORNfwTnxSFRKb"
        self.auth = tweepy.OAuthHandler("WKd7W3XoThJ9KCM02KXHtZzW9", "aHAd2Pr1eX8l2KZc6w9YQhKGqnhoV9w5jZYlBch2DJSEm77IJ7")
        self.auth.set_access_token("1306375500021903360-6hYTD0Ue97uYBVhy7GJtOLsgp0xmCu", "kMIA2Wqgsizwockn0IEaVT4tjwVrImoFVwKktlq7LGLDd")
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
        self.sentiment_url = "https://microsoft-text-analytics1.p.rapidapi.com/sentiment"
    def get_user_id(self,usernames):
        # url = "https://api.twitter.com/2/users?ids="
        list_of_ids = []
        for x in usernames:
            url = "https://api.twitter.com/2/users/by/username/"
            url = url + x
            results = requests.get(url, headers={"Authorization":self.bearer})
            searches = results.json()
            list_of_ids.append(searches["data"]["id"])
        return list_of_ids

    def recent_tweets(self, user, number=20):
        search1 = self.api.user_timeline(user,count=number)
        search = []
        for x in search1:
            search.append(x._json)
        list_of_recent_tweets = []
        for y in search:
            list_of_recent_tweets.append(y['text'])

        return list_of_recent_tweets

    def tweet(self, message):
        self.api.update_status("Test tweet!")

    def sentiment_analyzer(self,text):
        try:
            payload_part1 = "{ \"documents\": [  {   \"id\": \"1\",   \"language\": \"en\",   \"text\": \""

            payload_part2 = text
            payload_part3 = "\"  } ]}"
            payload = payload_part1 + payload_part2 + payload_part3
            headers = {
                'x-rapidapi-host': "microsoft-text-analytics1.p.rapidapi.com",
                'x-rapidapi-key': "19125d29f9mshb70843d5cd2b7fcp1da10cjsndbe15b3016e6",
                'content-type': "application/json",
                'accept': "application/json"
                }
            response1 = requests.request("POST", self.sentiment_url, data=payload, headers=headers)
            response = response1.json()

            # print(response['documents'][0]['sentiment'])
            # print(json.dumps(response,sort_keys=True,indent=4))
            return [response['documents'][0]['sentiment'], float(response['documents'][0]['confidenceScores']['negative']),float(response['documents'][0]['confidenceScores']['neutral']),float(response['documents'][0]['confidenceScores']['positive'])]
        except:
            return "No text"

    def char_is_emoji(self,character):
        return character in emoji.UNICODE_EMOJI

    def convert_to_text(self,tweet):
        listTweet = list(tweet)
        newTweet = ""
        for x in range(0,len(listTweet)):
            if(self.char_is_emoji(listTweet[x]) or (not listTweet[x].isalnum() and (listTweet[x] != "/" and listTweet[x] != ' ' and listTweet[x] != "."))):
                listTweet[x] = ""
            newTweet +=  listTweet[x]
        return newTweet
    def fix_tweets(self,tweets):
        noEmojiTweets = []
        for x in range(0,len(tweets)):
            noEmojiTweets.append(self.convert_to_text(tweets[x]))
        return noEmojiTweets

    def twitterUserSentimentCalculator(self,user,number=20):
        tweets = self.recent_tweets(user)
        tweets = self.fix_tweets(tweets)
        tweet_sentiments = []
        total_sentiment = 0
        for x in tweets:
            tweet_sentiments.append(self.sentiment_analyzer(x))

        for x in range(0,len(tweet_sentiments)):
            # print(tweet_sentiments[x][0])
            if tweet_sentiments[x] != "No text":
                if tweet_sentiments[x][2] > tweet_sentiments[x][1] and tweet_sentiments[x][2] > tweet_sentiments[x][3]:
                    total_sentiment += 0
                else:
                    total_sentiment = total_sentiment + (-(tweet_sentiments[x][1]) + tweet_sentiments[x][3])
        return total_sentiment/number
    def stat_interperter(self,number):
        if (number > 0.7):
            return "Very Positive"
        elif(number > 0.4):
            return "Positive"
        elif(number > 0):
            return "Slightly Positive"
        elif(number > -0.4):
            return "Slightly Negative"
        elif(number > -0.7):
            return "Negative"
        else:
            return "Extremely Negative"


if __name__ == '__main__':
    twitterBot = twitterBot()
    sentiment = twitterBot.twitterUserSentimentCalculator("Microsoft")
    print(sentiment)
    print(twitterBot.stat_interperter(sentiment))
    
