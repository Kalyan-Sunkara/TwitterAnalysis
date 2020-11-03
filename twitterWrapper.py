import json
import requests
import os



class twitterWrap:
    def __init__(self):
        self.auth = XXXXXXXXXXXX

    #pass in a twitter usernames and returns the unique ids for the users
    def get_user_id(self,usernames):
        # url = "https://api.twitter.com/2/users?ids="
        list_of_ids = []
        for x in usernames:
            url = "https://api.twitter.com/2/users/by/username/"
            url = url + x
            results = requests.get(url, headers={"Authorization":self.auth})
            searches = results.json()
            list_of_ids.append(searches["data"]["id"])
        return list_of_ids

    #pass in a list of twitter usernames and returns information on the usernames
    def user_info(self,usernames):
        url = "https://api.twitter.com/2/users/by?usernames="
        for x in usernames:
            if x != usernames[len(usernames)-1]:
                url = url + x + ","
            else:
                url = url + x
        url = url + "&expansions=pinned_tweet_id"
        url = url + "&user.fields=public_metrics"

        results = requests.get(url, headers={"Authorization":self.auth})
        searches = results.json()
        return searches

if __name__ == '__main__':
    twitterBot = twitterWrap()
    list_of_users = ["lilbaby4PF", "1lilgotit"]
    print(json.dumps(twitterBot.user_info(list_of_users),sort_keys=True,indent=4))
