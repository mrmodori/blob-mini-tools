import ast
import operator

class SafeEvaluator:
    def __init__(self):
        self.allowed_ops = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.FloorDiv: operator.floordiv,
            ast.Mod: operator.mod,
            ast.Pow: operator.pow,
            ast.USub: operator.neg,
            ast.UAdd: operator.pos,
        }

    def eval(self, expr: str):
        """Safely evaluate a mathematical expression string."""
        def eval_node(node):
            if isinstance(node, ast.Constant):
                if isinstance(node.value, (int, float)):
                    return node.value
                raise ValueError("Unsupported constant")
            elif isinstance(node, ast.BinOp):
                op_type = type(node.op)
                if op_type in self.allowed_ops:
                    return self.allowed_ops[op_type](eval_node(node.left), eval_node(node.right))
                raise ValueError("Unsupported binary operator")
            elif isinstance(node, ast.UnaryOp):
                op_type = type(node.op)
                if op_type in self.allowed_ops:
                    return self.allowed_ops[op_type](eval_node(node.operand))
                raise ValueError("Unsupported unary operator")
            elif isinstance(node, ast.Expression):
                return eval_node(node.body)
            raise ValueError("Invalid expression")

        parsed = ast.parse(expr, mode='eval')
        return eval_node(parsed.body)
