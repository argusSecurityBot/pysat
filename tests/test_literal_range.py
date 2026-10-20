import pytest
from pysat.solvers import Solver
from pysat.solvers import ergo_present

solvers = ['m22', 'mgh', 'mep', 'mpl', 'mcm', 'mc', 'mcb', 'lgl',
           'g3', 'g4', 'g41', 'gc3', 'gc4',
           'cd', 'cd15', 'cd19', 'cd30', 'ks', 'ergo']

if not ergo_present:  # not built on every platform
    solvers.remove('ergo')

bad_literals = [2**31, -2**31, 2**32 + 1, 2**63]


def test_literal_out_of_range_first():
    for name in solvers:
        for lit in bad_literals:
            with Solver(name=name) as solver:
                with pytest.raises((ValueError, OverflowError)):
                    solver.add_clause([lit])


def test_literal_out_of_range_after():
    for name in solvers:
        for lit in bad_literals:
            with Solver(name=name) as solver:
                solver.add_clause([1, 2])
                with pytest.raises((ValueError, OverflowError)):
                    solver.add_clause([lit])
                assert solver.solve() == True, 'solver {0} broken'.format(name)


def test_literal_out_of_range_bootstrap():
    for name in solvers:
        for lit in bad_literals:
            with pytest.raises((ValueError, OverflowError)):
                Solver(name=name, bootstrap_with=[[1, 2], [lit]])
