"""Bounded arithmetic calculator: no eval, assignments, or Python access."""
import ast
import math
import operator


def calculate(expression, variables):
    expression = expression.strip()
    if expression.startswith('='):
        expression = expression[1:].strip()
    expression = expression.replace('^', '**')
    if not expression.strip() or len(expression) > 1500:
        raise ValueError('Enter an expression of at most 1,500 characters.')
    try:
        tree = ast.parse(expression, mode='eval')
        if sum(1 for _ in ast.walk(tree)) > 300:
            raise ValueError('This expression is too long.')

        def visit(node):
            if isinstance(node, ast.Constant) and type(node.value) in (int, float):
                result = float(node.value)
            elif isinstance(node, ast.Name) and node.id in variables:
                result = float(variables[node.id])
            elif isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
                result = visit(node.operand) * (-1 if isinstance(node.op, ast.USub) else 1)
            elif isinstance(node, ast.BinOp) and type(node.op) in (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow):
                operations = {ast.Add:operator.add, ast.Sub:operator.sub, ast.Mult:operator.mul, ast.Div:operator.truediv, ast.Pow:operator.pow}
                left, right = visit(node.left), visit(node.right)
                if isinstance(node.op, ast.Pow) and (abs(right) > 100 or (left < 0 and right != int(right))):
                    raise ValueError('Use real powers with an exponent between -100 and 100.')
                result = operations[type(node.op)](left, right)
            elif (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                  and node.func.id in ('exp', 'sqrt', 'log', 'abs', 'min', 'max') and not node.keywords):
                args = [visit(arg) for arg in node.args]
                if node.func.id in ('min','max'):
                    if not 1 <= len(args) <= 20:
                        raise ValueError('Use one to twenty arguments for min or max.')
                    result = (min if node.func.id == 'min' else max)(args)
                else:
                    if len(args) != 1:
                        raise ValueError('This function takes one argument.')
                    result = {'exp':math.exp, 'sqrt':math.sqrt, 'log':math.log, 'abs':abs}[node.func.id](args[0])
            else:
                raise ValueError('Use numbers, the listed symbols, +, − (typed as -), *, /, parentheses, ^, exp, sqrt, log, abs, min and max.')
            if not math.isfinite(result) or abs(result) > 1e12:
                raise ValueError('The result is outside the calculator range.')
            return result

        return visit(tree.body)
    except (SyntaxError, ZeroDivisionError, OverflowError, TypeError, RecursionError) as exc:
        raise ValueError('Check the arithmetic, parentheses and denominators.') from exc
