# Bug 1: Check for unused variables (kiro)
def unused_var(x, y):
    a = 1
    b = 2
    c = a + b  # this variable is used
    d = x * y
    e = 1  # this variable is not defined
    return c


# Bug 2: Check Incorrect variables assignment divided by zero (kiro)
a = 1 / 0

# bug 3 : Check for undefined variables (kiro)
r=5
x= r + t

# Bug 4: Check for infinite loops (helmy)
while True:
    print("Infinite loop")

# Bug 5: Check for Empty print statement (helmy)
print()

# bug 6 : Check for incorrect use of class inheritance (sayed)
import os
class IncorrectPath(os.Path):
    pass


# Bug 7: Check for ising vars in dictionary initialization (sayed)
my_var = "ddd"
my_dict = {my_var: "value"}
