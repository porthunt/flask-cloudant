#!/usr/bin/env python
'''
Unit tests.
'''

import flask
import uuid
from flask_cloudant import FlaskCloudant
from flask_cloudant.error import FlaskCloudantException
import pytest

@pytest.fixture
def app():
    _app_ = flask.Flask(__name__)
    _app_.config.from_object('credentials')
    storage = FlaskCloudant(_app_)
    return storage

@pytest.fixture
def doc(app):
    doc = app.put({'test': uuid.uuid4().hex})
    return doc.content()['_id']

def test_get_existing(app, doc):
    doc_file = app.get(doc)
    assert type(doc_file.content()) is dict
    # removing the created doc
    app.delete(doc)

def test_get_not_existing(app):
    with pytest.raises(FlaskCloudantException) as ex:
        app.get('random-not-existing-id')
    assert ex.value.status_code == 404

def test_put(app, doc):
    with pytest.raises(FlaskCloudantException) as ex:
        app.put({'test': 'test_put'}, doc)
    assert ex.value.status_code == 405

def test_put_override(app, doc):
    doc_file = app.put({'test': 'test'}, doc,  override=True)
    assert doc_file.content()['test'] == 'test'
    # removing the created doc
    app.delete(doc)

def test_delete(app, doc):
    doc = app.put({'test': doc})
    assert doc.exists()
    app.delete(doc.content()['_id'])
    assert not doc.exists()
