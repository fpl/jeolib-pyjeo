"""Test suite for module pyjeo.demops."""
# Author(s): Pieter.Kempeneers@ec.europa.eu,
#            Ondrej Pesek,
#            Pierre.Soille@ec.europa.eu
# Copyright (C) 2018-2020 European Union (Joint Research Centre)
#
# This file is part of pyjeo.
#
# pyjeo is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyjeo is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyjeo.  If not, see <https://www.gnu.org/licenses/>.

import pyjeo as pj
import unittest


tiles = ['tests/data/red1.tif', 'tests/data/red2.tif']
vector = 'tests/data/nuts_italy.sqlite'


class BadDEMOps(unittest.TestCase):
    """Test functions and methods from DEMOps module."""

    @staticmethod
    def test_slope():
        """Test DEM flow functions and methods."""
        jim = pj.Jim(tiles[0])

        slope = pj.demops.slope(jim)
        stats = slope.stats.getStats(band=0)

        assert slope == jim.demops.slope(), \
            'Error: function demops.slope() not identical to method'
        jim.demops.slope()
        assert stats['max'] <= 90, \
            'Error: max>90 in demops.slope()'
        assert stats['min'] >= 0, \
            'Error: min<0 in demops.slope()'

    #todo: data type of flowDirectionFlat should be UInt16
    @staticmethod
    def test_flows():
        """Test DEM flow functions and methods."""
        jim = pj.Jim(tiles[0])

        destructive_object = pj.Jim(jim)
        flow = pj.demops.flowDirectionD8(destructive_object)
        stats = flow.stats.getStats(band=0)

        assert stats['max'] <= 8, \
            'Error in demops.flowDirectionD8()'
        assert stats['min'] >= 0, \
            'Error in demops.flowDirectionD8()'

        destructive_object.demops.flowDirectionD8()

        assert destructive_object.properties.isEqual(flow), \
            'Error in demops.flowDirectionD8()'

        flow_2 = pj.demops.flow(destructive_object, 8)
        stats = flow_2.stats.getStats(band=0)

        assert stats['min'] >= 1, \
            'Error in demops.flowDirectionD8()'

        destructive_object.demops.flow(8)

        assert destructive_object.properties.isEqual(flow_2), \
            'Error in demops.flowDirectionD8()'

        destructive_object = pj.Jim(jim)

        flow_new = pj.demops.flowNew(destructive_object, flow, 8)
        destructive_object.demops.flowNew(flow, 8)

        assert destructive_object.properties.isEqual(flow_new), \
            'Error in demops.flowNew()'
        assert flow_new.stats.getStats(band=0)['min'] > 0, \
            'Error in demops.flowNew()'
        assert destructive_object.properties.getDataType() == \
               flow_new.properties.getDataType(), \
            'Error in demops.flowNew() (changed data type of object)'

        flow = pj.demops.flowDirectionDInf(jim)
        jim.demops.flowDirectionDInf()
        stats = jim.stats.getStats(band=0)

        assert jim.properties.isEqual(flow), \
            'Error in demops.demFlowDirectionDInf()'
        assert stats['min'] >= -1, \
            'Error in demops.demFlowDirectionDInf()'
        assert stats['max'] < 6.5, \
            'Error in demops.demFlowDirectionDInf()'

        # jim2 = pj.Jim(tiles[0][:-8] + 'nir' + tiles[0][-5:])
        destructive_object = pj.Jim(jim)
        destructive_object[25:30, 25:30] = 65533

        # flow = pj.demops.flowDirectionFlat(destructive_object, jim2, 8)
        # destructive_object.demops.flowDirectionFlat(jim2, 8)
        # stats = destructive_object.stats.getStats(band=0)

        # assert destructive_object.properties.isEqual(flow), \
        #     'Error in demops.flowDirectionFlat()'
        # TODO: Uncomment after realizing why jim is changed during flow = ...
        #       and fixing the test / mialib / jiplib
        # assert stats['min'] >= 0, 'Error in demops.flowDirectionFlat()'
        # assert stats['max'] <= 8, 'Error in demops.flowDirectionFlat()'

        # flow = pj.demops.flowDirectionFlatGeodesic(jim, jim2, 8)
        # jim.demops.flowDirectionFlatGeodesic(jim2, 8)

        # assert jim.properties.isEqual(flow), \
        #     'Error in demops.flowDirectionFlatGeodesic()'
        # # TODO: Uncomment after bug in jiplib fixed

    @staticmethod
    def test_hillShade():
        """Test hillShade functions and methods."""
        dem = pj.Jim(ncol= 50, nrow = 50, otype = 'GDT_Byte')
        dem[24:25,24:25] = 100
        sza = pj.Jim(ncol= 50, nrow = 50, otype = 'GDT_Byte')
        sza.pixops.setData(20)
        saa = pj.Jim(ncol= 50, nrow = 50, otype = 'GDT_Byte')
        saa.pixops.setData(180)
        hs = pj.demops.hillShade(dem, sza, saa)

        assert hs[24,24] == 0, \
            'Error in demops.hillShade(), max elevation should not be shaded'
        assert hs[23,24] == 0, \
            'Error in demops.hillShade(), north of max elevation should be shaded'
        dem.demops.hillShade(sza, saa)
        assert dem.properties.isEqual(hs), \
            'Error in demops.hillShade(), function not equal to method'

    @staticmethod
    def test_drainage_areas():
        """Test drainage area functions and methods."""
        jim = pj.Jim(tiles[0])
        d8 = pj.demops.flowDirectionD8(jim)

        cda = pj.demops.contribDrainArea(d8, 8)
        destructive_object = pj.Jim(d8)
        destructive_object.demops.contribDrainArea(8)

        assert destructive_object.properties.isEqual(cda), \
            'Error in demops.contribDrainArea()'
        assert destructive_object.stats.getStats(band=0)['min'] >= 1, \
            'Error in demops.contribDrainArea()'
        thresh = pj.Jim(jim)
        thresh.pixops.setData(5)

        strat = pj.demops.contribDrainAreaStrat(cda, thresh, d8)
        destructive_object.demops.contribDrainAreaStrat(thresh, d8)
        stats = destructive_object.stats.getStats(band=0)
        assert destructive_object.properties.isEqual(strat), \
            'Error in demops.contribDrainAreaStrat()'
        assert stats['min'] == 0, 'Error in demops.contribDrainAreaStrat()'
        assert stats['max'] == 1, 'Error in demops.contribDrainAreaStrat()'

        inf = pj.demops.flowDirectionDInf(jim)

        # TODO: Suppress output originating in mialib (flag `quiet`, please?)
        cda_inf = pj.demops.contribDrainAreaInf(inf)
        inf.demops.contribDrainAreaInf()

        assert inf.properties.isEqual(cda_inf), \
            'Error in demops.contribDrainAreaInf()'
        assert abs(inf.stats.getStats(band=0)['min']) == 1, \
            'Error in demops.contribDrainAreaInf()'

    @staticmethod
    def test_slopes():
        """Test demSlopeD8() function and method."""
        jim = pj.Jim(tiles[0])
        destructive_object = pj.Jim(jim)

        slope = pj.demops.slopeD8(destructive_object)
        stats = slope.stats.getStats(band=0)

        assert stats['min'] >= 0, \
            'Error in demops.slopeD8()'

        destructive_object.demops.slopeD8()
        assert destructive_object.properties.isEqual(slope), \
            'Error in demops.slopeD8()'

        inf = pj.demops.slopeDInf(jim)
        jim.demops.slopeDInf()
        assert jim.properties.isEqual(inf), 'Error in demops.slopeDInf()'
        assert inf.stats.getStats(band=0)['min'] >= 0, \
            'Error in demops.slopeDInf()'

    @staticmethod
    def test_flood_dir():
        """Test floodDir() func and method."""
        jim = pj.Jim(tiles[0])

        flood_dir = pj.demops.floodDir(jim, 8)
        jim.demops.floodDir(8)
        stats = jim.stats.getStats(band=0)

        assert jim.properties.isEqual(flood_dir), 'Error in demops.floodDir()'
        assert stats['min'] >= 0, 'Error in demops.floodDir()'

        assert stats['max'] <= 8, 'Error in demops.floodDir()'

        # assert stats['max'] <= jim.properties.nrOfRow() * \
        #       jim.properties.nrOfCol(), 'Error in demops.floodDir()'

    @staticmethod
    def test_catchments():
        """Test catchment basin funcs and methods."""
        # jim = pj.Jim(tiles[0])
        # d8 = pj.demops.flowDirectionD8(jim)
        # jim.ccops.labelPixels()

        # outlet = pj.demops.catchmentBasinOutlet(jim, d8)
        # jim.demops.catchmentBasinOutlet(d8)

        # assert jim.properties.isEqual(outlet), \
        #     'Error in demops.catchmentBasinOutlet()'
        # # TODO: Uncomment after bug in jiplib fixed

        # TODO: catchmentBasinConfluence

    @staticmethod
    def test_strahler():
        """Test function and method for Strahler order."""
        jim = pj.Jim(tiles[0])
        jim.demops.flowDirectionD8()

        strahler = pj.demops.strahler(jim)
        jim.demops.strahler()
        stats = jim.stats.getStats(band=0)

        assert jim.properties.isEqual(strahler), 'Error in demops.strahler()'
        assert stats['min'] >= 0, 'Error in demops.strahler()'
        assert stats['max'] <= 8, 'Error in demops.strahler()'

    @staticmethod
    def test_pit_removals():
        """Test functions and methods for pit removals."""
        jim = pj.Jim(tiles[0])
        label = pj.ccops.labelPixels(jim)

        unpit = pj.demops.pitRemovalCarve(label, jim, 8, 212)
        pit_label = pj.Jim(label)
        pit_label.demops.pitRemovalCarve(jim, 8, 212)

        assert unpit.properties.isEqual(pit_label), \
            'Error in demops.pitRemovalCarve()'

        # TODO: Suppress output originating in mialib (flag `quiet`, please?)
        unpit = pj.demops.pitRemovalOptimal(label, jim, 8, 212, 0)
        label.demops.pitRemovalOptimal(jim, 8, 212, 0)

        assert unpit.properties.isEqual(label), \
            'Error in demops.pitRemovalOptimal()'


def load_tests(loader=None, tests=None, pattern=None):
    """Load tests."""
    if not loader:
        loader = unittest.TestLoader()
    suite_list = [loader.loadTestsFromTestCase(BadDEMOps)]
    return unittest.TestSuite(suite_list)
