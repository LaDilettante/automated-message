import tweepy
from twilio.rest import TwilioRestClient
import time, datetime
import pytz

import webapp2
from google.appengine.ext import ndb

class Message(ndb.Model): 
    text = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    twitter_user = ndb.StringProperty()
    twitter_date = ndb.DateTimeProperty()

class Messenger(webapp2.RequestHandler):

    def get(self):
        self.send_message()
        self.response.out.write(self.print_messages())

    def send_message(self):
        from passwords import consumer_key, consumer_secret, access_token, access_token_secret, \
            ACCOUNT_SID, AUTH_TOKEN, myTwilioNumber, myCellPhone
            
        # Scrape Twitter
        consumer_key = consumer_key
        consumer_secret = consumer_secret
        access_token = access_token
        access_token_secret = access_token_secret
        
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)


        screen_name = 'romanticmsgs'
        latest_tweet = api.user_timeline(screen_name = screen_name, count=1)[0]

        # Send message
        ACCOUNT_SID = ACCOUNT_SID
        AUTH_TOKEN = AUTH_TOKEN
        twilio_client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
        myTwilioNumber = myTwilioNumber
        myCellPhone = myCellPhone

        # Check if the latest tweet is newer than the latest sent message
        if Message.query().get() is None or Message.query().order(-Message.date).get().date < latest_tweet.created_at:

            # Does not send during sleep hours
            timezone = 'US/Eastern'
            if not 0 <= datetime.datetime.now(pytz.timezone(timezone)).hour <= 10:
                message = Message(text=latest_tweet.text + '- QA', 
                    twitter_user=latest_tweet.user.screen_name, 
                    twitter_date=latest_tweet.created_at)
                message_sent = twilio_client.messages.create(body=message.text, 
                    from_=myTwilioNumber, to=myCellPhone)
                message.put()
                self.response.out.write(
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + 
                    message.text + ". Sent<br>"
                )
            else:
                self.response.out.write(
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + 
                    "She's sleeping.<br>"
                )
        else:
            self.response.out.write(
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + 
                "No new message.<br>")


    def print_messages(self):
        s = "All messages:<br>"
        for message in Message.query().fetch():
            s += datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + \
                message.text + "<br>"
        return s

app = webapp2.WSGIApplication([
        ('/', Messenger)
], debug=True)

def main():
    app.run()

if __name__ == '__main__':
    main()