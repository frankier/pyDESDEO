# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Copyright (c) 2016  Vesa Ojalehto

from abc import ABCMeta, abstractmethod
import numpy as np
import copy
from _ast import Num

class PreferenceInformation(object):
    __metaclass__ = ABCMeta

    def __init__(self, method):
        self._method = method

    def _weights(self):
        return np.array([1.] * self._method.problem.nof_objectives())
        pass

    def weights(self):
        ''' Return weight vector corresponding to the given preference information
        '''
        return self._weights()

class Direction(PreferenceInformation):
    __metaclass__ = ABCMeta

    def default_input(self):
        return [0.0] * len(self._method.problem.nadir)

    def check_input(self, data):
        return ""

class PercentageSpecifictation(Direction):

    def __init__(self, problem, percentages):
        super(PercentageSpecifictation, self).__init__(problem)
        self.pref_input = percentages

    def _weights(self):
        return np.array(self.pref_input) / 100.

    def default_input(self):
        return [0] * len(self._method.problem.nadir)

    def check_input(self, input):
        inp = map(float, input)
        if np.sum(inp) != 100:
            return "Total of the preferences should be 100"
        return ""



class RelativeRanking(Direction):


    def __init__(self, problem, ranking):
        super(RelativeRanking, self).__init__(problem)
        self.pref_input = ranking

    def _weights(self):
        return 1. / np.array(self.pref_input)


class PairwiseRanking(Direction):

    def __init__(self, problem, selected_obj, other_ranking):
        super(PairwiseRanking, self).__init__(problem)
        self.pref_input = (selected_obj, other_ranking)

    def _weights(self):
        ranks = self.pref_input[1]
        fi = self.pref_input[0]
        ranks[:fi] + [1.0] + ranks[fi:]
        return ranks

class ReferencePoint(PreferenceInformation):

    def __init__(self, problem, reference_point = None):
        super(ReferencePoint, self).__init__(problem)
        self._reference_point = reference_point


    def reference_point(self):
        ''' Return reference point corresponding to the given preference information
        '''
        return self._reference_point

class DirectSpecification(Direction, ReferencePoint):
    def __init__(self, problem, direction, reference_point = None):
        super(DirectSpecification, self).__init__(problem, **{"reference_point":reference_point})
        self.pref_input = direction

    def _weights(self):
        return np.array(self.pref_input)

class NIMBUSClassification(ReferencePoint):
    '''
    Preferences by NIMBUS classification

    Attributes
    ----------
    _classification: Dict (objn_n, (class,value))
        NIMBUSClassification information pairing  objective n to  a classification
        with value if needed

    _maxmap: NIMBUSClassification (default:None)
        Minimization - maximiation mapping of classification symbols

    '''
    _maxmap = {">":"<", ">=":"<=", "<":">", "<=":">=", "=":"="}


    def __init__(self, problem, functions, **kwargs):
        ''' Initialize the classification information

        Parameters
        ----------
        functions: list ((class,value)
            Function classification information
        '''
        super(NIMBUSClassification, self).__init__(problem, **kwargs)
        self.__classification = {}
        for f_id, v in enumerate(functions):
            # This is classification
            try:
                iter(v)
                self.__classification[f_id] = v
            # This is reference point
            except TypeError:
                if np.isclose(v, self._problem.ideal[f_id]):
                    self.__classification[f_id] = ("<", self._problem.selected[f_id])
                elif np.isclose(v, self._problem.nadir[f_id]):
                    self.__classification[f_id] = ("<>", self._problem.selected[f_id])
                elif np.isclose(v, self._problem.selected[f_id]):
                    self.__classification[f_id] = ("=", self._problem.selected[f_id])
                elif v < self._problem.as_minimized(self._problem.selected)[f_id]:
                    self.__classification[f_id] = ("<=", v)
                else:
                    self.__classification[f_id] = (">=", v)
            else:
                self.__classification[f_id] = v

        self._reference_point = self.__as_reference_point()
        self._prefrence = self.__classification
    def __getitem__(self, key):
        '''Shortcut to query a classification.'''
        return self.__classification[key]

    def __setitem__(self, key, value):
        '''Shortcut to manipulate a single classification.'''
        self.__classification[key] = value

    def with_class(self, cls):
        ''' Return functions with the class
        '''
        rcls = []
        for key, value in self.__classification.iteritems():
            if value[0] == cls:
                rcls.append(key)
        return rcls

    def __as_reference_point(self):
        ''' Return classification information as reference point
        '''
        ref_val = []
        for fn, f in  self.__classification.iteritems():
            if f[0] == '<':
                ref_val.append(self._problem.ideal[fn])
            elif f[0] == '<>':
                ref_val.append(self._problem.nadir[fn])
            else:
                ref_val.append(f[1])

        return ref_val


class PreferredPoint(object):
        __metaclass__ = ABCMeta


