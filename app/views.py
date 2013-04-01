from django.shortcuts import render_to_response
from social_auth.models import UserSocialAuth


# build the api
from apiclient.discovery import build
from oauth2client.client import AccessTokenCredentials

import json 
import httplib2

def home(request):
    return render_to_response("main.html")

def loggedin(request):
    # retrieve the token first 
    access_token = UserSocialAuth.get_social_auth_for_user(request.user).get().tokens['access_token']

    # OAuth dance
    credentials = AccessTokenCredentials(access_token, 'my-user-agent/1.0')
    http = httplib2.Http()
    http = credentials.authorize(http)
    service = build('calendar', 'v3', http=http)


    # Snippet that lists all calendar events
    #request = service.events().list(calendarId='primary')
    
    #while request != None:
      ## Get the next page.
      #response = request.execute()
      ## Accessing the response like a dict object with an 'items' key
      ## returns a list of item objects (events).
      #for event in response.get('items', []):
        ## The event object is a dict object with a 'summary' key.
        #print repr(event.get('summary', 'NO SUMMARY')) + '\n'
      ## Get the next request object by passing the previous request object to
      ## the list_next method.
      #request = service.events().list_next(request, response)

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


    #payload = json.dumps(event)

    created_event = service.events().insert(calendarId='primary', body=event).execute()

    #response = urlfetch.fetch(
        #"https://www.google.com/calendar/feeds/default/private/full",
        #method=urlfetch.POST,
        #payload=payload,
        #headers = {"Content-Type": "application/json",
                   #"Authorization": "OAuth " + tokens})

    #if response.status_code == 201:
        #result = simplejson.loads(response.content)
        #logging.info("Status code was %s, and the returned event looks like %s", response.status_code, result)
        #return
    #raise Exception("Call failed. Status code %s. Body %s",
                #response.status_code, response.content)


    return render_to_response("logged-in.html", {'tokens': tokens})



