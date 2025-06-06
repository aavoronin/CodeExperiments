import numpy as np
"""
implement unit tests (give py code for unit tests) as instructed: Give me the full py script for this: 
1) Implement GaussianElimination class 
2) The class accepts matrix A of n x m size (it is possible that n = m and n > m and n < m) and 
vector B of size n that represent system of equations A * X = B where X are variables to be determined in solution. 
3) The class should contain methods __init__ that takes A and B and verifies that they fit by size, 
also contain method Solve that does GaussianElimination 
4) The class should have at least the following properties (A, B, n, m, X, error, was_run, solved, has_solution). 
After running __init__ and Solve the properties should have values error=True is matrix was properly init and solved. 
was_run should have true if Solve was executed successfully. 
has_solution should be a boolean vector indicating for each element of X has definite solution value or 
false if it might have multiple sulutions. 
X should contain values for those variables which have  definite solutions and None for those which are not. 
5) The type of matrix and vector elements should be double. 
6) Algorithm should was for overflow and prevent division for elements where are between -1E-50 and +1E-50 . 
Such element should be treated as 0 and assigned 0. 
7) Implement unit texts that all possible situations 
a) A and B incomparable in size -- error
b) system is solves successfully and each X has solution 
b) system is solves successfully  but is contradictory and has no solution 
c) system has only some variables solved 
d) system has redundant equations but is solved for all variables 
d) system has redundant equations but is solved for some variables 
8) use n, m in the range 2 - 10 for tests 
"""



class GaussianElimination:
    def __init__(self, A, B):
        # Flags and results
        self.error = False          # True if initialization failed due to bad inputs
        self.was_run = False        # True if Solve() has been executed
        self.solved = False         # True if the system was at least partially solved
        self.has_solution = []      # List indicating which variables have unique solutions
        self.X = []                 # Final solution vector (None if unknown)

        # Convert input lists to NumPy arrays of float64 for accurate math
        try:
            self.A = np.array(A, dtype=np.float64)  # Coefficient matrix
            self.B = np.array(B, dtype=np.float64)  # Right-hand side vector
        except:
            self.error = True  # Error converting to float64 arrays
            return

        # Validate input dimensions
        if self.A.ndim != 2 or self.B.ndim != 1:
            self.error = True
            return

        self.n, self.m = self.A.shape  # n = number of equations (rows), m = number of variables (columns)

        # Ensure the B vector has one value per equation
        if self.B.shape[0] != self.n:
            self.error = True

    def Solve(self):
        # Do not proceed if there was an initialization error
        if self.error:
            return

        self.was_run = True

        # Copy A and B to avoid modifying original data
        A = self.A.copy()
        B = self.B.copy()
        n, m = self.n, self.m
        EPS = 1e-50  # Very small threshold to treat as zero to prevent division by near-zero

        # Create augmented matrix [A|B]
        Ab = np.hstack([A, B.reshape(-1, 1)])

        row = 0  # Index of the current pivot row
        for col in range(m):  # For each column (variable)
            pivot_row = None  # Find a pivot row
            for r in range(row, n):  # Search below current row
                if abs(Ab[r][col]) > EPS:  # If entry is significantly non-zero
                    pivot_row = r
                    break

            if pivot_row is None:
                continue  # Skip column if no pivot found (free variable)

            # Swap current row with pivot_row to bring pivot into place
            Ab[[row, pivot_row]] = Ab[[pivot_row, row]]

            # Normalize pivot row so pivot element becomes 1
            pivot = Ab[row][col]
            if abs(pivot) < EPS:
                pivot = 0.0  # Treat very small pivots as zero

            if pivot != 0:
                Ab[row] = Ab[row] / pivot  # Normalize row

            # Eliminate variable from all rows below
            for r in range(row + 1, n):
                factor = Ab[r][col]
                Ab[r] = Ab[r] - factor * Ab[row]

            row += 1  # Move to next row

        # Back-substitution phase
        X = [None] * m  # Initialize solution list with None (unknowns)

        for i in reversed(range(n)):  # Start from bottom row
            coeffs = Ab[i, :-1]       # Coefficients of variables
            rhs = Ab[i, -1]           # Right-hand side value

            nz = np.where(np.abs(coeffs) > EPS)[0]  # Find non-zero coefficients

            if len(nz) == 0:
                if abs(rhs) > EPS:
                    # Row looks like 0 = non-zero → contradiction
                    self.solved = True
                    self.has_solution = [False] * m
                    self.X = [None] * m
                    return
                else:
                    # Row is 0 = 0 → redundant equation
                    continue

            # Leading variable index
            leading = nz[0]

            # Compute sum of known values for variables already solved
            sum_known = sum(Ab[i][j] * (X[j] if X[j] is not None else 0) for j in nz[1:])

            val = rhs - sum_known  # Adjust RHS based on knowns
            coeff = Ab[i][leading]

            if abs(coeff) < EPS:
                coeff = 0.0

            if coeff != 0:
                X[leading] = val / coeff  # Solve for the leading variable

        self.X = X
        self.has_solution = [x is not None for x in X]  # Mark which variables have unique solutions
        self.solved = True if any(self.has_solution) else False  # True if any variable is solved
