import os

import numpy as np

from desdeo.method.NIMBUS import NIMBUS
from desdeo.preference.PreferenceInformation import NIMBUSClassification
from desdeo.problem.Problem import PreGeneratedProblem
from desdeo.optimization.OptimizationMethod import PointSearch, SciPyDE

from examples.AuxiliaryServices import example_path
from examples.NarulaWeistroffer import RiverPollution

def run(method, preference):
    ''' test method for steps iterations with given  reference point and bounds (if any)'''
    return method.nextIteration(preference = preference)

def test_running_NIMBUS():
    vals = []
    method = NIMBUS(PreGeneratedProblem(filename = os.path.join(example_path, "AuxiliaryServices.csv")), PointSearch)

    run1 = run(method, NIMBUSClassification(method.problem, [("<", None), (">=", 1), ("<", None)]))
    assert run1[0][1] < 1
    assert len(run1) == 2

    # When using point search, there should not be better solutions when projected
    cls = []
    for v in run1[0]:
        cls.append(("<=", v))
    run2 = run(method, NIMBUSClassification(method.problem, cls))

    assert np.isclose(run1[0], run2[1]).all()  # pylint: disable=E1101

def test_narula():
    method = NIMBUS(RiverPollution(), SciPyDE)

    vals = method.initIteration()
    assert len(vals) == 1
    vals = method.nextIteration(preference = NIMBUSClassification(method.problem, [("<", None), ("<=", .1), ("<", None), ("<=", 0.4)]))
    assert len(vals) == 2
    vals = method.nextIteration(preference = NIMBUSClassification(method.problem, [("<", None), ("<=", .1), ("<", None), ("<=", 0.4)]), scalars = ["NIM"])
    assert len(vals) == 1


def test_classification(method):
    vals = method.initIteration()
    method.problem.selected = vals[0]
    cls = NIMBUSClassification(method.problem, vals[0])
    assert cls.reference_point() == vals[0]
