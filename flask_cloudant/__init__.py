#!/usr/bin/env python
from error import FlaskCloudantException
from requests.exceptions import HTTPError

try:
    import cloudant
except ImportError:
    raise FlaskCloudantException(101)

__all__ = ('FlaskCloudant', )
__version__ = '0.0.1.dev'

class FlaskCloudant(object):

    def __init__(self, app=None, config_name='CLOUDANT', **kwargs):
        self.config_name = config_name

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        cloudant_user = app.config.get('{0}_USER'.format(self.config_name))
        cloudant_pwd = app.config.get('{0}_PWD'.format(self.config_name))
        cloudant_account = app.config.get('{0}_ACCOUNT'
                                          .format(self.config_name),
                                          cloudant_user)
        cloudant_database = app.config.get('{0}_DB'.format(self.config_name))

        self.connect(cloudant_user, cloudant_pwd,
                     cloudant_account, cloudant_database)


    def connect(self, user, pwd, account, db):
        try:
            self._client = cloudant.Cloudant(user, pwd, account=account)
            self._client.connect()
            self._db = self._client[db]
            self._client.disconnect()
        except HTTPError as ex:
            raise FlaskCloudantException(ex.response.status_code, user)
        except KeyError:
            raise FlaskCloudantException(400, db)
