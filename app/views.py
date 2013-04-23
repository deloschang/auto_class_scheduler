from django.shortcuts import render_to_response
from django.template import RequestContext
from social_auth.models import UserSocialAuth

from django.contrib.auth.decorators import login_required


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

from django.utils.html import strip_tags # sanitize

# extra
import datetime
from datetime import timedelta
from random import randint
import random



# if logged in already, redirect to the main
def home(request):
    try: 
        link = UserSocialAuth.get_social_auth_for_user(request.user).get().tokens
        access_token = link['access_token']

        return render_to_response("logged-in.html", {'access_token': access_token}, RequestContext(request))

    except:
        return render_to_response("main.html", RequestContext(request))

@login_required
def loggedin(request):
    try: 
        link = UserSocialAuth.get_social_auth_for_user(request.user).get().tokens

        access_token = link['access_token']

        # OAuth dance
        #credentials = AccessTokenCredentials(access_token, 'my-user-agent/1.0')
        #http = httplib2.Http()
        #http = credentials.authorize(http)
        #service = build('calendar', 'v3', http=http)


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
        #event = {
          #'summary': "summary",
          #'description': "description",
          #'start' : { 'dateTime' : "2013-04-01T15:00:00.000Z"},
          #'end' : { 'dateTime' : "2013-04-01T17:00:00.000Z"}
        #}


        #payload = json.dumps(event)

        #created_event = service.events().insert(calendarId='primary', body=event).execute()

        #print "Created Event: %s" % created_event['id']
        return render_to_response("logged-in.html", RequestContext(request))

    except: 
        return render_to_response("main.html", RequestContext(request))

def tutorial_class_input(request):
    global SAVE_DUE_DATE
    global SAVE_CLASS_NAME
    global SAVE_TIME_TO_FINISH
    global SIZE

    # Tutorial: user just entered class
    if request.method == 'POST':
        class_name = strip_tags(request.POST['class_name'])
        try:
            info = class_name.split(' ')

            dept_abbr = info[0]
            coursenum = info[1]

            # scrape for the class period
            user = request.user
            response = find_class_period(dept_abbr, coursenum)
        except:
            error = 'Invalid class! Please enter full dept name and number. E.g.: COSC 050'
            return render_to_response("logged-in.html", {'error':error}, RequestContext(request))

        period = response[0]
        class_title = response[1]

        # found class time, now process and add to the calendar
        insert_to_calendar(user, class_name, period)


        # extra
        due_date = random_date(datetime.datetime.now() + timedelta(2),datetime.datetime.now() + timedelta(5)) 
        SAVE_DUE_DATE = due_date # save in global for now
        SAVE_CLASS_NAME = class_name

        due_date_formatted = due_date.strftime('%m/%d')

        size = random.randrange(40,103)
        time_to_finish = random.randrange(4,10)
        SAVE_TIME_TO_FINISH = time_to_finish
        SIZE = str(size)

        return render_to_response("confirmation.html", 
                {'class_name':class_name, 'period':period, 'class_title':class_title, 
                    'due_date':due_date_formatted, 'size':size, 'time_to_finish':time_to_finish}, RequestContext(request))



