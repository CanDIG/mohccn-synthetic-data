from clinical_etl import mappings
import ast

def self(data_values):
    cell = mappings.single_val(data_values)
    if cell is not None:
        result = ast.literal_eval(cell)
    else:
    # Handle the case when cell is None
        result = None  
    return result