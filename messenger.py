import tweepy
from twilio.rest import TwilioRestClient
import time, datetime

import webapp2
from google.appengine.ext import ndb

class Message(ndb.Model): 
    text = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    twitter_user = ndb.StringProperty()
    twitter_date = ndb.DateTimeProperty()

    @classmethod
    def query(cls, date):
        return cls.query(date=date).order(-cls.date)

class Messenger(webapp2.RequestHandler):

    def get(self):
        self.send_message()
        self.response.out.write(self.print_messages())

    def send_message(self):
        # Scrape Twitter
        consumer_key='1NtqH9qnMgzcK82RemH28g'
        consumer_secret='mwpGgnqSVAoRKrOGnFYZy0CUnrZe2hZcmEfk8NkgT5g'
        access_token='1550021167-j87u9Mwzt2FYeowViGkoNpXZQ6mDlGs6iRaVKtc'
        access_token_secret='OZVtiSII8zHT8Xk2eSk2XekZWN3V11KhjOwcqh6fg'
        
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)


        screen_name = 'romanticmsgs'
        latest_tweet = api.user_timeline(screen_name = screen_name, count=1)[0]

        # Send message
        # accountSID = 'ACc621084ad6077b28d99f73db023a2162'
        # authToken = '0b985eb7ccbc935bdfd474806dff1eb2'
        # twilio_client = TwilioRestClient(accountSID, authToken)
        # myTwilioNumber = ''
        # myCellPhone = '+18607595666'

        ACCOUNT_SID = "AC7a56e4b84af6661e2e26f7635cecbc56" 
        AUTH_TOKEN = "388c4d360b45093df23313b645a564cf" 
        twilio_client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
        myTwilioNumber = '+18329813253'
        myCellPhone = '+19195251603'

        message = Message(text=latest_tweet.text + '- QA', 
            twitter_user=latest_tweet.user.screen_name, 
            twitter_date=latest_tweet.created_at)
        message_sent = twilio_client.messages.create(body=message.text, 
            from_=myTwilioNumber, to=myCellPhone)
        message.put()

    def print_messages(self):
        s = "All messages:<br>"
        for message in Message.all():
            s += message.date + message.text + "<br>"
        return s

app = webapp2.WSGIApplication([
        ('/', Messenger)
], debug=True)

def main():
    app.run()

if __name__ == '__main__':
    main()