def add_estimate(request):
    # grab access token
    link = UserSocialAuth.get_social_auth_for_user(request.user).get().tokens
    access_token = link['access_token']

    # OAuth dance
    credentials = AccessTokenCredentials(access_token, 'my-user-agent/1.0')
    http = httplib2.Http()
    http = credentials.authorize(http)
    service = build('calendar', 'v3', http=http)

    
    # initialize globals
    due_date = SAVE_DUE_DATE - timedelta(1)
    due_date_format = due_date.strftime('%Y-%m-%d')

    size = SIZE
    time_to_finish = SAVE_TIME_TO_FINISH
    class_name = SAVE_CLASS_NAME
    
    offset = random.randrange(1,3) # time to work
    assignment_number = random.randrange(2,5)
    time_left = time_to_finish - offset

    reasons = ['Open Time', 'Usually @ Library', 'Usual Study Time', 'Most Productive']
    end_time_saved = []

    while (due_date - datetime.datetime.now()) > timedelta (minutes = 0) and time_left > 0:


        # generate random time...
        random_min = random.randrange(0,59)
        random_hour = random.randrange(15,20) # from 3pm to 11pm

        random_min_format = str(random_min).zfill(2)
        random_hour_format = str(random_hour).zfill(2)

        end_time = random_hour + offset
        end_time_format = str(end_time).zfill(2)

        # working event
        event = {
          'summary': class_name + " Assignment " + assignment_number,
          'description': size + " students spent avg. " + time_to_finish + " hrs to complete.",
          'start' : { 'dateTime' : due_date_format + "T"+random_hour_format+":"+random_min_format+":00.000",
              'timeZone' : 'America/New_York'
          },
          'end' : { 'dateTime' : due_date_format + "T"+end_time_format+":"+random_min_format+":00.000",
              'timeZone' : 'America/New_York'}
        }
        
        # insert prediction time
# demo: calendar ID for 'Estimates-Timely'
        created_event = service.events().insert(calendarId='2i4qubb29vdurj8qntlklsdvp4@group.calendar.google.com', body=event).execute()
        print created_event['id']

        due_date = due_date - timedelta(1)
        due_date_format = due_date.strftime('%Y-%m-%d')

        # recalc offset
        offset = random.randrange(1,4) # time to work
        time_left -= offset

        # if the offset puts time_left negative, finish off the time_left as a bulk
        #if time_left < 0:
            #offset = time_left

        # save the random time to display info about...

        reason_index = random.randrange(0,3)
        end_time_saved.append(due_date.strftime('%m-%d') + " : " + random_hour_format + ":" + random_min_format + " - " + end_time_format + ":" + random_min_format + " ( " + reasons[reason_index] + " )" )


    return render_to_response("estimateconfirmation.html", 
            {'class_name':class_name, 'due_date_saved':SAVE_DUE_DATE.strftime('%m-%d'), 
                'end_time_saved':end_time_saved}, RequestContext(request))
    



def random_date(start, end):
    return start + timedelta(
        seconds=randint(0, int((end - start).total_seconds())))



# user to schedule for
# class_name e.g. ART 1
def insert_to_calendar(user, class_name, period):
    # grab access token
    link = UserSocialAuth.get_social_auth_for_user(user).get().tokens
    access_token = link['access_token']

    # OAuth dance
    credentials = AccessTokenCredentials(access_token, 'my-user-agent/1.0')
    http = httplib2.Http()
    http = credentials.authorize(http)
    service = build('calendar', 'v3', http=http)


    # short-circuit special arrangements
    if period.encode('utf-8') == 'AR':
        return

    # check the date and time for this period
    response = check_period_time(period)

    # create the event
    #event = {
      #'summary': class_name,
      #'description': class_name,
      #'start' : { 
          #'dateTime' : "2013-04-01T15:00:00.000",
          #'timeZone' : "Europe/Zurich"
      #},
      #'end' : { 
          #'dateTime' : "2013-04-01T17:00:00.000",
          #'timeZone' : "Europe/Zurich"
      #},
      #'recurrence' : [
          #'RRULE:FREQ=WEEKLY;BYDAY=Mo,We,Fr;UNTIL=20130603',
      #],
    #}

    # insert class
    event = {
      'summary': class_name,
      'description': class_name,
      'start' : { 
          'dateTime' : "2013-03-25T"+response[1],
          'timeZone' : "America/New_York"
      },
      'end' : { 
          'dateTime' : "2013-03-25T"+response[2],
          'timeZone' : "America/New_York"
      },
      'recurrence' : [
          'RRULE:FREQ=WEEKLY;BYDAY='+response[0]+';UNTIL=20130529',
      ],
    }

    try: 
        # demo: add to "Classes-Timely"
        # calendar ID for "Classes - Timely"
        created_event = service.events().insert(calendarId='hskbfmkfc5dhbb517ih1r11gjs@group.calendar.google.com', body=event).execute()
    except:
        # default to primary
        created_event = service.events().insert(calendarId='primary', body=event).execute()

    print "Created Event: %s" % created_event['id']

