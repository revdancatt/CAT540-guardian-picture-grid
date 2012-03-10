#!/usr/bin/env python
import os
import simplejson
from admin.models import Settings
from google.appengine.api import memcache
from admin.functions import get_query_string

args = get_query_string(os.environ['QUERY_STRING'])

memkey = 'settings'

itemsRows = memcache.get(memkey)
if itemsRows is None:
    itemsRows = Settings.all()
    memcache.add(memkey, itemsRows, 60 * 1)

if itemsRows.count() == 0:
    newResults = {'stat': 'error'}
else:
    results = simplejson.loads(itemsRows[0].json)
    del results['rejects']
    del results['rejectsList']

    #   TODO: validate limit in args as positive numerical
    if 'limit' in args:
        newStories = {}
        newStoriesList = []
        for i in range(int(args['limit'])):
            newStories[results['storiesList'][i]] = results['stories'][results['storiesList'][i]]
            newStoriesList.append(results['storiesList'][i])

        results['stories'] = newStories
        results['storiesList'] = newStoriesList

    newResults = {'stat': 'ok', 'results': results}

print 'Cache-Control: public,max-age=60'
print 'Content-Type: application/json; charset=UTF-8'
print ''
print simplejson.dumps(newResults)
