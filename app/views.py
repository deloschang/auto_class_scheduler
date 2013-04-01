from django.shortcuts import render_to_response
from social_auth.models import UserSocialAuth


import json 
import urllib2

def home(request):
    return render_to_response("main.html")

def loggedin(request):
    # retrieve the token first 
    tokens = UserSocialAuth.get_social_auth_for_user(request.user).get().tokens


    # adding test event
    event = {"data":{
        "title": "Test Event",
        "details": "Details of test event",
        "transparency": "opaque",
        "status": "confirmed",
        "location": "My Place",
        "when": [{
            "start": "2013-04-01T15:00:00.000Z",
            "end": "2013-04-01T17:00:00.000Z"
            }]
        }
    }
    payload = json.dumps(event)

    response = urlfetch.fetch(
        "https://www.google.com/calendar/feeds/default/private/full",
        method=urlfetch.POST,
        payload=payload,
        headers = {"Content-Type": "application/json",
                   "Authorization": "OAuth " + tokens})

    if response.status_code == 201:
        result = simplejson.loads(response.content)
        logging.info("Status code was %s, and the returned event looks like %s", response.status_code, result)
        return
    raise Exception("Call failed. Status code %s. Body %s",
                response.status_code, response.content)


    return render_to_response("logged-in.html", {'tokens': tokens})
    

