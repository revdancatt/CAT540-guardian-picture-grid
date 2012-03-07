#!/usr/bin/env python
import os
import simplejson

from admin.models import Settings
from admin.functions import get_query_string

args = get_query_string(os.environ['QUERY_STRING'])

if 'apiKey' not in args:
    statusJSON = {'status': 'error', 'msg': 'you need to pass an apiKey. ?apiKey=xxxxxx'}
else:
    #   We need to check that we don't already have the data in the database as
    #   we don't want people to overwrite what we already have, yup, that's right
    #   once we've made a selection there's no going back unless we either blow
    #   away the database, or go in by hand and update it
    settingsRows = Settings.all()

    if settingsRows.count() == 0:
        newJSON = {
            'stories': {},
            'storiesList': [],
            'rejects': {},
            'rejectsList': []
        }

        #   Now put it into the database
        settingsRow = Settings()
        settingsRow.apiKey = args['apiKey']
        settingsRow.json = simplejson.dumps(newJSON)
        settingsRow.put()

        statusJSON = {'status': 'ok', 'results': newJSON}

    else:

        statusJSON = {'status': 'error', 'msg': 'already have a settingsJSON record'}

print 'Content-Type: application/json; charset=UTF-8'
print ''
print simplejson.dumps(statusJSON)
