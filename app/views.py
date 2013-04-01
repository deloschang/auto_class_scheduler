from django.shortcuts import render_to_response
from social_auth.models import UserSocialAuth


# build the api
from apiclient.discovery import build
from oauth2client.client import AccessTokenCredentials

import json 
import httplib2


# scraper
import urllib
import urllib2
import cookielib
from html5lib import HTMLParser, treebuilders


def home(request):
    return render_to_response("main.html")

def loggedin(request):
    link = UserSocialAuth.get_social_auth_for_user(request.user).get().tokens

    # retrieve the token first 
    if 'access_token' in link:
        access_token = link['access_token']

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

        #except AccessTokenRefreshError:
        ## The AccessTokenRefreshError exception is raised if the credentials
        ## have been revoked by the user or they have expired.
        #print ('The credentials have been revoked or expired, please re-run'
               #'the application to re-authorize')

        # working event
        event = {
          'summary': "summary",
          'description': "description",
          'start' : { 'dateTime' : "2013-04-01T15:00:00.000Z"},
          'end' : { 'dateTime' : "2013-04-01T17:00:00.000Z"}
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


        print "Created Event: %s" % created_event['id']
        return render_to_response("logged-in.html", {'access_token': access_token})

    else: 
        return render_to_response("main.html")

# course-watch modified scraper
def scraper(request):
    post_data = {
            'classyear' : '2008', # why??
            'subj': 'COSC',
            'crsenum': '50'
        }
    url = 'http://oracle-www.dartmouth.edu/dart/groucho/timetable.course_quicksearch'

    
    # scrape the html
    cj = cookielib.LWPCookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)
    headers =  {'User-agent' : 'Mozilla/c.0 (compatible; MSIE 5.5; Windows NT)'}
    request = urllib2.Request(url, urllib.urlencode(post_data), headers)
    handle = urllib2.urlopen(request)
    html = handle.read()

    # parse for the dept and course number
    parser = HTMLParser(tree=treebuilders.getTreeBuilder("beautifulsoup"))
    soup = parser.parse(html)
    #tbody = soup.find('th', text='Term').parent.parent.parent
    #soup = tbody.findAll('tr')[2]('td')
    

    return render_to_response("scraper.html", {'soup': soup})

# tidying: http://valet.htmlhelp.com/tidy/tidy.cgi
def scraper2(request):
    #url = 'http://oracle-www.dartmouth.edu/dart/groucho/timetable.display_courses'
    #parameters = 'crnl=no_value&distribradio=alldistribs&depts=no_value&periods=no_value&distribs=no_value&distribs_i=no_value&distribs_wc=no_value&pmode=public&term=&levl=&fys=n&wrt=n&pe=n&review=n&classyear=2008&searchtype=Subject+Area%28s%29&termradio=selectterms&terms=no_value&terms=201303&subjectradio=allsubjects&hoursradio=allhours&sortorder=dept'

    #headers = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        #"Accept-Encoding":"gzip, deflate",
        #"Accept-Language":"en-US,en;q=0.5",
        #"Connection":"keep-alive",
        #"Host":"oracle-www.dartmouth.edu",
        #"Referer":"http://oracle-www.dartmouth.edu/dart/groucho/timetable.subject_search",
        #"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:19.0) Gecko/20100101 Firefox/19.0"
    #}
	
    #req = urllib2.Request(url, parameters, headers)
    #response = urllib2.urlopen(req)

    #html = response.read()
    ## parse for the dept and course number
    #parser = HTMLParser(tree=treebuilders.getTreeBuilder("beautifulsoup"))
    #soup = parser.parse(html)

    # no need to keep scraping.
    html = open('spring2013_scraped.txt', 'r')
    parser = HTMLParser(tree=treebuilders.getTreeBuilder("beautifulsoup"))
    soup = parser.parse(html)
    tbody = soup.find('th', text='Term').parent.parent.parent
    
    return render_to_response("scraper.html", {'soup': tbody})


    



