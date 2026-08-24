import math

class UnitConverter:
    def __init__(self):
        # Conversion factors relative to a base unit
        self.conversions = {
            "Length": {
                "base": "meters",
                "units": {
                    "meters": 1.0,
                    "kilometers": 1000.0,
                    "centimeters": 0.01,
                    "millimeters": 0.001,
                    "miles": 1609.34,
                    "yards": 0.9144,
                    "feet": 0.3048,
                    "inches": 0.0254
                }
            },
            "Mass": {
                "base": "grams",
                "units": {
                    "grams": 1.0,
                    "kilograms": 1000.0,
                    "milligrams": 0.001,
                    "pounds": 453.592,
                    "ounces": 28.3495
                }
            },
            "Volume": {
                "base": "liters",
                "units": {
                    "liters": 1.0,
                    "milliliters": 0.001,
                    "gallons": 3.78541,
                    "cups": 0.236588
                }
            }
        }

    def convert(self, value, category, from_unit, to_unit):
        """Converts a value from one unit to another within a category."""
        if category not in self.conversions:
            raise ValueError(f"Category '{category}' not supported.")
        
        cat_data = self.conversions[category]
        units = cat_data["units"]
        
        if from_unit not in units or to_unit not in units:
            raise ValueError(f"Invalid units for {category}. Supported: {list(units.keys())}")

        # Convert from_unit to base unit
        value_in_base = value * units[from_unit]
        
        # Convert from base unit to to_unit
        result = value_in_base / units[to_unit]
        
        steps = [
            f"Starting value: {value} {from_unit}",
            f"Convert to base ({cat_data['base']}): {value_in_base} {cat_data['base']}",
            f"Convert from base to {to_unit}: {result} {to_unit}"
        ]
        
        return result, steps
