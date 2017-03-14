#!/usr/bin/env python
'''
Unit tests.
'''

import flask
from flask_cloudant import FlaskCloudant
from flask_cloudant.error import FlaskCloudantException
import pytest

@pytest.fixture
def app():
    _app_ = flask.Flask(__name__)
    _app_.config.from_object('credentials')
    storage = FlaskCloudant(_app_)
    return storage

def test_get_existing(app):
    doc = app.get('f8d43659205e0ba4f37ed26f71074333')
    assert type(doc.content()) is dict

def test_get_not_existing(app):
    with pytest.raises(FlaskCloudantException) as ex:
        app.get('random-not-existing-id')
    assert ex.value.status_code == 404

def test_put(app):
    with pytest.raises(FlaskCloudantException) as ex:
        app.put({'test': 'test_put'},
                '3a6999acddc088784398b8ce62be7972')
    assert ex.value.status_code == 405

def test_put_override(app):
    doc = app.put({'test': 'test_put_fails'},
                  '3a6999acddc088784398b8ce62be7972',
                  override=True)
    assert doc.content()['test'] == 'test_put_fails'
    # moving back to its original state
    app.put({'test': 0},
            '3a6999acddc088784398b8ce62be7972',
            override=True)


def test_delete(app):
    doc = app.put({'test': 'test-to-delete'})
    assert doc.exists()
    app.delete(doc.content()['_id'])
    assert not doc.exists()
