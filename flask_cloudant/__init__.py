#!/usr/bin/env python
from flask_cloudant.error import FlaskCloudantException
from requests.exceptions import HTTPError
from cloudant.error import CloudantClientException
from types import DictType

try:
    import cloudant
except ImportError:
    raise FlaskCloudantException(101)

__all__ = ('FlaskCloudant', )
__version__ = '0.0.1.dev'


class FlaskCloudant(object):
    """
    Creates a connection to Cloudant server. Needs a `config.py` file
    with the `CLOUDANT_USER`, `CLOUDANT_PWD` and `CLOUDANT_DB`.
    The `CLOUDANT_ACCOUNT` is optional, if it is not setted, FlaskCloudant
    will use `CLOUDANT_USER` as the account.

    :param str app: Flask app initialized with `Flask(__name__)`.
    """

    CLIENT = None

    def __init__(self, app=None, **kwargs):
        if app is not None:
            self.__init_app__(app)

    def __init_app__(self, app):
        """
        Initializes the connection using the settings from `config.py`.
        """
        cloudant_user = app.config.get('CLOUDANT_USER')
        cloudant_pwd = app.config.get('CLOUDANT_PWD')
        cloudant_account = app.config.get('CLOUDANT_ACCOUNT', cloudant_user)
        cloudant_database = app.config.get('CLOUDANT_DB')

        try:
            FlaskCloudant.CLIENT = cloudant.Cloudant(cloudant_user,
                                                     cloudant_pwd,
                                                     account=cloudant_account)
            self.__connect__()
            self._db = FlaskCloudant.CLIENT[cloudant_database]
            self.__disconnect__()
        except CloudantClientException as ex:
            raise FlaskCloudantException(ex.status_code)
        except HTTPError as ex:
            raise FlaskCloudantException(ex.response.status_code,
                                         cloudant_user)
        except KeyError:
            raise FlaskCloudantException(400, cloudant_database)

    def get(self, document_id):
        """
        Pulls a document from the database using the `document_id`.

        :param str document_id: Document ID used on the database.
        :returns: A `FlaskCloudantDocument` object.
        """
        self.__connect__()
        doc = FlaskCloudantDocument(cloudant.document.Document(self._db,
                                                               document_id))
        self.__disconnect__()
        return doc

    def put(self, content, document_id=None, override=False):
        """
        Creates a document on the database using the
        dictionary passed as paramenter.

        :param dict content: The content of your document.
        :param str document_id: _id for your document.
            Default: None. Cloudant will generate its own _id.
        """
        self.__connect__()
        cloudant_doc = cloudant.document.Document(self._db, document_id)

        if cloudant_doc.exists() and not override:
            raise FlaskCloudantException(405, cloudant_doc['_id'])
        elif cloudant_doc.exists() and override:
            cloudant_doc.fetch()
            cloudant_doc.delete()

        doc = FlaskCloudantDocument(cloudant_doc, exists=False)

        try:
            doc.content(content)
        except AssertionError:
            raise FlaskCloudantException(700, 'Content', DictType)

        doc.save()
        self.__disconnect__()
        return doc

    def delete(self, document_id):
        """
        Delete a document from the database using the `document_id`.

        :param str document_id: Document ID used on the database.
        """
        doc = self.get(document_id)
        self.__connect__()
        doc.delete()
        self.__disconnect__()

    def __connect__(self):
        FlaskCloudant.CLIENT.connect()

    def __disconnect__(self):
        FlaskCloudant.CLIENT.disconnect()


class FlaskCloudantDocument(object):
    """
    Creates a FlaskCloudantDocument. If it exists on the database,
    it will pull the information.
    """

    def __init__(self, cloudant_doc, exists=True):
        if exists:
            if cloudant_doc.exists():
                self.document = cloudant_doc
                self.document.fetch()
            else:
                raise FlaskCloudantException(404, cloudant_doc['_id'])
        else:
            self.document = cloudant_doc

    def __repr__(self):
        return self.document['_id']

    def __str__(self):
        return self.document['_id']

    def content(self, content=None):
        """
        Used to set or get the content of a document.

        :param dict content: Dictionary containing the content to be
            inserted on the document. If the content is `None`, it will
            simply return the content from the current document.
        """
        if content is None:
            return dict(self.document)
        else:
            assert type(content) is DictType
            for key, value in content.iteritems():
                self.document.field_set(self.document, key, value)

    def exists(self):
        FlaskCloudant.CLIENT.connect()
        exists = self.document.exists()
        FlaskCloudant.CLIENT.disconnect()
        return exists

    def save(self):
        """
        Creates the document on the database.
        """
        self.document.create()

    def delete(self):
        """
        Deletes the document from the database.
        """
        self.document.delete()


class FlaskCloudantView(object):
    """
    Creates a FlaskCloudantView.
    """
    pass
