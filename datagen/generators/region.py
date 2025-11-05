from typing import Optional, Union, List, Dict
import pandas as pd
from faker import Faker
import random

# Global regions with their countries
REGIONS = {
    'North America': {
        'code': 'NA',
        'countries': ['United States', 'Canada', 'Mexico'],
        'timezones': ['America/New_York', 'America/Chicago', 'America/Denver', 
                     'America/Los_Angeles', 'America/Toronto', 'America/Mexico_City'],
        'hq_cities': ['New York', 'Toronto', 'San Francisco', 'Chicago', 'Mexico City']
    },
    'South America': {
        'code': 'SA',
        'countries': ['Brazil', 'Argentina', 'Chile', 'Colombia', 'Peru'],
        'timezones': ['America/Sao_Paulo', 'America/Argentina/Buenos_Aires', 
                     'America/Santiago', 'America/Bogota', 'America/Lima'],
        'hq_cities': ['São Paulo', 'Buenos Aires', 'Santiago', 'Bogotá', 'Lima']
    },
    'Europe': {
        'code': 'EU',
        'countries': ['United Kingdom', 'Germany', 'France', 'Spain', 'Italy', 
                     'Netherlands', 'Poland', 'Sweden', 'Switzerland'],
        'timezones': ['Europe/London', 'Europe/Berlin', 'Europe/Paris', 
                     'Europe/Madrid', 'Europe/Rome', 'Europe/Amsterdam'],
        'hq_cities': ['London', 'Berlin', 'Paris', 'Madrid', 'Amsterdam', 'Stockholm']
    },
    'Middle East': {
        'code': 'ME',
        'countries': ['United Arab Emirates', 'Saudi Arabia', 'Israel', 'Turkey', 'Egypt'],
        'timezones': ['Asia/Dubai', 'Asia/Riyadh', 'Asia/Jerusalem', 
                     'Europe/Istanbul', 'Africa/Cairo'],
        'hq_cities': ['Dubai', 'Riyadh', 'Tel Aviv', 'Istanbul', 'Cairo']
    },
    'Africa': {
        'code': 'AF',
        'countries': ['South Africa', 'Nigeria', 'Kenya', 'Egypt', 'Morocco'],
        'timezones': ['Africa/Johannesburg', 'Africa/Lagos', 'Africa/Nairobi', 
                     'Africa/Cairo', 'Africa/Casablanca'],
        'hq_cities': ['Johannesburg', 'Lagos', 'Nairobi', 'Cairo', 'Casablanca']
    },
    'Asia Pacific': {
        'code': 'APAC',
        'countries': ['China', 'Japan', 'India', 'Australia', 'Singapore', 
                     'South Korea', 'Indonesia', 'Thailand', 'Vietnam'],
        'timezones': ['Asia/Shanghai', 'Asia/Tokyo', 'Asia/Kolkata', 
                     'Australia/Sydney', 'Asia/Singapore', 'Asia/Seoul'],
        'hq_cities': ['Shanghai', 'Tokyo', 'Mumbai', 'Sydney', 'Singapore', 'Seoul']
    }
}

def generate_regions(
        n: Optional[int] = None,
        seed: Optional[int] = None,
        include_all: bool = True,
        output_format: str = "dataframe"
) -> Union[pd.DataFrame, List[Dict], str]:
    
    valid_formats = ['dataframe', 'dict', 'csv', 'json']
    if output_format not in valid_formats:
        raise ValueError(f"output_format must be one of {valid_formats}")
    
    # Initialize Faker with seed reproducibility
    fake = Faker()
    if seed is not None:
        Faker.seed(seed)
        random.seed(seed)

    # Determine which regions to generate
    if include_all:
        region_names = list(REGIONS.keys())
    else:
        if n is None:
            n = 3
        region_names = random.sample(list(REGIONS.keys()), min(n, len(REGIONS)))
    
    regions_data = []

    for region_name in region_names:
        region_info = REGIONS[region_name]

        # Select headquaters city and country
        hq_city = random.choice(region_info['hq_cities'])

        # Map city to country
        city_to_country = {
            'New York': 'United States', 'Toronto': 'Canada', 'San Francisco': 'United States',
            'Chicago': 'United States', 'Mexico City': 'Mexico',
            'São Paulo': 'Brazil', 'Buenos Aires': 'Argentina', 'Santiago': 'Chile',
            'Bogotá': 'Colombia', 'Lima': 'Peru',
            'London': 'United Kingdom', 'Berlin': 'Germany', 'Paris': 'France',
            'Madrid': 'Spain', 'Amsterdam': 'Netherlands', 'Stockholm': 'Sweden',
            'Dubai': 'United Arab Emirates', 'Riyadh': 'Saudi Arabia', 'Tel Aviv': 'Israel',
            'Istanbul': 'Turkey', 'Cairo': 'Egypt',
            'Johannesburg': 'South Africa', 'Lagos': 'Nigeria', 'Nairobi': 'Kenya',
            'Casablanca': 'Morocco',
            'Shanghai': 'China', 'Tokyo': 'Japan', 'Mumbai': 'India',
            'Sydney': 'Australia', 'Singapore': 'Singapore', 'Seoul': 'South Korea'
        }
        hq_country = city_to_country.get(hq_city, region_info['countries'][0])

        # Generate manager details
        manager_name = fake.name()
        manager_email = f"{manager_name.lower().replace(' ', '.')}@company.com"

        # Create region record
        region_record = {
            'region_id': fake.uuid4(),
            'region_name': region_name,
            'region_code': region_info['code'],
            'countries': ', '.join(region_info['countries']),
            'country_count': len(region_info['countries']),
            'primary_timezone': region_info['timezones'][0],
            'all_timezones': ', '.join(region_info['timezones']),
            'hq_city': hq_city,
            'hq_country': hq_country,
            'regional_manager': manager_name,
            'manager_email': manager_email,
            'established_date': fake.date_between(start_date='-10y', end_date='-1y').strftime('%Y-%m-%d')
        }

        regions_data.append(region_record)

    # Convert to requested format
    if output_format == 'dict':
        return regions_data
    
    df = pd.DataFrame(regions_data)
    
    if output_format == 'dataframe':
        return df
    elif output_format == 'csv':
        return df.to_csv(index=False)
    elif output_format == 'json':
        return df.to_json(orient='records', indent=2)


def save_regions(
        regions: Union[pd.DataFrame, List[Dict]],
        filename: str,
        file_format: Optional[str] = None
) -> None:
    
    # Convert to DataFrame if needed
    if isinstance(regions, list):
        df = pd.DataFrame(regions)
    else:
        df = regions
    
    # Infer format from filename if not specified
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
    
    # Save to file
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
    
    print(f"✓ Saved {len(df)} region records to {filename}")

if __name__ == "__main__":
    # Example usage
    print("Generating all global regions...")
    regions = generate_regions(seed=42)
    print(regions)
    print(f"\nGenerated {len(regions)} regions")
    print(f"Columns: {list(regions.columns)}")
    print(f"\nRegion summary:")
    print(regions[['region_name', 'region_code', 'country_count', 'hq_city']].to_string(index=False))
