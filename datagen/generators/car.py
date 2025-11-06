from typing import Optional, Union, List, Dict
import pandas as pd
from faker import Faker
import random
import os
from datagen.utils.io import save_data

# Common vehicles in Kenyan Market
KENYA_CAR_BASE = [
    {"make": "Toyota", "model": "Corolla", "base_price": 1800000, "transmission": "Automatic", "fuel_type": "Petrol"},
    {"make": "Toyota", "model": "Probox", "base_price": 1200000, "transmission": "Manual", "fuel_type": "Petrol"},
    {"make": "Nissan", "model": "Note", "base_price": 1400000, "transmission": "Automatic", "fuel_type": "Petrol"},
    {"make": "Mazda", "model": "Demio", "base_price": 1500000, "transmission": "Automatic", "fuel_type": "Petrol"},
    {"make": "Subaru", "model": "Forester", "base_price": 2500000, "transmission": "Automatic", "fuel_type": "Petrol"},
    {"make": "Mitsubishi", "model": "Outlander", "base_price": 2700000, "transmission": "Automatic", "fuel_type": "Diesel"},
    {"make": "Volkswagen", "model": "Passat", "base_price": 2200000, "transmission": "Automatic", "fuel_type": "Petrol"},
    {"make": "BMW", "model": "X3", "base_price": 4500000, "transmission": "Automatic", "fuel_type": "Diesel"},
    {"make": "Mercedes-Benz", "model": "C-Class", "base_price": 5500000, "transmission": "Automatic", "fuel_type": "Petrol"},
    {"make": "Isuzu", "model": "D-Max", "base_price": 3200000, "transmission": "Manual", "fuel_type": "Diesel"}
]

def generate_cars(
        n: int = 100,
        seed: Optional[int] = None,
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
   
    colors = ["Black", "White", "Silver", "Blue", "Red", "Gray", "Green", "Beige", "Maroon"]
    dealer_cities = ["Nairobi", "Mombasa", "Kisumu", "Eldoret", "Nakuru"]
    
        
    records = []

    for i in range(n):
        car = random.choice(KENYA_CAR_BASE)
        make, model = car["make"], car["model"]
        base_price = car["base_price"]
        transmission = car["transmission"]
        fuel_type = car["fuel_type"]
        
        # Synthetic attributes
        year = random.randint(2008, 2025)
        color = random.choice(colors)
        dealer_city = random.choice(dealer_cities)
       
        # Simulate depreciation or appreciation
        age_factor = 1 - ((2025 - year) * 0.03)
        price_kes = max(500000, round(base_price * age_factor * random.uniform(0.9, 1.1), -4))

        record = {
            "car_id": fake.uuid4(),
            "make": make,
            "model": model,
            "year": year,
            "color": color,
            "transmission_type": transmission,
            "fuel_type": fuel_type,
            "assembled_in": "Japan",
            "dealer_city": dealer_city,
            "price_kes": price_kes
        }
        records.append(record)

    df = pd.DataFrame(records)

    # Convert to requested format
    if output_format == "dataframe":
        return df
    elif output_format == "csv":
        return df.to_csv(index=False)
    elif output_format == "json":
        return df.to_json(orient="records", indent=2)
    elif output_format == "dict":
        return records

if __name__ == "__main__":
    print("Generating 10 Kenya-market cars...")
    cars = generate_cars(n=10, seed=42)
    print(cars)
    print(f"\nGenerated {len(cars)} cars")
    print(f"Columns: {list(cars.columns)}")
    save_data(cars, filename="./output/kenyan_cars.csv", file_format="csv")
    print("\nCommon cars in the Kenyan market successfully generated and saved!")
