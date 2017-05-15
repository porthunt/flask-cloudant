#!/usr/bin/env python
'''
Unit tests.
'''

from flask_cloudant import FlaskCloudant
from flask_cloudant import FlaskCloudantDocument
from flask_cloudant.error import FlaskCloudantException
import flask
import pytest
import uuid


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

def test_content(app, doc):
    doc_file = app.get(doc)
    assert doc_file.content()['_id'] == doc
    app.delete(doc)

def test_exists(app):
    pass


def save(app):
    pass


def delete(app):
    pass