def check_period_time(period):
    # maybe parse from the link in the future?

    response = []

    period = period.encode('utf-8')

    ## list of classes
    if period == '12':
        response.insert(0, "Mo,We,Fr")
        response.insert(1, "12:30:00.000")
        response.insert(2, "13:35:00.000")

    elif period == '9L': 
        response.insert(0, "Mo,We,Fr")
        response.insert(1, "8:45:00.000")
        response.insert(2, "9:50:00.000")

    elif period == '10':
        response.insert(0, "Mo,We,Fr")
        response.insert(1, "10:00:00.000")
        response.insert(2, "11:05:00.000")
        
    elif period == '11':
        response.insert(0, "Mo,We,Fr")
        response.insert(1, "11:15:00.000")
        response.insert(2, "12:20:00.000")

    elif period == '2':
        response.insert(0, "Mo,We,Fr")
        response.insert(1, "13:45:00.000")
        response.insert(2, "14:50:00.000")

    elif period == '10A':
        response.insert(0, "Tu,Th")
        response.insert(1, "10:00:00.000")
        response.insert(2, "11:50:00.000")

    elif period == '2A':
        response.insert(0, "Tu,Th")
        response.insert(1, "14:00:00.000")
        response.insert(2, "15:50:00.000")

    elif period == '8':
        response.insert(0, "Mo,Tu,Th,Fr")
        response.insert(1, "7:45:00.000")
        response.insert(2, "8:35:00.000")

    elif period == '9S':
        response.insert(0, "Mo,Tu,Th,Fr")
        response.insert(1, "9:00:00.000")
        response.insert(2, "9:50:00.000")

    # 3A 
    elif period == '3B':
        response.insert(0, "Tu,Th")
        response.insert(1, "4:00:00.000")
        response.insert(2, "5:50:00.000")
    # handle the edge case with manually entered date times

    return response




# helper that scrapes for the class period
def find_class_period(dept_abbr, course_num):
    response = []

    # define
    post_data = {
            'classyear' : '2008', # why??
            'subj': dept_abbr,
            'crsenum': course_num,
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
    tbody = soup.find('th', text='Term').parent.parent.parent
    cells = tbody.findAll('tr')[2]('td')

    # sometimes there is a listing like Tu 3:00PM-6:00PM.
    try: 
        period = cells[7].contents[0].contents[0]
    except AttributeError:
        period = cells[7].contents[0]

    class_name = cells[5].contents[0].contents[0].encode('utf-8')
    
    #enrolled = int(cells[-2].contents[0])
    #capacity = int(cells[-3].contents[0])
    #available = capacity - enrolled
    #print "%i spaces left (capacity of %i with %i enrolled)" % (available, capacity, enrolled)

    response.insert(0, period)
    response.insert(1, class_name)


    return response
    


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
# scrapes the entire course listing (in case we want to load it into the database)
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

    parsed = tbody.findAll('tr')

    # loop through each item 
    for i in range(1, len(parsed)):
        cells = parsed[i]('td')

        # sometimes the dept isn't hyperlinked
        try:
            subj = cells[2].contents[0].contents[0]
        except AttributeError:
            subj = cells[2].contents[0]

        coursenum = cells[3].contents[0]
        title = cells[6].contents[0].contents[0]

        # sometimes there is a listing like Tu 3:00PM-6:00PM.
        try: 
            period = cells[8].contents[0].contents[0]
        except AttributeError:
            period = cells[8].contents[0]

        print subj
        print coursenum
        print title
        print period

    return render_to_response("scraper.html", {'soup': title})


    



