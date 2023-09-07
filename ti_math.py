from ti_interop import tiexec
from ti_collections import TiCollections

import sys
if sys.platform == 'win32':
    from lib.wrappers import ensure_paired_type, ensure_paired_or_single_type
else:    
    from wrappers import ensure_paired_type, ensure_paired_or_single_type

class TiMath:
    
    @ensure_paired_type((int, float, list))
    def lcm(self, lhs, rhs):
        pass
    
    @ensure_paired_or_single_type((int, float, list))
    def max(self, lhs, rhs=None):
        pass
    
    def exact(self, val: (str, list)):
        if TiCollections.is_reg_py_list(val):
            val = TiCollections.to_py_list(val)
        elif TiCollections.is_py_mat(val):
            val = TiCollections.to_py_mat(val)
        return tiexec("exact", val)
    
    
    """
        solve(Equation, Var) ⇒ Boolean expression
        solve(Equation, Var=Guess) ⇒ Boolean expression
        solve(Inequality, Var) ⇒ Boolean expression
        solve(Eqn1 and Eqn2[and …],VarOrGuess1, VarOrGuess2[, …]) ⇒ Boolean expression
        solve(SystemOfEqns, VarOrGuess1,VarOrGuess2[, …]) ⇒ Boolean expression
        solve({Eqn1, Eqn2 [,...]} {VarOrGuess1,VarOrGuess2 [, … ]}) ⇒ Boolean expression
        
        • solve(Equation, Var=Guess)|lowBound<Var<upBound
        • solve(Equation, Var)|lowBound<Var<upBound
        • solve(Equation, Var=Guess)
    """
    def solve(self, *args):
        pass
    
    """
        linSolve( SystemOfLinearEqns, Var1, Var2, ...) ⇒ list
        linSolve(LinearEqn1 and LinearEqn2 and..., Var1, Var2, ...) ⇒ list
        linSolve({LinearEqn1, LinearEqn2, ...},Var1, Var2, ...) ⇒ list
        linSolve(SystemOfLinearEqns, {Var1, Var2, ...}) ⇒ list
        linSolve(LinearEqn1 and LinearEqn2 and..., {Var1, Var2, ...}) ⇒ list
        linSolve({LinearEqn1, LinearEgn2, ...},{Var1, Var2, ...})  ⇒ list
        Returns a list of solutions for the variablesVar1, Var2, ...
    """

    # Define a function to check if the zero vector is in the set
    def check_zero_vector(self):
        # CAS: Check if the zero vector [0, 0, 0]^T satisfies the conditions defining the set
        # Params: The equations defining the set
        # Return: True if zero vector is in the set, False otherwise
        pass

    # Define a function to check closure under addition
    def check_addition_closure(self):
        # CAS: Take any two generic vectors A and B from the set
        # Compute their sum A + B and check if it's in the set
        # Params: The equations defining the set
        # Return: True if the set is closed under addition, False otherwise
        pass

    # Define a function to check closure under scalar multiplication
    def check_scalar_multiplication_closure(self):
        # CAS: Take any generic vector A from the set and a scalar c
        # Compute the scalar multiple cA and check if it's in the set
        # Params: The equations defining the set
        # Return: True if the set is closed under scalar multiplication, False otherwise
        pass

    def is_subspace(self):
        if not self.check_zero_vector():
            return False, "The zero vector is not in the set."
        
        if not self.check_addition_closure():
            return False, "The set is not closed under addition."
        
        if not self.check_scalar_multiplication_closure():
            return False, "The set is not closed under scalar multiplication."
        
        return True, "The set is a subspace of R^3." 
    
    
# a,b,h = symbols('a b h')

# eq1 = ( -3, -6*a -15 )
# eq2 = ( 2, 1*a + 7 )
# eq3 = ( 3, 8*a + h )
# a.substitute(2)
# print(a.symbolic())
# print(type(a))
# print(a.value)