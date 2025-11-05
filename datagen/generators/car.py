from typing import Optional, Union, List, Dict
import pandas as pd
from faker import Faker
import random

# Vehicle data categories
CAR_DATA = {
    'Toyota': {
        'models': ['Corolla', 'Camry', 'RAV4', 'Highlander', 'Prius', 'Land Cruiser'],
        'origins': 'Japan'
    },
    'Honda': {
        'models': ['Civic', 'Accord', 'CR-V', 'Pilot', 'Fit', 'Odyssey'],
        'origins': 'Japan'
    },
    'Ford': {
        'models': ['Fiesta', 'Focus', 'Fusion', 'Escape', 'Explorer', 'Mustang', 'F-150'],
        'origins': 'USA'
    },
    'Chevrolet': {
        'models': ['Spark', 'Malibu', 'Equinox', 'Traverse', 'Tahoe', 'Silverado'],
        'origins': 'USA'
    },
    'BMW': {
        'models': ['3 Series', '5 Series', '7 Series', 'X1', 'X3', 'X5', 'X7'],
        'origins': 'Germany'
    },
    'Mercedes-Benz': {
        'models': ['A-Class', 'C-Class', 'E-Class', 'S-Class', 'GLA', 'GLC', 'GLE'],
        'origins': 'Germany'
    },
    'Audi': {
        'models': ['A3', 'A4', 'A6', 'A8', 'Q3', 'Q5', 'Q7'],
        'origins': 'Germany'
    },
    'Tesla': {
        'models': ['Model 3', 'Model Y', 'Model S', 'Model X'],
        'origins': 'USA'
    },
    'Hyundai': {
        'models': ['Elantra', 'Sonata', 'Tucson', 'Santa Fe', 'Kona'],
        'origins': 'South Korea'
    },
    'Kia': {
        'models': ['Rio', 'Forte', 'Sportage', 'Sorento', 'Telluride'],
        'origins': 'South Korea'
    }
}

TRANSMISSIONS = ['Manual', 'Automatic', 'CVT', 'Dual-Clutch']
COLORS = ['White', 'Black', 'Silver', 'Gray', 'Blue', 'Red', 'Green', 'Yellow', 'Orange', 'Brown']

def generate_cars(
        n: int = 100,
        seed: Optional[int] = None,
        currency: str = "USD",
        output_format: str = "dataframe"
) -> Union[pd.DataFrame, List[Dict], str]:
    """Generate deterministic synthetic car dataset."""
    if n < 1:
        raise ValueError("Number of cars (n) must be at least 1")

    valid_formats = ['dataframe', 'dict', 'csv', 'json']
    if output_format not in valid_formats:
        raise ValueError(f"output_format must be one of {valid_formats}")

    fake = Faker()
    if seed is not None:
        Faker.seed(seed)
        random.seed(seed)

    cars = []

    for _ in range(n):
        make = random.choice(list(CAR_DATA.keys()))
        model = random.choice(CAR_DATA[make]['models'])
        origin = CAR_DATA[make]['origins']

        # Deterministic attributes
        year = random.randint(2005, 2025)
        color = random.choice(COLORS)
        transmission = random.choice(TRANSMISSIONS)

        # Determine price range by brand tier
        base_ranges = {
            'Economy': (15000, 35000),
            'Midrange': (30000, 60000),
            'Luxury': (60000, 150000),
            'EV': (40000, 130000)
        }

        if make in ['Toyota', 'Honda', 'Hyundai', 'Kia', 'Ford', 'Chevrolet']:
            price_min, price_max = base_ranges['Economy']
        elif make in ['BMW', 'Mercedes-Benz', 'Audi']:
            price_min, price_max = base_ranges['Luxury']
        elif make == 'Tesla':
            price_min, price_max = base_ranges['EV']
        else:
            price_min, price_max = base_ranges['Midrange']

        # Price influenced by year and transmission
        price = random.randint(price_min, price_max)
        if year > 2020:
            price *= 1.1
        if transmission in ['Manual']:
            price *= 0.9

        price = round(price, -2)  # round to nearest hundred

        car_record = {
            'car_id': fake.uuid4(),
            'make': make,
            'model': model,
            'year': year,
            'color': color,
            'transmission': transmission,
            'origin_country': origin,
            'currency': currency,
            'price': int(price),
            'vin': fake.unique.bothify(text='?#??#####?#??????', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
            'created_at': fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S')
        }

        cars.append(car_record)

    if output_format == 'dict':
        return cars

    df = pd.DataFrame(cars)

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
