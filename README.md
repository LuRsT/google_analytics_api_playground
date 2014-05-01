google_analytics_api_playground
===========================

Extremely hacky sandbox for playing around with google analytics API

Useful links:

* http://ga-dev-tools.appspot.com/explorer/
* https://developers.google.com/analytics/devguides/reporting/core/dimsmets#view=detail&group=event_tracking

## Before you use this

    mkvirtualenv google_analytics_api_playground
    pip install -r requirements.txt

Then you need to get the `client_secrets.json` as explained [here](https://developers.google.com/analytics/solutions/articles/hello-analytics-api#register_project)
and put it in the same directory as this project, by running the `reporting.py`
script, it will prompt you to authorize access to the Google Analytics Data.

After accepting it, you will have an `analytics.dat` file in your directory
which will make the script not bother you about auth again.

## Using

The script `reporting.py` is used to filter event tracking on google analytics,
here is an example for it's use:

    python reporting.py ga:1111111 'Event Action' 'Event Label'

## Disclaimer:

This is super hacky and I do not garantee that it will work, I strongly recommend
getting the google's [sample tools](https://code.google.com/p/google-api-python-client/source/browse/#hg%2Fsamples%2Fanalytics).

They might be able to help you get your head around their API better than this script.

You've been warned
