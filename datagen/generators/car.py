from typing import Optional, Union, List, Dict
import pandas as pd
from faker import Faker
import random
import os


def generate_cars(
        n: int = 100,
        seed: Optional[int] = None,
        external_data_path: Optional[str] = None,
        output_format: str = "dataframe"
) -> Union[pd.DataFrame, List[Dict], str]:
    """Generate deterministic synthetic car dataset."""
    if n < 1:
        raise ValueError("Number of cars (n) must be at least 1")

    valid_formats = ['dataframe', 'dict', 'csv', 'json']
    if output_format not in valid_formats:
        raise ValueError(f"output_format must be one of {valid_formats}")
    
    # Set deterministic randomness
    if seed is not None:
        random.seed(seed)
        Faker.seed(seed)

    fake = Faker()
   
    # Load base data
    if external_data_path and os.path.exists(external_data_path):
        cars_df = pd.read_csv(external_data_path)
    else:
        # Load internal CSV shipped with the package
        internal_path = os.path.join(os.path.dirname(__file__), "..", "data", "cars_base.csv")
        if not os.path.exists(internal_path):
            raise FileNotFoundError("Internal cars_base.csv not found in datagen/data/")
        cars_df = pd.read_csv(internal_path)

    # Validate inputs
    required_cols = {"make", "model", "base_price", "transmission", "fuel_type"}
    if not required_cols.issubset(cars_df.columns):
        raise ValueError(f"Input CSV must contain the following columns: {required_cols}")
    
    colors = [
        "Black", "White", "Silver", "Blue", "Red", "Gray", "Green", "Beige", "Yellow", "Orange"
    ]
        
    car_records = []

    for i in range(n):
        row = cars_df.sample(n=1, random_state=seed + i if seed is not None else None).iloc[0]

        make = row["make"]
        model = row["model"]
        base_price = float(row["base_price"])
        transmission = row["transmission"]
        
        # Synthetic attributes
        year = random.randint(2010, 2025)
        color = random.choice(colors)
       
        # Price variation (±20% depending on year)
        price_flactuation = random.uniform(0.8, 1.2)
        year_adjustment = 1 + ((year - 2015)) * 0.01
        price = round(base_price * price_flactuation * year_adjustment, -2)

        record = {
            "car_id": fake.uuid4(),
            "make": make,
            "model": model,
            "year": year,
            "color": color,
            "transmission_type": transmission,
            "price": price
        }

        car_records.append(record)

    # Convert to requested format
    if output_format == 'dict':
        return car_records

    df = pd.DataFrame(car_records)

    if output_format == 'dataframe':
        return df
    elif output_format == 'csv':
        return df.to_csv(index=False)
    elif output_format == 'json':
        return df.to_json(orient='records', indent=2)


def save_cars(
        cars: Union[pd.DataFrame, List[Dict]],
        filename: str,
        file_format: Optional[str] = None
) -> None:
    """Save generated car data to file in multiple formats."""
    if isinstance(cars, list):
        df = pd.DataFrame(cars)
    else:
        df = cars

    if file_format is None:
        if filename.endswith('.csv'):
            file_format = 'csv'
        elif filename.endswith('.json'):
            file_format = 'json'
        elif filename.endswith(('.xlsx', '.xls')):
            file_format = 'excel'
        elif filename.endswith('.parquet'):
            file_format = 'parquet'
        else:
            file_format = 'csv'

    if file_format == 'csv':
        df.to_csv(filename, index=False)
    elif file_format == 'json':
        df.to_json(filename, orient='records', indent=2)
    elif file_format == 'excel':
        df.to_excel(filename, index=False)
    elif file_format == 'parquet':
        df.to_parquet(filename, index=False)
    else:
        raise ValueError(f"Unsupported file format: {file_format}")

    print(f"✓ Saved {len(df)} car records to {filename}")


if __name__ == "__main__":
    print("Generating 10 sample cars...")
    cars = generate_cars(n=10, seed=42)
    print(cars)
    print(f"\nGenerated {len(cars)} cars")
    print(f"Columns: {list(cars.columns)}")
    print("\nSample summary:")
    print(cars[['make', 'model', 'year', 'price']].head().to_string(index=False))
