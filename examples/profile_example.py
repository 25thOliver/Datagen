"""

This script demonstrates how to use the profile generator to create
synthetic user profiles with Kenya localization.

"""

from datagen import generate_profiles, save_data
import pandas as pd

def main():
    print("-" * 60)
    print("Profile Generator Example")
    print("-" * 60)
    
    # Example 1: Generate 20 profiles with seed for reproducibility
    print("\n1. Generating 10 profiles with seed=42...")
    profiles = generate_profiles(n=20, seed=42, locale="en_KE")
    print(profiles[['full_name', 'email', 'city', 'age']].to_string(index=False))
    
    # Example 2: Generate profiles and get as dictionary
    print("\n2. Generating 20 profiles as dictionary...")
    profiles_dict = generate_profiles(n=20, seed=123, output_format="dict")
    for i, profile in enumerate(profiles_dict[:2], 1):
        print(f"\nProfile {i}:")
        print(f"  Name: {profile['full_name']}")
        print(f"  Email: {profile['email']}")
        print(f"  Location: {profile['city']}, {profile['country']}")
        print(f"  Coordinates: ({profile['latitude']}, {profile['longitude']})")
    
    # Example 3: Generate larger dataset and analyze
    print("\n3. Generating 100 profiles for analysis...")
    large_profiles = generate_profiles(n=100, seed=42)
    
    print(f"\nDataset Statistics:")
    print(f"  Total profiles: {len(large_profiles)}")
    print(f"\nGender distribution:")
    print(large_profiles['gender'].value_counts())
    print(f"\nCity distribution (top 5):")
    print(large_profiles['city'].value_counts().head())
    print(f"\nAge statistics:")
    print(large_profiles['age'].describe())
    
    # Example 4: Save to different formats
    print("\n4. Saving profiles to different formats...")
    save_data(large_profiles, "examples/output/profiles.csv", file_format="csv")
    save_data(large_profiles, "examples/output/profiles.json", file_format="json")
    save_data(large_profiles, "examples/output/profiles.xlsx", file_format="excel")
    print("✓ Saved to CSV, JSON, and Excel formats")
    
    # Example 5: Reproducibility test
    print("\n5. Testing reproducibility...")
    profiles_a = generate_profiles(n=20, seed=999)
    profiles_b = generate_profiles(n=20, seed=999)
    are_equal = profiles_a.equals(profiles_b)
    print(f"  Same seed produces identical output: {are_equal}")
    
    print("\n" + "-" * 60)
    print("Profile generation examples completed successfully!")
    print("-" * 60)

if __name__ == "__main__":
    main()