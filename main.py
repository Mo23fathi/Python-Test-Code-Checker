import ast
import builtins

def find_unused_variables(module):
    unused_vars = []

    # Collect all names defined in the module
    defined_names = set(
        node.id for node in ast.walk(module) if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store))

    # Find all names used in the module
    used_names = set(
        node.id for node in ast.walk(module) if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load))

    # Check if any defined names are not used in the module
    for defined_name in defined_names:
        if defined_name not in used_names:
            # Check if the name is used in any nested scopes
            if not any(defined_name in used_names for used_names in ast.walk(module) if
                       isinstance(module, (ast.FunctionDef, ast.ClassDef))):
                unused_vars.append(defined_name)

    if unused_vars.__len__() != 0:
        unused_vars.insert(0, "unused variables : ")
        return unused_vars
    else:
        return "unused variables test passed"


def check_variable_assignments(module):
    bugs = []
    for node in ast.walk(module):
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
            if isinstance(node.value, ast.BinOp) and isinstance(node.value.op, ast.Div) and isinstance(
                    node.value.right, ast.Num) and node.value.right.n == 0:
                bugs.append(node.targets[0].id)

    if bugs.__len__() != 0:
        bugs.insert(0, "Incorrect variables assignment divided by zero : ")
        return bugs
    else:
        return "Incorrect variables assignment divided by zero test passed "


def check_infinite_loop(module):
    bugs = []
    for node in ast.walk(module):
        if isinstance(node, ast.While) and isinstance(node.test, ast.Constant) and node.test.value == True:
            bugs.append("Infinite loop")
    if bugs.__len__() != 0:
        return bugs
    else:
        return "No infinite loops test passed "


def check_empty_print(module):
    bugs = []
    for node in ast.walk(module):
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call) and isinstance(node.value.func,
                                                                                          ast.Name) and node.value.func.id == "print":
            if len(node.value.args) == 0:
                bugs.append("Empty print statement")
    if bugs.__len__() != 0:
        return bugs
    else:
        return "No empty print test passed "



def analyze_module(module):
    bugs = []
    for node in ast.walk(module):
        if isinstance(node, ast.ClassDef) and len(node.bases) > 0:
            for base in node.bases:
                if isinstance(base, ast.Attribute) and isinstance(base.value,
                                                                  ast.Name) and base.value.id == "os" and base.attr == "Path":
                    bugs.append("Incorrect use of class inheritance")

    # Check if there are any bugs found
    if len(bugs) != 0:
        return bugs
    else:
        return "Incorrect use of class inheritance test passed"




def find_dict_initialization_bugs(module):

    bugs = []
    for node in ast.walk(module):
        if isinstance(node, ast.Dict) and len(node.keys) > 0:
            for key_node in node.keys:
                if not isinstance(key_node, ast.Constant):
                    bugs.append("Incorrect dictionary initialization")
    if len(bugs) != 0:
        return bugs
    else:
        return "Incorrect dictionary initialization test passed"

def find_undefined_variables(module):
    bugs = []
    for node in ast.walk(module):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            if not any(isinstance(parent, ast.FunctionDef) for parent in ast.walk(node)):
                # Check if the variable is actually defined in the module
                if not any(isinstance(n, ast.Name) and n.id == node.id and isinstance(n.ctx, ast.Store) for n in ast.walk(module)):
                    # Check if the variable is a built-in function or a variable in the builtins module
                    if node.id not in dir(builtins):
                        if not any(isinstance(n, ast.ImportFrom) and n.module == "builtins" and node.id in [a.name for a in n.names] for n in ast.walk(module)):
                            bugs.append(node.id)
    if bugs.__len__() != 0:
        bugs.insert(0, "undefined variables : ")
        return bugs
    else:
        return "Check for undefined variables test passed "




# Define the function to detect bugs
def detect_bugs(path):
    with open(path, 'r') as f:
        x = f.read()

    # Parse the code string into an AST
    try:
        module = ast.parse(x)
    except SyntaxError as e:
        return f"Syntax error: {e}"

    # Check for bugs in the AST
    bugs = []


    # Bug 1: Check for unused variables (kiro)
    bugs.append(find_unused_variables(module))

    # Bug 2: Check Incorrect variables assignment divided by zero (kiro)
    bugs.append(check_variable_assignments(module))

    # bug 3 : Check for undefined variables (kiro)
    bugs.append(find_undefined_variables(module))

    # Bug 4: Check for infinite loops (helmy)
    bugs.append(check_infinite_loop(module))

    # Bug 5: Check for Empty print statement (helmy)
    bugs.append(check_empty_print(module))

    # bug 6 : Check for incorrect use of class inheritance (sayed)
    bugs.append(analyze_module(module))

    # Bug 7: Check for ising vars in dictionary initialization (sayed)
    bugs.append(find_dict_initialization_bugs(module))


    return bugs


print(detect_bugs("error.py"))
