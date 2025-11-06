from typing import Optional, Union, List, Dict
import pandas as pd
from faker import Faker
import random
from datagen.utils.io import save_data

def generate_profiles(
        n: int = 100,
        seed: Optional[int] = None,
        locale: str = "en_KE",
        output_format: str = "dataframe"
) -> Union[pd.DataFrame, List[Dict], str]:
    """
    Generate synthetic user profile data deterministically.

    Args:
        n (int): Number of profiles to generate. Default = 100.
        seed (Optional[int]): Random seed for reproducibility.
        locale (str): Faker locale for regional data variation. Default = 'en_KE'.
        output_format (str): Format of returned data: 'dataframe', 'dict', 'csv', 'json'.

    Returns:
        Union[pd.DataFrame, List[Dict], str]: Generated data in the specified format.
    """
    
    # Validate inputs
    if n < 1:
        raise ValueError("Number of profiles (n) must be atleast 1")
    
    valid_formats = ['dataframe', 'dict', 'csv', 'json']
    if output_format not in valid_formats:
        raise ValueError(f"output_format must be one of {valid_formats}")
    
    # Initialize Faker with seed for reproducibility
    fake = Faker(locale)
    if seed is not None:
        Faker.seed(seed)
        random.seed(seed)

    genders = ['Male', 'Female', 'Non-binary']
    profiles = []

    for _ in range(n):
        gender = random.choice(genders)

        # Generate name based on gender
        if gender == 'Male':
            first_name = fake.first_name_male()
        elif gender == 'Female':
            first_name = fake.first_name_female()
        else:
            first_name = fake.first_name()

        last_name = fake.last_name()
        full_name = f"{first_name} {last_name}"

        # contact info
        username = f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 999)}"
        email = f"{username}@{fake.free_email_domain()}"

        # date of birth
        dob = fake.date_of_birth(minimum_age=18, maximum_age=80)
        from datetime import date
        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

        # Generate address
        address = fake.address().replace('\n', ', ')

        # Create profile dictionary
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
            'street_address': fake.street_address(),
            'city': fake.city(),
            'state': fake.state(),
            'postal_code': fake.postcode(),
            'country': fake.country(),
            'latitude': float(fake.latitude()),
            'longitude': float(fake.longitude()),
            'created_at': fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S')
        }

        profiles.append(profile)

    # Return in the requested format
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
) -> str:
    
    """
    Save generated profiles using the shared save_data utility.

    Args:
        profiles (Union[pd.DataFrame, List[Dict]]): Generated profile data.
        filename (str): Destination filename (e.g., './output/profiles.csv').
        file_format (Optional[str]): Format override. Inferred if None.

    Returns:
        str: Absolute path to saved file.
    """
    return save_data(profiles, filename, file_format)
    
   

if __name__ == "__main__":
    print("Generating 10 sample profiles...")
    profiles = generate_profiles(n=10, seed=42)
    print(profiles)
    print(f"\nGenerated {len(profiles)} profiles")
    print(f"Columns: {list(profiles.columns)}")
    
    save_profiles(profiles, "./output/sample_profiles.csv")