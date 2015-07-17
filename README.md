# automated-message
Check Twitter update for romantic messages (@romanticmsgs) and SMS them to your loved ones

- `Tweepy` to pull message from Twitter (`python-twitter` does not work when hosted on Google App Engine)
- `Twilio` to send SMS message
- Script is hosted on Google App Engine with a cron job

## How to Deploy

#### Sign up with Twitter's API
1. Follow [this quick guide](http://www.gabfirethemes.com/create-twitter-api-key/) to get Twitter's API key

#### Sign up with Twilio's API
1. Follow [this quick guide](https://automatetheboringstuff.com/chapter16/) on how to sign up and use `Twilio` (Ctrl-F "Signing up for a Twilio Account")
2. The trial `Twilio` account will preface your SMS with "Sent from trial account". You can pay (a little) to remove this restriction

#### Create a `passwords.py` file in the project root folder
1. In this folder, write down the credentials from your Twitter and Twilio account. (My own `passwords.py` is included in `.gitignore` so that it doesn't show up on github.)
2. Like so

```python
# Twitter API credentials
consumer_key = 'your_own_credentials'
consumer_secret = 'your_own_credentials'
access_token = 'your_own_credentials'
access_token_secret = 'your_own_credentials'

# Twilio API credentials
ACCOUNT_SID = 'your_own_credentials'
AUTH_TOKEN = 'your_own_credentials'

# Twilio phone number
myTwilioNumber = '+18885553333'
myCellPhone = '+12229993333'
```

#### Deploy on Google App Engine
1. Follow the [Google App Engine (GAE)'s Python tutorial](https://cloud.google.com/appengine/docs/python/gettingstartedpython27/introduction) to download GAE Python SDK
2. Follow [GAE's tutorial](https://cloud.google.com/appengine/docs/python/gettingstartedpython27/uploading) on how to upload your application. TL;DR: `appcfg.py -A PROJECT_NAME update automated-message`
3. Go to http://console.developers.google.com to monitor your application

## Configuration
1. Change the Twitter source: In `messenger.py`, change `screen_name = 'romanticmsgs'screen_name = 'romanticmsgs'` to use any other Twitter user as source
2. Change the frequency of checking Twitter for updates in `cron.yaml`. See [GAE's docs](https://cloud.google.com/appengine/docs/python/config/cron) on cron's syntax
3. Change the hours NOT to send message: In `messenger.py` > `# Does not send during sleep hours`

## Troubleshoot

> Failed to send request: The Socket API will be enabled for this application once billing has been enabled in the admin console.

We need to enable billing for our GAE's app for `Tweepy` and `Twilio` API to work, as follows. In http://console.developers.google.com, 
- go to `Settings (the cog symbol, top right) > Billing Accounts` to add payment methods to your GAE account
- go to `Settings > Project Billing Settings` to enable billing for this particular project
