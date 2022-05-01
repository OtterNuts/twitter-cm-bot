import tweepy
import logging

logger = logging.getLogger()


class TwitterClient:
    def __init__(self):
        self.consumer_key = ""
        self.consumer_secret = ""
        self.access_token = ""
        self.access_token_secret = ""

    def tweeter_auth(self):
        # Authenticate to Twitter
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)

        # Create API object
        client = tweepy.API(auth, wait_on_rate_limit=True)
        try:
            client.verify_credentials()
        except Exception as e:
            logging.error("Error creating API", exc_info=True)
            raise e
        print("API created")

        return client
