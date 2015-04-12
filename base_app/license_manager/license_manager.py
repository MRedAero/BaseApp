__author__ = 'Michael Redmond'

import sys

#TODO: add checks for license
#TODO: add signals to communicate with application that license is or is not valid, for instance the view and controller
#TODO: would need to know when it's not valid


class LicenseManager(object):
    def __init__(self):
        pass

    def check_license(self, *args, **kwargs):

        license_ok = True

        if not license_ok:
            print "License not found!"
            sys.exit()


license_manager = LicenseManager()