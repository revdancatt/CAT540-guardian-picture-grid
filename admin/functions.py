#!/usr/bin/env python
import simplejson
from google.appengine.api import urlfetch


# This function probably takes the query string args
# and strips them down into a lookup thingy
def get_query_string(qs):
    args = {}
    args_a = qs.split('?')[0]
    if len(args_a) > 0:
        args_a = args_a.split('&')
        for arg in args_a:
            value_pair = arg.split('=')
            if len(value_pair) > 0:
                args[value_pair[0]] = value_pair[1]
    return args


def fetchStories(page, apiKey, direction, settingsJSON):

    fetchUrl = 'http://content.guardianapis.com/search?page=%s&format=json&show-media=picture&api-key=%s' % (page, apiKey)
    result = urlfetch.fetch(url=fetchUrl)
    resultJSON = simplejson.loads(result.content)

    #   Check that we have a response and then go thru all the items
    if 'response' in resultJSON and 'results' in resultJSON['response']:
        latestJSON = resultJSON['response']['results']

        #   If we are going to be *prepending* items that means we want to
        #   be putting newer and newer items at the front, and so we
        #   want to reverse the page of results given to us by the API
        #   so we can add the oldest ones first and the newest ones last
        #   (and therefor at the very front of the list)
        if direction == 'prepend':
            latestJSON.reverse()

        for item in latestJSON:

            #   If we have already have this story (or have already rejected it) skip onto the next one
            if item['apiUrl'] in settingsJSON['stories'] or item['apiUrl'] in settingsJSON['rejects']:
                continue

            #   If there aren't any media assets then we want to reject this item
            if 'mediaAssets' not in item:
                settingsJSON['rejects'][item['apiUrl']] = 1
                settingsJSON['rejectsList'].append(item['apiUrl'])
                continue

            #   See if we can pull out a valid image
            imgUrl = None
            imgCaption = None
            for m in item['mediaAssets']:
                if m['index'] == 1 and m['rel'] == 'body' and 'fields' in m and 'credit' in m['fields'] and 'width' in m['fields'] and 'height' in m['fields'] and int(m['fields']['width']) == 460 and int(m['fields']['height']) == 276:
                    imgUrl = m['file']
                    imgCaption = m['fields']['credit']
                    break

            #   If we didn't find a valid image then bump it here
            if imgUrl is None:
                settingsJSON['rejects'][item['apiUrl']] = 1

                #   Put the record either at the start or end of the list (depending
                #   if we are backfilling, i.e. going back in time, or topping up
                #   i.e. adding the latest).
                if direction == 'append':
                    settingsJSON['rejectsList'].append(item['apiUrl'])
                else:
                    settingsJSON['rejectsList'].insert(0, item['apiUrl'])

                continue

            #   Otherwise, we have an image, lets build the result set here
            newResult = {
                'webTitle': item['webTitle'],
                'webUrl': item['webUrl'],
                'apiUrl': item['apiUrl'],
                'sectionName': item['sectionName'],
                'sectionId': item['sectionId'],
                'imgUrl': imgUrl,
                'imgCaption': imgCaption
            }

            #   store it
            settingsJSON['stories'][item['apiUrl']] = newResult
            #   Put the record either at the start or end of the list (depending
            #   if we are backfilling, i.e. going back in time, or topping up
            #   i.e. adding the latest).
            if direction == 'append':
                settingsJSON['storiesList'].append(item['apiUrl'])
            else:
                settingsJSON['storiesList'].insert(0, item['apiUrl'])

    #   Now we need to trim the results if they are too long
    while len(settingsJSON['storiesList']) > 60:
        apiUrl = settingsJSON['storiesList'].pop()
        del settingsJSON['stories'][apiUrl]

    while len(settingsJSON['rejectsList']) > 100:
        apiUrl = settingsJSON['rejectsList'].pop()
        del settingsJSON['rejects'][apiUrl]

    return
