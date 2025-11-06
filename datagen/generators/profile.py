from typing import Optional, Union, List, Dict
import pandas as pd
from faker import Faker
import random
from datagen.utils.io import save_data  # DRY utility for saving

def generate_profiles(
        n: int = 100,
        seed: Optional[int] = None,
        locale: str = "en_KE",
        output_format: str = "dataframe"
) -> Union[pd.DataFrame, List[Dict], str]:
    """
    Generate synthetic user profile data localized to Kenya.

    Each profile includes realistic Kenyan names, addresses, coordinates, and contact details.

    Args:
        n (int): Number of profiles to generate.
        seed (Optional[int]): Random seed for reproducibility.
        locale (str): Locale for Faker (default 'en_KE').
        output_format (str): Output format ('dataframe', 'dict', 'csv', 'json').

    Returns:
        Union[pd.DataFrame, List[Dict], str]: Generated data in the requested format.
    """

    # Validate inputs
    if n < 1:
        raise ValueError("Number of profiles (n) must be at least 1.")

    valid_formats = ['dataframe', 'dict', 'csv', 'json']
    if output_format not in valid_formats:
        raise ValueError(f"output_format must be one of {valid_formats}")

    # Initialize Faker for Kenya with reproducibility
    fake = Faker(locale)
    if seed is not None:
        Faker.seed(seed)
        random.seed(seed)

    # Kenyan city list for realism
    kenyan_cities = [
        "Nairobi", "Mombasa", "Kisumu", "Nakuru", "Eldoret",
        "Thika", "Machakos", "Nyeri", "Garissa", "Naivasha"
    ]

    profiles = []
    genders = ['Male', 'Female', 'Non-binary']

    for _ in range(n):
        gender = random.choice(genders)

        # Gendered first names
        if gender == 'Male':
            first_name = fake.first_name_male()
        elif gender == 'Female':
            first_name = fake.first_name_female()
        else:
            first_name = fake.first_name()

        last_name = fake.last_name()
        full_name = f"{first_name} {last_name}"

        # Generate contact info
        username = f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 999)}"
        email = f"{username}@{fake.free_email_domain()}"

        # Birth date and age
        dob = fake.date_of_birth(minimum_age=18, maximum_age=80)
        from datetime import date
        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

        # Location and address (Kenya-scoped)
        city = random.choice(kenyan_cities)
        state = "Kenya"
        postal_code = fake.postcode()
        street_address = fake.street_address()
        country = "Kenya"

        # Geo realism — bounding box for Kenya
        latitude = round(random.uniform(-4.7, 5.0), 6)
        longitude = round(random.uniform(34.0, 41.9), 6)

        # Compile profile record
        profile = {
            'profile_id': fake.uuid4(),
            'first_name': first_name,
            'last_name': last_name,
            'full_name': full_name,
            'email': email,
            'username': username,
            'gender': gender,
            'date_of_birth': dob.strftime('%Y-%m-%d'),
            'age': age,
            'phone': fake.phone_number(),
            'street_address': street_address,
            'city': city,
            'state': state,
            'postal_code': postal_code,
            'country': country,
            'latitude': latitude,
            'longitude': longitude,
            'created_at': fake.date_time_between(start_date='-2y', end_date='now').strftime('%Y-%m-%d %H:%M:%S')
        }

        profiles.append(profile)

    # Convert to desired output format
    if output_format == 'dict':
        return profiles

    df = pd.DataFrame(profiles)

    if output_format == 'dataframe':
        return df
    elif output_format == 'csv':
        return df.to_csv(index=False)
    elif output_format == 'json':
        return df.to_json(orient='records', indent=2)


def save_profiles(
        profiles: Union[pd.DataFrame, List[Dict]],
        filename: str,
        file_format: Optional[str] = None
) -> None:
    """
    Save generated profiles using the shared I/O utility.
    """
    save_data(profiles, filename, file_format)


if __name__ == "__main__":
    print("Generating 10 Kenya-localized sample profiles...")
    profiles = generate_profiles(n=10, seed=42)
    print(profiles.head())
    print(f"\nGenerated {len(profiles)} profiles")
    print(f"Columns: {list(profiles.columns)}")
