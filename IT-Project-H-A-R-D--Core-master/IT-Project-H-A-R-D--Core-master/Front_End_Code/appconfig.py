
import os

CSRF_ENABLED = True

# OpenID Providers

OPENID_PROVIDERS = [
    { 'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id' },
    { 'name': 'Yahoo', 'url': 'https://me.yahoo.com' },
    { 'name': 'AOL', 'url': 'http://openid.aol.com/<username>' },
    { 'name': 'Flickr', 'url': 'http://www.flickr.com/<username>' }]

# Mail server settings

MAIL_SERVER   = 'localhost'
MAIL_PORT     = 25
MAIL_USERNAME = None
MAIL_PASSWORD = None

# Administrator list

ADMINS = ['joe@example.com']


