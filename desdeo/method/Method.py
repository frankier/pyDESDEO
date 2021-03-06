# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2016  Vesa Ojalehto
'''
Module description
'''
import abc
class InteractiveMethod(object):
    '''
    Abstract base class for interactive multiobjective methods

    '''
    __metaclass__ = abc.ABCMeta

    def __init__(self, problem, method_class):
        self.problem = problem
        self.method_class = method_class

    @abc.abstractmethod
    def _nextIteration(self, *args, **kwargs):
        pass

    def nextIteration(self, *args, **kwargs):
        '''
        Return solution(s) for the next iteration
        '''
        return self._nextIteration(*args, **kwargs)

    @abc.abstractmethod
    def _initIteration(self, *args, **kwargs):
        pass

    def initIteration(self, *args, **kwargs):
        '''
        Return the initial solution(s)
        '''
        return self._initIteration(*args, **kwargs)
