# from babyshki import *
from babyshki import *
import unittest
import pytest

def test_find_contact():
    phone = '+79253792174'
    contacts = find_contact(phone)
    assert contacts is not None




class TestPrepareFunctions:
    def test_prepare_parking_size(self):
        fields = {'ParkingSize10': True}
        assert prepare_parking_size(fields) == 203

        fields = {'ParkingTracks': True}
        assert prepare_parking_size(fields) == 205

        fields = {'ParkingNot': True}
        assert prepare_parking_size(fields) == 207

        fields = {}
        assert prepare_parking_size(fields) is None

    def test_prepare_parking_distance(self):
        fields = {'ParkingDistance': True}
        assert prepare_parking_distance(fields) == 209

        fields = {'ParkingDistanceId': True}
        assert prepare_parking_distance(fields) == 211

        fields = {'ParkingDistanceMore': True}
        assert prepare_parking_distance(fields) == 213

        fields = {}
        assert prepare_parking_distance(fields) == 213

    def test_prepare_lift(self):
        fields = {'Lift': True}
        assert prepare_lift(fields) == 415

        fields = {'LiftLight': True}
        assert prepare_lift(fields) == 417

        fields = {'LiftNot': True}
        assert prepare_lift(fields) == 419

        fields = {}
        assert prepare_lift(fields) is None

    def test_prepare_power_electric(self):
        fields = {'PowerElectric': 20}
        assert prepare_power_electric(fields) == 221

        fields = {'PowerElectric': 30}
        assert prepare_power_electric(fields) == 223

        fields = {'PowerElectric': 80}
        assert prepare_power_electric(fields) == 225

        fields = {'PowerElectric': 150}
        assert prepare_power_electric(fields) == 227

    def test_prepare_neighbors(self):
        fields = {'NeighborsId': '1'}
        assert prepare_neighbors(fields) == 251

        fields = {'NeighborsId': '2'}
        assert prepare_neighbors(fields) == 255

        fields = {'NeighborsId': '3'}
        assert prepare_neighbors(fields) == 349

        fields = {}
        assert prepare_neighbors(fields) is None

    def test_prepare_region(self):
        fields = {'Region': 'Москва и МО'}
        assert prepare_region(fields) == 409

        fields = {'Region': 'Санкт-Петербург'}
        assert prepare_region(fields) == 411

        fields = {'Region': 'Другой'}
        assert prepare_region(fields) == 413

        fields = {}
        assert prepare_region(fields) == 413