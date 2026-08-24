import re
import json
import os
import statistics
import math
from datetime import datetime
from sympy import sympify, expand, symbols
from converter import UnitConverter

class MathEngine:
    def __init__(self, variables=None, history_file="history.json"):
        self.variables = variables if variables is not None else []
        self.steps = []
        self.current_expression = ""
        self.history_file = history_file
        self.history = self._load_history()
        self.converter = UnitConverter()

    def _load_history(self):
        """Loads calculation history from a JSON file."""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []

    def _save_history_to_disk(self):
        """Saves the current history list to the JSON file."""
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.history, f, indent=4)
        except IOError as e:
            print(f"Error saving history: {e}")

    def _record_step(self, action, result):
        """Logs an internal calculation step."""
        formatted_res = format(result, '.4f') if isinstance(result, (float, int)) else result
        self.steps.append(f"{action} -> {formatted_res}")

    def _save_to_history(self, expression, result, format_type):
        """Archives the calculation with a timestamp and persists it."""
        now = datetime.now()
        timestamp = now.strftime("%H:%M:%S")
        entry = {
            "timestamp": timestamp,
            "expression": expression,
            "result": result,
            "format": format_type,
            "steps": list(self.steps)
        }
        self.history.append(entry)
        self._save_history_to_disk()

    def get_history(self):
        """Returns the calculation history."""
        return self.history

    def calculate_statistics(self, data_str, operation):
        """Calculates statistics for a dataset with step-by-step breakdown."""
        self.steps = []
        self.current_expression = data_str
        
        try:
            clean_data = data_str.replace(',', ' ').split()
            numbers = [float(x) for x in clean_data]
            
            if not numbers:
                raise ValueError("No numbers found in the dataset.")
            
            self._record_step("Data Parsing", f"Dataset: {numbers}")
            self._record_step("Count", f"N = {len(numbers)}")

            result = None
            if operation == "mean":
                total_sum = sum(numbers)
                self._record_step("Summation", f"Sum = {total_sum}")
                result = total_sum / len(numbers)
                self._record_step("Division", f"{total_sum} / {len(numbers)} = {result}")
            elif operation == "median":
                sorted_nums = sorted(numbers)
                self._record_step("Sorting", f"Sorted Data: {sorted_nums}")
                n = len(sorted_nums)
                if n % 2 == 1:
                    result = sorted_nums[n // 2]
                else:
                    mid1 = sorted_nums[n // 2 - 1]
                    mid2 = sorted_nums[n // 2]
                    result = (mid1 + mid2) / 2
                    self._record_step("Average of middle elements", f"({mid1} + {mid2}) / 2 = {result}")
            elif operation == "mode":
                try:
                    result = statistics.mode(numbers)
                    self._record_step("Frequency Check", f"Most frequent value: {result}")
                except statistics.StatisticsError:
                    from collections import Counter
                    counts = Counter(numbers)
                    max_count = max(counts.values())
                    modes = [k for k, v in counts.items() if v == max_count]
                    result = modes[0]
                    self._record_step("Frequency Check", f"Multiple modes found. Picking first: {result}")
            elif operation == "variance":
                result = statistics.variance(numbers)
                self._record_step("Variance Calculation", f"Calculated variance: {result}")
            elif operation == "std_dev":
                result = statistics.stdev(numbers)
                self._record_step("Standard Deviation Calculation", f"Calcul: {result}")
            else:
                raise ValueError(f"Unknown operation: {operation}")

            res_str = f"{result:g}"
            self._save_to_history(data_str, res_str, operation)
            return res_str, self.steps
        except Exception as e:
            self._record_step("Failure", str(e))
            return None, self.steps

    def solve_geometry(self, shape, operation, params):
        """Calculates Area or Perimeter for 2D/3D shapes."""
        self.steps = []
        shape = shape.lower()
        operation = operation.lower()
        
        try:
            result = None
            if shape == "circle":
                r = params['radius']
                self._record_step("Input", f"Radius = {r}")
                if operation == "area":
                    result = math.pi * (r**2)
                    self._record_step("Formula", "π * r²")
                    self._record_step("Calculation", f"π * {r}² = {result:g}")
                elif operation == "perimeter":
                    result = 2 * math.pi * r
                    self._record_step("Formula", "2 * π * r")
                    self._record_step("Calculation", f"2 * π * {r} = {result:g}")
            elif shape == "rectangle":
                l, w = params['length'], params['width']
                self._record_step("Input", f"L={l}, W={w}")
                if operation == "area":
                    result = l * w
                    self._record_step("Formula", "L * W")
                    self._record_step("Calculation", f"{l} * {w} = {result:g}")
                elif operation == "perimeter":
                    result = 2 * (l + w)
                    self._record_step("Formula", "2 * (L + W)")
                    self._record_step("Calculation", f"2 * ({l} + {w}) = {result:g}")
            elif shape == "square":
                s = params['side']
                self._record_step("Input", f"Side = {s}")
                if operation == "area":
                    result = s**2
                    self._record_step("Formula", "s²")
                    self._record_step("Calculation", f"{s}² = {result:g}")
                elif operation == "perimeter":
                    result = 4*s
                    self._record_step("Formula", "4 * s")
                    self._record_step("Calculation", f"4 * {s} = {result:g}")
            elif shape == "triangle":
                if operation == "area":
                    b, h = params['base'], params['height']
                    self._record_step("Input", f"Base = {b}, Height = {param_h}")
                    result = 0.5 * b * h
                    self._record_step("Formula", "0.5 * b * h")
                    self._record_step("Calculation", f"0.5 * {b} * {h} = {result:g}")
                elif operation == "perimeter":
                    sides = [params.get('side1', 1), params.get('side2', 1), params.get('side3', 1)]
                    result = sum(sides)
                    self._record_step("Input", f"Sides = {sides}")
                    self._record_step("Formula", "sum(sides)")
                    self._record_step("Calculation", f"Sum = {result:g}")
            elif shape == "sphere":
                r = params['radius']
                self._record_step("Input", f"Radius = {r}")
                if operation == "volume":
                    result = (4/3) * math.pi * (r**3)
                    self._record_step("Formula", "(4/3) * π * r³")
                    self._record_step("Calculation", f"(4/3) * π * {r}³ = {result:g}")
                else:
                    result = 4 * math.pi * (r**2)
                    self._record_step("Formula", "4 * π * r²")
                    self._record_step("Calculation", f"4 * π * {r}² = {result:g}")
            else:
                raise ValueError(f"Shape {shape} not implemented")

            res_str = f"{result:g}"
            self._save_to_history(shape, res_str, operation)
            return res_str, self.steps
        except Exception as e:
            self._record_step("Error", str(e))
            return None, self.steps

    def solve(self, expression_str, format_type='decimal'):
        """Standard algebra solver."""
        self.steps = []
        clean_expr = expression_str.replace('^', '**')
        self.current_expression = clean_expr
        
        try:
            syms = symbols(self.variables)
            local_dict = {s: s for s in syms}
            
            while '(' in self.current_expression:
                match = re.search(r'\(([^()]+)\)', self.current_expression)
                if not match: break
                inner_content = match.group(1).replace('^', '**')
                inner_result = sympify(inner_content, locals=local_dict)
                self._record_step(f"Solved parentheses: ({match.group(1)})", inner_result)
                self.current_expression = self.current_expression.replace(f"({match.group(1)})", str(inner_result), 1)

            final_expr = sympify(self.current_expression, locals=local_dict)
            
            if format_type == 'expanded':
                res_obj = expand(final_expr)
                res_str = str(res_obj)
            elif format_type == 'fraction':
                res_obj = final_expr.as_rational()
                res_str = str(res_obj)
            else:
                res_obj = final_expr.evalf(10)
                res_str = f"{res_obj:g}"

            self._save_to_history(expression_str, res_str, format_type)
            return res_str, self.steps
        except Exception as e:
            self._record_step("Error", str(e))
            return None, self.steps

    def solve_trig(self, expression_str, unit='degrees', format_type='decimal'):
        """Trigonometry solver."""
        self.steps = []
        try:
            expr_str = expression_str.replace('^', '**')
            self._record_step("Input", expr_str)
            working_expr = expr_str
            if unit == 'degrees':
                patterns = [r'(sin|cos|tan|asin|acos|atan)\s*\(\s*([\d\.]+)\s*\)']
                for pattern in patterns:
                    def repl_func(m):
                        func, val = m.group(1), float(m.group(2))
                        return f"{func}({math.radians(val)})"
                    working_expr = re.sub(pattern, repl_func, working_expr)
                self._record_step("Unit Conversion", "Converted degrees to radians")

            final_expr = sympify(working_expr)
            self._record_step("Parsed Expression", str(final_expr))
            
            if format_type == 'decimal':
                res_str = f"{final_expr.evalf(10):g}"
            elif format_type == 'fraction':
                res_str = str(final_expr.as_rational())
            else:
                res_str = str(final_expr)
            
            self._record_step("Result", res_str)
            self._save_to_history(expression_str, res_str, unit)
            return res_str, self.steps
        except Exception as e:
            self._record_step("Error", str(e))
            return None, self.steps
