# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function, division, absolute_import
import json
from http.client import OK

import dpath
from nose.tools import assert_equal, assert_in

from . import subject


def assert_items_equal(x, y):
    assert_equal(sorted(x), sorted(y))


openAPI_response = subject.get('/spec')


def test_return_code():
    assert_equal(openAPI_response.status_code, OK)


body = json.loads(openAPI_response.data.decode('utf-8'))


def test_paths():
    assert_items_equal(
        body['paths'],
        ["/parameter/{parameterID}",
        "/parameters",
        "/variable/{variableID}",
        "/variables",
        "/trace",
        "/calculate",
        "/spec"]
        )


def test_entity_definition():
    assert_in('parents', dpath.get(body, 'definitions/Household/properties'))
    assert_in('children', dpath.get(body, 'definitions/Household/properties'))
    assert_in('salary', dpath.get(body, 'definitions/Person/properties'))
    assert_in('rent', dpath.get(body, 'definitions/Household/properties'))
    assert_equal('Float', dpath.get(body, 'definitions/Person/properties/salary/additionalProperties/type'))


def test_situation_definition():
    situation_input = body['definitions']['SituationInput']
    situation_output = body['definitions']['SituationOutput']
    for situation in situation_input, situation_output:
        assert_in('households', dpath.get(situation, '/properties'))
        assert_in('persons', dpath.get(situation, '/properties'))
        assert_equal("#/definitions/Household", dpath.get(situation, '/properties/households/additionalProperties/$ref'))
        assert_equal("#/definitions/Person", dpath.get(situation, '/properties/persons/additionalProperties/$ref'))