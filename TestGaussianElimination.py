import unittest
from GaussianElimination import GaussianElimination

# ------------------------
# Unit Test Cases for GaussianElimination
# ------------------------

class TestGaussianElimination(unittest.TestCase):

    def test_incompatible_dimensions(self):
        # Test when B vector has the wrong size (doesn't match number of rows in A)
        A = [[1, 2], [3, 4]]
        B = [5]  # Incorrect size: should be length 2
        ge = GaussianElimination(A, B)
        self.assertTrue(ge.error)       # Expect error flag due to incompatible sizes
        self.assertFalse(ge.was_run)    # Solver should not have run

    def test_unique_solution(self):
        # Test a system with a unique solution
        A = [[2, 3], [1, -1]]
        B = [8, 0]
        ge = GaussianElimination(A, B)
        ge.Solve()
        self.assertFalse(ge.error)               # Should initialize successfully
        self.assertTrue(ge.was_run)              # Solver was executed
        self.assertTrue(all(ge.has_solution))    # All variables are uniquely solved
        self.assertTrue(ge.solved)               # System was successfully solved
        self.assertAlmostEqual(ge.X[0], 1.6, places=5)  # Validate value of x1
        self.assertAlmostEqual(ge.X[1], 1.6, places=5)  # Validate value of x2

    def test_no_solution(self):
        # Test an inconsistent system (parallel lines, no intersection)
        A = [[1, 1], [2, 2]]
        B = [3, 5]  # No solution: inconsistent right-hand sides
        ge = GaussianElimination(A, B)
        ge.Solve()
        self.assertTrue(ge.was_run)                  # Solver ran
        self.assertFalse(any(ge.has_solution))       # No variable can be solved
        self.assertFalse(any(x is not None for x in ge.X))  # All solutions should be None

    def test_underdetermined_some_solution(self):
        # Test a system with more variables than equations
        A = [[1, 2, 3], [0, 1, 4]]
        B = [5, 6]  # Underdetermined: infinitely many solutions
        ge = GaussianElimination(A, B)
        ge.Solve()
        self.assertTrue(ge.was_run)          # Solver ran
        self.assertTrue(ge.solved)           # Marked as solved (partially)
        self.assertIn(None, ge.X)            # At least one variable should be undetermined
        self.assertIn(True, ge.has_solution) # At least one variable has a value

    def test_redundant_equations_all_solved(self):
        # Test a system where all equations are multiples of each other
        A = [[1, 2], [2, 4], [3, 6]]
        B = [5, 10, 15]  # Redundant but consistent
        ge = GaussianElimination(A, B)
        ge.Solve()
        self.assertTrue(ge.was_run)                       # Solver executed
        self.assertTrue(all(h is True for h in ge.has_solution[:1]))  # At least one variable solved
        self.assertTrue(ge.solved)                        # System was consistent

    def test_redundant_equations_some_solved(self):
        # System with some redundancy and partial solvability
        A = [[1, 2, 3], [2, 4, 6], [1, 1, 1]]
        B = [6, 12, 3]  # First two rows are linearly dependent
        ge = GaussianElimination(A, B)
        ge.Solve()
        self.assertTrue(ge.was_run)         # Solver ran
        self.assertIn(None, ge.X)           # At least one variable undetermined
        self.assertIn(True, ge.has_solution)  # At least one variable has a value

    def test_more_rows_than_columns(self):
        # More equations than unknowns, but linearly dependent (should reduce)
        A = [
            [1, 2],
            [2, 4],
            [3, 6],
            [4, 8]
        ]
        B = [3, 6, 9, 12]  # All equations describe the same line
        ge = GaussianElimination(A, B)
        ge.Solve()
        self.assertTrue(ge.was_run)         # Solver executed
        self.assertTrue(ge.solved)          # System is consistent
        self.assertIn(True, ge.has_solution)  # At least one variable is known
        self.assertIn(None, ge.X)           # At least one variable undetermined due to redundancy

    def test_matrix_with_more_than_8_rows(self):
        # Large system with known unique solution: x = [1, 2, 3]
        A = [
            [1, 0, 0],    # x = 1
            [0, 1, 0],    # y = 2
            [0, 0, 1],    # z = 3
            [1, 1, 0],    # x + y = 3
            [0, 1, 1],    # y + z = 5
            [1, 0, 1],    # x + z = 4
            [2, 1, 0],    # 2x + y = 4
            [0, 2, 1],    # 2y + z = 7
            [1, 1, 1]     # x + y + z = 6
        ]
        B = [
            1, 2, 3,      # direct assignments
            3, 5, 4,      # combinations
            4, 7, 6       # more combinations
        ]
        ge = GaussianElimination(A, B)
        ge.Solve()
        self.assertTrue(ge.was_run)             # Solver ran
        self.assertTrue(ge.solved)              # System is solvable
        self.assertTrue(all(ge.has_solution))   # All variables are determined
        self.assertEqual(len(ge.X), 3)          # Three variables in solution
        self.assertAlmostEqual(ge.X[0], 1.0, places=5)  # x = 1
        self.assertAlmostEqual(ge.X[1], 2.0, places=5)  # y = 2
        self.assertAlmostEqual(ge.X[2], 3.0, places=5)  # z = 3
