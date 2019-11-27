import tweepy

with open("TMM_Project/private/tokens.txt") as tokens:
    consumer_token, consumer_secret, access_token, access_secret = tokens.readline().split(" ")
    tokens.close()

auth_handler = tweepy.OAuthHandler(consumer_token, consumer_secret)
auth_handler.set_access_token(access_token, access_secret)
api = tweepy.API(auth_handler)

l = 0
for tweet in tweepy.Cursor(api.search, q='#HimToo').items():
    l +=1
print(l) # Retrieves 122 tweets
