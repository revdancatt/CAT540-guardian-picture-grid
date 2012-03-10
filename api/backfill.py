#!/usr/bin/env python
import os
import simplejson

from admin.models import Settings
from admin.functions import get_query_string, fetchStories

args = get_query_string(os.environ['QUERY_STRING'])
if 'page' not in args:
    statusJSON = {'status': 'error', 'msg': 'no page parameter passed'}
else:

    #   Get the settings file, if there isn't one then throw an error
    settingsRows = Settings.all()

    if settingsRows.count() == 0:
        statusJSON = {'status': 'error', 'msg': 'no settingsJSON record'}
    else:
        #   Now we need to grab the API key and go fetch a whole bunch
        #   of stories from the Guardian
        apiKey = settingsRows[0].apiKey
        settingsJSON = simplejson.loads(settingsRows[0].json)

        #   go and top up the settingsJSON with a bunch of stories
        fetchStories(int(args['page']), apiKey, 'append', settingsJSON)

        #   Now we need to put the data back into the database
        storeRow = settingsRows[0]
        storeRow.json = simplejson.dumps(settingsJSON)
        storeRow.put()

        statusJSON = {'status': 'ok', 'msg': len(settingsJSON['storiesList'])}


print 'Content-Type: application/json; charset=UTF-8'
print ''
print simplejson.dumps(statusJSON)
