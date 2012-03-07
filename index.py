#!/usr/bin/env python
import os
import sys
import simplejson

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import util

from admin.models import Settings


class MainHandler(webapp.RequestHandler):
    def get(self):

        # build an empty template_values object that we can stuff full
        # of handy information and so on
        template_values = {
          'msg': 'Hello World',
        }

        #   grab the settings file
        #   TODO: put this into memcache
        settingsRows = Settings.all()

        #   If we don't have the settings file, then we need to
        #   take the user to the settings page
        if settingsRows.count() == 0:
            path = os.path.join(os.path.dirname(__file__), 'templates/setup.html')
            self.response.out.write(template.render(path, template_values))
        else:

            #   Grab the JSON out of the settings row
            settingsJSON = simplejson.loads(settingsRows[0].json)

            #   If we don't have enough stories then we need to go to the
            #   setup page and let it carry on backfilling
            if len(settingsJSON['storiesList']) < 60:
                template_values['backfilling'] = True
                template_values['backfill'] = len(settingsJSON['storiesList'])
                path = os.path.join(os.path.dirname(__file__), 'templates/setup.html')
                self.response.out.write(template.render(path, template_values))
            else:
                template_values['settingsJSON'] = settingsJSON
                path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
                self.response.out.write(template.render(path, template_values))


def main():
    application = webapp.WSGIApplication([('/', MainHandler)], debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
