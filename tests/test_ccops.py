"""Test suite for module pyjeo.ccops."""
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

import numpy as np


tiles = ['tests/data/red1.tif', 'tests/data/red2.tif']
rasterfn = 'tests/data/modis_ndvi_2010.tif'


class BadCCOps(unittest.TestCase):
    """Test functions and methods from ccops modules."""

    @staticmethod
    def test_colorsys():
        """Test color system conversions."""
        jim = pj.Jim(rasterfn, band = [0, 1, 2])
        jim.pixops.convert('GDT_Byte')
        hsv = pj.ccops.convertRgbToHsx(jim, 'V')
        jim.ccops.convertRgbToHsx('V')
        assert jim.properties.isEqual(hsv), \
            'Inconsistency in ccops.convertRgbToHsx(V)' \
            '(method returns different result than function)'

        jim = pj.Jim(rasterfn, band = [0, 1, 2])
        jim.pixops.convert('GDT_Byte')
        hsv = pj.ccops.convertRgbToHsx(jim, 'L')
        jim.ccops.convertRgbToHsx('L')
        assert jim.properties.isEqual(hsv), \
            'Inconsistency in ccops.convertRgbToHsx(L)' \
            '(method returns different result than function)'

        jim = pj.Jim(rasterfn, band = [0, 1, 2])
        jim.pixops.convert('GDT_Byte')
        hsv = pj.ccops.convertRgbToHsx(jim, 'I')
        jim.ccops.convertRgbToHsx('I')
        assert jim.properties.isEqual(hsv), \
            'Inconsistency in ccops.convertRgbToHsx(I)' \
            '(method returns different result than function)'

        # jim = pj.Jim(rasterfn, band = [0, 1, 2])
        # jim.pixops.convert('GDT_Byte')
        # rgb = pj.ccops.convertHsiToRgb(jim)
        # jim.ccops.convertHsiToRgb()
        # assert jim.properties.isEqual(rgb), \
        #     'Inconsistency in ccops.convertHsiToRgb()' \
        #     '(method returns different result than function)'

        # jim = pj.Jim(rasterfn, band = [0, 1, 2])
        # jim.pixops.convert('GDT_Byte')
        # rgb = pj.ccops.convertHlsToRgb(jim)
        # jim.ccops.convertHlsToRgb()
        # assert jim.properties.isEqual(rgb), \
        #     'Inconsistency in ccops.convertHlsToRgb()' \
        #     '(method returns different result than function)'


    @staticmethod
    def test_distances():
        """Test the distance functions and methods."""
        jim = pj.Jim(tiles[0])

        jim.pixops.convert('Byte')
        distances = pj.ccops.distance2dEuclideanSquared(jim)
        jim.ccops.distance2dEuclideanSquared()

        assert jim.properties.isEqual(distances), \
            'Error in ccops.distance2dEuclideanSquared()'

        stats = jim.stats.getStats(band=0)

        assert stats['min'] == 0, 'Error in ccops.distance2dEuclideanSquared()'
        assert stats['max'] <= \
               jim.properties.nrOfCol()*jim.properties.nrOfRow(), \
            'Error in ccops.distance2dEuclideanSquared()'

        # Test distance2dEuclideanSquared for multi-plane images
        jim = pj.Jim(tiles[1])
        jim.geometry.stackPlane(pj.Jim(tiles[0]))

        jim.pixops.convert('Byte')
        distances2 = pj.ccops.distance2dEuclideanSquared(jim)

        assert(pj.geometry.cropPlane(distances2, 1).
               properties.isEqual(distances)), \
               'Error in multi-plane ccops.distance2dEuclideanSquared()'

        assert(not pj.geometry.cropPlane(distances2, 0).
               properties.isEqual(distances)), \
               'Error in multi-plane ccops.distance2dEuclideanSquared()'

        jim.ccops.distance2dEuclideanSquared()
        assert jim.properties.isEqual(distances2), \
            'Error in multi-plane ccops.distance2dEuclideanSquared()'

        stats = jim.stats.getStats(band=0)

        assert stats['min'] == 0, 'Error in ccops.distance2dEuclideanSquared()'
        assert stats['max'] <= \
               jim.properties.nrOfCol()*jim.properties.nrOfRow(), \
            'Error in ccops.distance2dEuclideanSquared()'

        # Test distance2dEuclideanSquared for multi-plane multi-band images
        jim = pj.Jim(tiles[0])
        jim.geometry.stackBand(pj.Jim(tiles[1]))
        jim1 = pj.Jim(tiles[1])
        jim1.geometry.stackBand(pj.Jim(tiles[0]))
        jim.geometry.stackPlane(jim1)

        jim.pixops.convert('Byte')
        distances1 = pj.ccops.distance2dEuclideanSquared(jim, band = 0)
        distances2 = pj.ccops.distance2dEuclideanSquared(jim, band = 1)

        assert(distances1.properties.nrOfBand() == 1), \
               'Error in number of bands ccops.distance2dEuclideanSquared()'

        assert(distances2.properties.nrOfBand() == 1), \
               'Error in number of bands ccops.distance2dEuclideanSquared()'

        assert(pj.geometry.cropPlane(distances1, 0).
               properties.isEqual(pj.geometry.cropPlane(distances2, 1))), \
               'Error in multi-plane ccops.distance2dEuclideanSquared()'

        assert(pj.geometry.cropPlane(distances1, 1).
               properties.isEqual(pj.geometry.cropPlane(distances2, 0))), \
               'Error in multi-plane ccops.distance2dEuclideanSquared()'

        assert(pj.geometry.cropPlane(distances1, 0).
               properties.isEqual(distances)), \
               'Error in multi-plane ccops.distance2dEuclideanSquared()'

        # Test distance2d4

        jim = pj.Jim(tiles[0])

        distances = pj.ccops.distance2d4(jim)
        jim.ccops.distance2d4()
        stats = jim.stats.getStats(['max', 'min'])

        assert jim.properties.isEqual(distances), \
            'Inconsistency in ccops.distance2d4() ' \
            '(method returns different result than function)'

        assert stats['max'] == jim.properties.nrOfRow() / 2 - 1, \
            'Error in Jim.ccops.distance2d4() (wrong maximum value)'
        assert stats['min'] == 0, \
            'Error in Jim.ccops.distance2d4() (wrong minimum value)'

        # Test distance2dChamfer

        jim = pj.Jim(tiles[0])[0:10, 0:10]

        chamfer_type = 11
        distances = pj.ccops.distance2dChamfer(jim, chamfer_type)
        jim.ccops.distance2dChamfer(chamfer_type)
        stats = jim.stats.getStats(['max', 'min'])

        assert jim.properties.isEqual(distances), \
            'Inconsistency in ccops.distance2dChamfer() ' \
            '(method returns different result than function)'

        assert 0 < stats['min'] < 10, \
            'Error in Jim.ccops.distance2dChamfer() (suspicious minimum value)'
        assert stats['max'] <= chamfer_type, \
            'Error in Jim.ccops.distance2dChamfer() (wrong maximum value)'

        chamfer_type = 5711
        jim.ccops.distance2dChamfer(chamfer_type)

        assert not jim.properties.isEqual(distances), \
            'Suspicious values for distance2dChamfer() ' \
            '(same results for different types of distance)'

        # Test distance2dEuclideanConstrained

        jim1 = pj.Jim(tiles[0])
        jim1.pixops.convert('Byte')
        jim2 = pj.Jim(jim1)

        jim1.pixops.simpleThreshold(127, 250, 0, 1)
        jim2.pixops.simpleThreshold(127, 200, 0, 1)

        jim_byte = pj.Jim(jim2)

        distances = pj.ccops.distance2dEuclideanConstrained(jim2, jim1)
        jim_byte.ccops.distance2dEuclideanConstrained(jim1)
        stats = jim_byte.stats.getStats(band=0)
        max = stats['max']

        assert jim_byte.properties.isEqual(distances), \
            'Inconsistency in ccops.distance2dEuclideanConstrained() ' \
            '(method returns different result than function)'

        assert not jim2.properties.isEqual(distances), \
            'Error in ccops.distance2dEuclideanConstrained() ' \
            '(did not have any effect)'

        assert 0 < max < jim_byte.properties.nrOfCol() * \
               jim_byte.properties.nrOfRow(), \
            'Error in Jim.ccops.distance2dEuclideanConstrained() ' \
            '(maximum value not smaller than nrOfCol * nrOfRow or equal to 0)'
        assert stats['min'] == 0, \
            'Error in Jim.ccops.distance2dEuclideanConstrained() ' \
            '(minimum value not 0 for Byte)'

        # Test distanceInfluenceZones2dEuclidean
        nrow = ncol = 500
        jim = pj.Jim(nrow=nrow, ncol=ncol, otype='Byte')
        for i in range(15):
            jim[np.random.randint(0, 500), np.random.randint(0, 500)] = i

        jim_byte = pj.Jim(jim)

        distances = pj.ccops.distanceInfluenceZones2dEuclidean(jim_byte)
        jim_byte.ccops.distanceInfluenceZones2dEuclidean()

        stats = jim_byte.stats.getStats(['max', 'min'])

        assert jim_byte.properties.isEqual(distances), \
            'Inconsistency in ccops.distanceInfluenceZones2dEuclidean() ' \
            '(method returns different result than function)'

        assert not jim.properties.isEqual(distances), \
            'Error in ccops.distanceInfluenceZones2dEuclidean() ' \
            '(did not have any effect)'

        assert stats['max'] == 14, \
             'Error in Jim.ccops.distanceInfluenceZones2dEuclidean() ' \
             '(maximum value not 255 for Byte)'
        assert stats['min'] >= 1, \
            'Error in Jim.ccops.distanceInfluenceZones2dEuclidean() ' \
            '(minimum value not 1 for Byte)'

        # Test distanceGeodesic

        jim1 = pj.Jim(tiles[0])
        jim1.pixops.convert('Byte')
        jim2 = pj.Jim(jim1)
        # jim2.pixops.convert('Byte')

        jim1.pixops.simpleThreshold(127, 250, 0, 1)
        jim2.pixops.simpleThreshold(127, 200, 0, 1)

        jim_byte1 = pj.Jim(jim1)
        jim_byte2 = pj.Jim(jim1)

        distances = pj.ccops.distanceGeodesic(jim_byte1, jim2, 4)
        jim_byte1.ccops.distanceGeodesic(jim2, 4)
        stats = jim_byte1.stats.getStats(band=0)
        mean = stats['mean']

        assert jim_byte1.properties.isEqual(distances), \
            'Inconsistency in ccops.distanceGeodesic() ' \
            '(method returns different result than function)'

        assert not jim1.properties.isEqual(distances), \
            'Error in ccops.distanceGeodesic() ' \
            '(did not have any effect)'

        assert stats['max'] == 255, \
            'Error in Jim.ccops.distanceGeodesic() ' \
            '(maximum value not 255 for Byte)'
        assert stats['min'] == 0, \
            'Error in Jim.ccops.distanceGeodesic() ' \
            '(minimum value not 0 for Byte)'

        distances = pj.ccops.distanceGeodesic(jim_byte2, jim2, 8)
        jim_byte2.ccops.distanceGeodesic(jim2, 8)
        stats = jim_byte2.stats.getStats(band=0)

        assert jim_byte2.properties.isEqual(distances), \
            'Inconsistency in ccops.distanceGeodesic() ' \
            '(method returns different result than function)'

        assert not jim_byte2.properties.isEqual(jim_byte1), \
            'Error in ccops.distanceGeodesic() ' \
            '(the same result for graph=8 and graph=4)'

        assert stats['max'] == 255, \
            'Error in Jim.ccops.distanceGeodesic() ' \
            '(maximum value not 255 for Byte)'
        assert stats['min'] == 0, \
            'Error in Jim.ccops.distanceGeodesic() ' \
            '(minimum value not 0 for Byte)'
        assert stats['mean'] < mean, \
            'Error in Jim.ccops.distanceGeodesic() ' \
            '(mean value for graph=8 not smaller than for graph=4)'

    @staticmethod
    def test_labelling():
        """Test the labelling functions and methods."""
        jim1 = pj.Jim(tiles[0])
        jim2 = pj.Jim(tiles[1])

        jim1.pixops.convert('Byte')
        jim2.pixops.convert('Byte')

        labelled = pj.ccops.dissimToAlphaCCs(jim1, jim2, 0)
        labelled_different = pj.ccops.dissimToAlphaCCs(jim1, jim2, 5)
        # jim1_copy = pj.Jim(jim1)
        #member function not supported
        # jim1_copy.ccops.dissimToAlphaCCs(jim2, 0)

        stats = labelled.stats.getStats()

        # assert jim1_copy.properties.isEqual(labelled), \
        #     'Inconsistency in ccops.dissimToAlphaCCs() ' \
        #     '(method returns different result than function)'

        assert not labelled.properties.isEqual(labelled_different), \
            'Error in ccops.dissimToAlphaCCs() ' \
            'created the same object for different alpha value)'

        assert stats['min'] == 0, \
            'Error in Jim.ccops.dissimToAlphaCCs() ' \
            '(minimum value not equal to 0)'
        assert 0 < stats['max'] < jim1.properties.nrOfCol() * \
               jim1.properties.nrOfRow(), \
            'Error in Jim.ccops.dissimToAlphaCCs() ' \
            '(maximum value not smaller than nrOfCol * nrOfRow or equal to 0)'

        # Test labelConstrainedCCsVariance()

        labelled = pj.ccops.labelConstrainedCCsVariance(
            jim1, 0, 0, 0, 0, 0, 0.0, pj.Jim(graph=4))
        labelled_different = pj.ccops.labelConstrainedCCsVariance(
            jim1, 0, 0, 0, 0, 0, 0.0, pj.Jim(graph=8))
        jim1_copy = pj.Jim(jim1)
        jim1_copy.ccops.labelConstrainedCCsVariance(0, 0, 0, 0, 0, 0,
                                                    pj.Jim(graph=4))

        stats = labelled.stats.getStats(band=0)

        assert jim1_copy.properties.isEqual(labelled), \
            'Inconsistency in ccops.labelConstrainedCCsVariance() ' \
            '(method returns different result than function)'

        assert not labelled.properties.isEqual(labelled_different), \
            'Error in ccops.labelConstrainedCCsVariance() ' \
            '(created the same object for different alpha value)'

        assert stats['min'] == 0, \
            'Error in Jim.ccops.labelConstrainedCCsVariance() ' \
            '(minimum value not equal to 0)'
        assert 0 < stats['max'] < jim1.properties.nrOfCol() * \
               jim1.properties.nrOfRow(), \
            'Error in Jim.ccops.labelConstrainedCCsVariance() ' \
            '(maximum value not smaller than nrOfCol * nrOfRow or ' \
            'equal to 0)'

        labelled_different = pj.ccops.labelConstrainedCCsVariance(
            jim1, 0, 0, 0, 1, 1, 5, pj.Jim(graph=4))
        stats2 = labelled_different.stats.getStats(band=0)

        assert stats2['max'] < stats['max'], \
            'Error in Jim.ccops.labelConstrainedCCsVariance() ' \
            '(maximum value for rg2, rl2 and varmax2 > rg1, rl1 and varmax1 ' \
            'not smaller)'

        labelled_different = pj.ccops.labelConstrainedCCsVariance(
            jim1, 5, 5, 0, 0, 0, 0, pj.Jim(graph=4))

        assert labelled_different[1, 1].np()[0, 0] == 0, \
            'Error in Jim.ccops.labelConstrainedCCsVariance() ' \
            '(some of parameters ox, oy, oz not applied)'

        non_zero1 = np.count_nonzero(jim1_copy.np())
        non_zero2 = np.count_nonzero(labelled_different.np())
        assert non_zero1 > non_zero2, \
            'Error in Jim.ccops.labelConstrainedCCsVariance() ' \
            '(some of parameters ox, oy, oz not applied)'

        # Test labelFlatZonesSeeded()
        nr_of_col = nr_of_row = 20
        jim = pj.Jim(jim1[0:nr_of_col, 0:nr_of_row])

        ngb = pj.Jim(ncol=3, nrow=3, otype='Byte')
        ngb[0, 1] = 1
        ngb[1, 0] = 1
        ngb[1, 2] = 1
        ngb[2, 1] = 1

        seeds = pj.Jim(ncol=nr_of_col,
                       nrow=nr_of_row,
                       uniform=[0, 2],
                       otype='Byte')

        labelled = pj.ccops.labelFlatZonesSeeded(jim, ngb, seeds,
                                                 1, 1, 0)
        jim.ccops.labelFlatZonesSeeded(ngb, seeds, 1, 1, 0)

        labelled_different = pj.ccops.labelFlatZonesSeeded(
            jim, ngb, seeds, 0, 0, 0)

        stats = jim.stats.getStats(['min', 'max'])

        assert jim.properties.isEqual(labelled), \
            'Inconsistency in ccops.labelFlatZonesSeeded() ' \
            '(method returns different result than function)'
        assert not labelled.properties.isEqual(labelled_different), \
            'Error in ccops.labelFlatZonesSeeded() ' \
            '(created the same object for different ox and oy)'
        assert stats['min'] == 0, \
            'Error in Jim.ccops.labelFlatZonesSeeded() ' \
            '(minimum value not equal to 0)'
        assert labelled.np()[0, 0] == 0, \
            'Error in Jim.ccops.labelFlatZonesSeeded() ' \
            '(value at position [0, 0] with 3x3 jim_ngb not equal to 0)'
        assert 0 < stats['max'] < nr_of_col * nr_of_row, \
            'Error in Jim.ccops.labelFlatZonesSeeded() ' \
            '(maximum value not smaller than nrOfCol * nrOfRow or ' \
            'equal to 0)'


def load_tests(loader=None, tests=None, pattern=None):
    """Load tests."""
    if not loader:
        loader = unittest.TestLoader()
    suite_list = [loader.loadTestsFromTestCase(BadCCOps)]
    return unittest.TestSuite(suite_list)
