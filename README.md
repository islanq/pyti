# pyti
A python library for the TI-Nspire designed to show step by step math solving.


## Parsing systems of Equations from Strings
```python
from matrix import parse_equation_systems

print(parse_equation_systems([["-4x−28y=-40"],["x-4y-2z=-3"],["-2x-3y+4*z=-5"]]))
print(parse_equation_systems("-4x−28*y=-40","x-4y-2z=-3","-2x-3y+4z=-5"))
print(parse_equation_systems("x + y = 2", "2x + 3y = 5"))
```

```
[[-4, -28, 0, -40], [1, -4, -2, -3], [-2, -3, 4, -5]]
[[-4, -28, 0, -40], [1, -4, -2, -3], [-2, -3, 4, -5]]
[[1, 1, 2], [2, 3, 5]]
```

## Matrix arithmetic

```python
from matrix import Matrix

m1 = Matrix([[1,2,3], [3,2,1], [2,1,3]])
m2 = Matrix([[4,3,2], [2,3,4], [3,4,2]])
m3 = Matrix([[1,1,1], [1,1,1], [1,1,0]])
print("add m1 and m2")
print(m1 + m2)

print("\nsub m2 from m1")
print(m1 - m2)

print("\nraise m3 to the power of 2")
print(m3 ** 2)
```

```
add m1 and m2
[[ 1+4, 2+3, 3+2 ],
 [ 3+2, 2+3, 1+4 ],
 [ 2+3, 1+4, 3+2 ]]
[[ 5, 5, 5 ],
 [ 5, 5, 5 ],
 [ 5, 5, 5 ]]

sub m2 from m1
[[ 1-4, 2-3, 3-2 ],
 [ 3-2, 2-3, 1-4 ],
 [ 2-3, 1-4, 3-2 ]]
[[ -3, -1, 1 ],
 [ 1, -1, -3 ],
 [ -1, -3, 1 ]]

raise m3 to the power of 2
[[ 1*1+0*1+0*1, 1*1+0*1+0*1, 1*1+0*1+0*0 ],
 [ 0*1+1*1+0*1, 0*1+1*1+0*1, 0*1+1*1+0*0 ],
 [ 0*1+0*1+1*1, 0*1+0*1+1*1, 0*1+0*1+1*0 ]]
[[ 1*1+1*1+1*1, 1*1+1*1+1*1, 1*1+1*1+1*0 ],
 [ 1*1+1*1+1*1, 1*1+1*1+1*1, 1*1+1*1+1*0 ],
 [ 1*1+1*1+0*1, 1*1+1*1+0*1, 1*1+1*1+0*0 ]]
[[ 3, 3, 2 ],
 [ 3, 3, 2 ],
 [ 2, 2, 2 ]]
```
# REF and RREF
```python
# Section 1.2 P 7

m = Matrix([[-1, -1, -7], [1, -1, 3], [-2, 3, 1]])
print(m.is_ref()) 
print(m.is_rref())
m.to_ref()
m.to_rref()
```

```
False
False
Swapping row 1 with row 3: r1↔r3
[[ -2, 3, 1 ],
 [ 1, -1, 3 ],
 [ -1, -1, -7 ]]
Divide row 1 by -2
[[ 1.0, -1.5, -0.5 ],
 [ 1, -1, 3 ],
 [ -1, -1, -7 ]]
Subtract 1 times row 1 from row 2
[[ 1.0, -1.5, -0.5 ],
 [ 0.0, 0.5, 3.5 ],
 [ -1, -1, -7 ]]
Subtract -1 times row 1 from row 3
[[ 1.0, -1.5, -0.5 ],
 [ 0.0, 0.5, 3.5 ],
 [ 0.0, -2.5, -7.5 ]]
Swapping row 2 with row 3: r2↔r3
[[ 1.0, -1.5, -0.5 ],
 [ 0.0, -2.5, -7.5 ],
 [ 0.0, 0.5, 3.5 ]]
Divide row 2 by -2.5
[[ 1.0, -1.5, -0.5 ],
 [ -0.0, 1.0, 3.0 ],
 [ 0.0, 0.5, 3.5 ]]
Subtract 0.5 times row 2 from row 3
[[ 1.0, -1.5, -0.5 ],
 [ -0.0, 1.0, 3.0 ],
 [ 0.0, 0.0, 2.0 ]]
Divide row 3 by 2.0
[[ 1.0, -1.5, -0.5 ],
 [ -0.0, 1.0, 3.0 ],
 [ 0.0, 0.0, 1.0 ]]
The matrix in Row Echelon Form (REF) is:
[[ 1.0, -1.5, -0.5 ],
 [ -0.0, 1.0, 3.0 ],
 [ 0.0, 0.0, 1.0 ]]
The matrix in Row Echelon Form (REF) is:
[[ 1.0, -1.5, -0.5 ],
 [ -0.0, 1.0, 3.0 ],
 [ 0.0, 0.0, 1.0 ]]
Subtract 3.0 times row 3 from row 2
[[ 1.0, -1.5, -0.5 ],
 [ -0.0, 1.0, 0.0 ],
 [ 0.0, 0.0, 1.0 ]]
Subtract -0.5 times row 3 from row 1
[[ 1.0, -1.5, 0.0 ],
 [ -0.0, 1.0, 0.0 ],
 [ 0.0, 0.0, 1.0 ]]
Subtract -1.5 times row 2 from row 1
[[ 1.0, 0.0, 0.0 ],
 [ -0.0, 1.0, 0.0 ],
 [ 0.0, 0.0, 1.0 ]]
The matrix in Reduced Row Echelon Form (RREF) is:
[[ 1.0, 0.0, 0.0 ],
 [ -0.0, 1.0, 0.0 ],
 [ 0.0, 0.0, 1.0 ]]
```

# Gaussian Elimination (Lin Solve w/ Steps)
```python
# Section 1.2 P 7
from matrix import gaussian_elimination
from matrix import Matrix

m = Matrix([[-1, -1, -7], [1, -1, 3]])
gaussian_elimination(m, [-2, 3, 1])
```
```
Normalize row 1 with pivot -1 by dividing row 1 by -1
    1.00 |     1.00 |     7.00 |     2.00
    1.00 |    -1.00 |     3.00 |     3.00
----------------------------------------
Eliminate below pivot in column 1 by subtracting 1 * row 1 from row 2
    1.00 |     1.00 |     7.00 |     2.00
    0.00 |    -2.00 |    -4.00 |     1.00
----------------------------------------
Normalize row 2 with pivot -2.0 by dividing row 2 by -2.0
    1.00 |     1.00 |     7.00 |     2.00
   -0.00 |     1.00 |     2.00 |    -0.50
----------------------------------------
Back substitution for x_2
x[2] = -0.5
Back substitution for x_1
x[1] = 2.5

[2.5, -0.5, 0]
```