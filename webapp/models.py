import urllib2
from django.contrib.auth.models import User
from django.db import models


class Plans(models.Model):
    created = models.DateTimeField(auto_now=True)
    plan_name = models.CharField(max_length=100)
    owner = models.ForeignKey(User)
    time_result = models.CharField(max_length=2000)


class Times(models.Model):
    created = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User)
    parent_plan = models.ForeignKey(Plans)
    times = models.CharField(max_length=2000)


class FacebookSessionError(Exception):
    def __init__(self, error_type, message):
        self.message = message
        self.type = error_type

    def get_message(self):
        return self.message

    def get_type(self):
        return self.type

    def __unicode__(self):
        return u'%s: "%s"' % (self.type, self.message)


class FacebookSession(models.Model):

    access_token = models.CharField(max_length=350, unique=True)
    expires = models.IntegerField(null=True)

    user = models.ForeignKey(User, null=True)
    uid = models.BigIntegerField(unique=True, null=True)

    class Meta:
        unique_together = (('user', 'uid'), ('access_token', 'expires'))

    def query(self, object_id, connection_type=None, metadata=False):
        import urllib
        import json

        url = 'https://graph.facebook.com/%s' % object_id
        if connection_type:
            url += '/%s' % connection_type
        params = {'access_token': self.access_token}
        if metadata:
            params['metadata'] = 1

        url += '?' + urllib.urlencode(params)

        response = json.loads(urllib2.urlopen(url).read())

        if 'error' in response:
            error = response['error']
            raise FacebookSessionError(error['type'], error['message'])

        return response

