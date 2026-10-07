from typing import Union, List, Dict
import pandas as pd

VALID_FORMATS = ['dataframe', 'dict', 'csv', 'json']

def validate_generator_inputs(n: int, output_format: str) -> None:
    if n < 1:
        raise ValueError("Number of records (n) must be at least 1.")
    if output_format not in VALID_FORMATS:
        raise ValueError(f"output_format must be one of {VALID_FORMATS}")

def format_output(records: List[Dict], output_format: str) -> Union[pd.DataFrame, List[Dict], str]:
    if output_format == 'dict':
        return records

    df = pd.DataFrame(records)

    if output_format == 'dataframe':
        return df
    elif output_format == 'csv':
        return df.to_csv(index=False)
    elif output_format == 'json':
        return df.to_json(orient='records', indent=2)