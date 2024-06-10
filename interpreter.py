import ast
import operator as op
import math
import logging
import graphviz

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Supported operators
operators = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg
}

# Supported functions
functions = {
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'sqrt': math.sqrt,
    'log': math.log
}

# Function registry for user-defined functions
function_registry = {}


def eval_expr(expr, variables={}, user_functions={}):
    """
    Evaluate a mathematical expression with given variables and user functions.

    :param expr: Expression string
    :param variables: Dictionary of variables
    :param user_functions: Dictionary of user-defined functions
    :return: Evaluated result
    """
    try:
        validate_input(expr, variables, user_functions)
        # Update function registry with user functions
        function_registry.update(user_functions)
        # Parse expression
        tree = ast.parse(expr, mode='eval')
        return _eval(tree.body, variables)
    except Exception:
        logger.error(f"Error evaluating expression: {expr}", exc_info=True)
        raise


def _eval(node, variables):
    if isinstance(node, ast.Num):  # <number>
        return node.n
    elif isinstance(node, ast.BinOp):  # <left> <operator> <right>
        return operators[type(node.op)](_eval(node.left, variables),
                                        _eval(node.right, variables))
    elif isinstance(node, ast.UnaryOp):  # <operator> <operand> e.g., -1
        return operators[type(node.op)](_eval(node.operand, variables))
    elif isinstance(node, ast.Name):
        if node.id in variables:
            return variables[node.id]
        raise NameError(f"Undefined variable: {node.id}")
    elif isinstance(node, ast.Call):  # <function>(<arguments>)
        func = node.func.id
        args = [_eval(arg, variables) for arg in node.args]
        if func in functions:
            return functions[func](*args)
        elif func in function_registry:
            return function_registry[func](*args)
        raise NameError(f"Undefined function: {func}")
    else:
        raise TypeError(node)


def validate_input(expr, variables={}, user_functions={}):
    """
    Validate the input data to ensure correctness before evaluation.

    :param expr: Expression string
    :param variables: Dictionary of variables
    :param user_functions: Dictionary of user-defined functions
    :return: True if valid, raises an exception if invalid
    """
    try:
        ast.parse(expr, mode='eval')
        for var in variables:
            if not isinstance(var, str) or not var.isidentifier():
                raise ValueError(f"Invalid variable name: {var}")
        for func in user_functions:
            if not isinstance(func, str) or not func.isidentifier():
                raise ValueError(f"Invalid function name: {func}")
            if not callable(user_functions[func]):
                raise ValueError(f"Function {func} is not callable")
        return True
    except Exception:
        logger.error("Validation failed", exc_info=True)
        raise


def visualize_expr(expr):
    """
    Visualize the expression as a tree using Graphviz.

    :param expr: Expression string
    :return: Graphviz source object
    """
    try:
        tree = ast.parse(expr, mode='eval')
        graph = graphviz.Digraph()

        def add_nodes(node, parent=None):
            node_id = str(id(node))
            label = type(node).__name__
            if isinstance(node, ast.Num):
                label = str(node.n)
            elif isinstance(node, ast.Name):
                label = node.id
            elif isinstance(node, ast.BinOp):
                label = type(node.op).__name__
            elif isinstance(node, ast.UnaryOp):
                label = type(node.op).__name__
            elif isinstance(node, ast.Call):
                label = node.func.id

            graph.node(node_id, label)
            if parent:
                graph.edge(parent, node_id)

            for child in ast.iter_child_nodes(node):
                add_nodes(child, node_id)

        add_nodes(tree.body)
        return graph
    except Exception:
        logger.error(f"Error visualizing expression: {expr}", exc_info=True)
        raise


# if __name__ == '__main__':
#     expr = "a + 2 - sin(-0.3) * (b - c)"
#     variables = {'a': 1, 'b': 4, 'c': 2}
#     user_functions = {"foo": lambda x: x * 42}
#
#     result = eval_expr(expr, variables, user_functions)
#     print(f"Result: {result}")
#
#     graph = visualize_expr(expr)
#     graph.render('expression_tree', format='png', view=True)
