#!/usr/bin/env python
'''
Integration tests.
'''

import flask
from flask_cloudant import FlaskCloudant
import pytest


@pytest.fixture
def app():
    _app_ = flask.Flask(__name__)
    _app_.config.from_object('credentials')
    return _app_


def test_constructor(app):
    storage = FlaskCloudant(app)
    assert storage._client is not None
