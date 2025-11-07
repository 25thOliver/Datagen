"""
DataGen Complete Demo
=====================

This script demonstrates all four generators in the datagen library
and shows how they can be used together for comprehensive synthetic
data generation.

"""

from datagen import (
    generate_profiles,
    generate_salaries,
    generate_regions,
    generate_cars,
    save_data
)
import pandas as pd
from datetime import datetime

def print_section(title):
    """Print a formatted section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def main():
    print_section("DataGen Library - Complete Demonstration")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Set seed for reproducibility across all generators
    SEED = 42
    
    # ========================================================================
    # 1. PROFILE GENERATION
    # ========================================================================
    print_section("1. Profile Generation")
    print("Generating 50 user profiles with Kenya localization...")
    
    profiles = generate_profiles(n=50, seed=SEED, locale="en_KE")
    
    print(f"\n✓ Generated {len(profiles)} profiles")
    print(f"  Columns: {', '.join(profiles.columns)}")
    print(f"\nSample profiles:")
    print(profiles[['full_name', 'email', 'city', 'age', 'gender']].head(5).to_string(index=False))
    
    print(f"\nProfile Statistics:")
    print(f"  Age range: {profiles['age'].min()} - {profiles['age'].max()}")
    print(f"  Gender distribution: {profiles['gender'].value_counts().to_dict()}")
    print(f"  Cities: {profiles['city'].nunique()} unique cities")
    
    # ========================================================================
    # 2. SALARY GENERATION
    # ========================================================================
    print_section("2. Salary Generation")
    print("Generating 50 salary records in KES...")
    
    salaries = generate_salaries(n=50, seed=SEED, currency="KES")
    
    print(f"\n✓ Generated {len(salaries)} salary records")
    print(f"  Columns: {', '.join(salaries.columns)}")
    print(f"\nSample salaries:")
    print(salaries[['job_title', 'department', 'level', 'total_compensation']].head(5).to_string(index=False))
    
    print(f"\nSalary Statistics:")
    print(f"  Average compensation: KES {salaries['total_compensation'].mean():,.0f}")
    print(f"  Salary range: KES {salaries['total_compensation'].min():,.0f} - KES {salaries['total_compensation'].max():,.0f}")
    print(f"  Departments: {salaries['department'].nunique()}")
    print(f"  Experience levels: {salaries['level'].nunique()}")
    
    # ========================================================================
    # 3. REGION GENERATION
    # ========================================================================
    print_section("3. Region Generation")
    print("Generating all global regions...")
    
    regions = generate_regions(seed=SEED, include_all=True)
    
    print(f"\n✓ Generated {len(regions)} regions")
    print(f"  Columns: {', '.join(regions.columns)}")
    print(f"\nAll regions:")
    print(regions[['region_name', 'region_code', 'country_count', 'hq_city']].to_string(index=False))
    
    print(f"\nRegion Statistics:")
    print(f"  Total countries: {regions['country_count'].sum()}")
    print(f"  Average countries per region: {regions['country_count'].mean():.1f}")
    
    # ========================================================================
    # 4. CAR GENERATION
    # ========================================================================
    print_section("4. Car Generation")
    print("Generating 50 vehicle records for Kenyan market...")
    
    cars = generate_cars(n=50, seed=SEED)
    
    print(f"\n✓ Generated {len(cars)} car records")
    print(f"  Columns: {', '.join(cars.columns)}")
    print(f"\nSample cars:")
    print(cars[['make', 'model', 'year', 'price_kes', 'dealer_city']].head(5).to_string(index=False))
    
    print(f"\nCar Statistics:")
    print(f"  Makes: {cars['make'].nunique()}")
    print(f"  Average price: KES {cars['price_kes'].mean():,.0f}")
    print(f"  Year range: {cars['year'].min()} - {cars['year'].max()}")
    print(f"  Dealer cities: {cars['dealer_city'].nunique()}")
    
    # ========================================================================
    # 5. COMBINED ANALYSIS
    # ========================================================================
    print_section("5. Combined Dataset Analysis")
    
    print("\nDataset Summary:")
    print(f"  Profiles: {len(profiles):,} records")
    print(f"  Salaries: {len(salaries):,} records")
    print(f"  Regions: {len(regions):,} records")
    print(f"  Cars: {len(cars):,} records")
    print(f"  Total records: {len(profiles) + len(salaries) + len(regions) + len(cars):,}")
    
    # ========================================================================
    # 6. SAVE ALL DATA
    # ========================================================================
    print_section("6. Saving All Datasets")
    
    output_dir = "examples/output"
    
    print(f"\nSaving to '{output_dir}/' directory...")
    
    # Save profiles
    save_data(profiles, f"{output_dir}/demo_profiles.csv", file_format="csv")
    save_data(profiles, f"{output_dir}/demo_profiles.json", file_format="json")
    print("  ✓ Profiles saved (CSV, JSON)")
    
    # Save salaries
    save_data(salaries, f"{output_dir}/demo_salaries.csv", file_format="csv")
    save_data(salaries, f"{output_dir}/demo_salaries.json", file_format="json")
    print("  ✓ Salaries saved (CSV, JSON)")
    
    # Save regions
    save_data(regions, f"{output_dir}/demo_regions.csv", file_format="csv")
    save_data(regions, f"{output_dir}/demo_regions.json", file_format="json")
    print("  ✓ Regions saved (CSV, JSON)")
    
    # Save cars
    save_data(cars, f"{output_dir}/demo_cars.csv", file_format="csv")
    save_data(cars, f"{output_dir}/demo_cars.json", file_format="json")
    print("  ✓ Cars saved (CSV, JSON)")
    
    # ========================================================================
    # 7. REPRODUCIBILITY TEST
    # ========================================================================
    print_section("7. Reproducibility Verification")
    
    print("\nTesting reproducibility with same seed...")
    
    profiles_test = generate_profiles(n=10, seed=SEED)
    salaries_test = generate_salaries(n=10, seed=SEED)
    regions_test = generate_regions(seed=SEED)
    cars_test = generate_cars(n=10, seed=SEED)
    
    print(f"  ✓ Profiles reproducible: {profiles.head(10).equals(profiles_test)}")
    print(f"  ✓ Salaries reproducible: {salaries.head(10).equals(salaries_test)}")
    print(f"  ✓ Regions reproducible: {regions.equals(regions_test)}")
    print(f"  ✓ Cars reproducible: {cars.head(10).equals(cars_test)}")
    
    # ========================================================================
    # COMPLETION
    # ========================================================================
    print_section("Demo Completed Successfully!")
    
    print("\nKey Features Demonstrated:")
    print("  ✓ All four generators (profiles, salaries, regions, cars)")
    print("  ✓ Reproducible generation with seed control")
    print("  ✓ Multiple output formats (DataFrame, CSV, JSON)")
    print("  ✓ Kenya-specific localization")
    print("  ✓ Comprehensive data analysis")
    print("  ✓ File saving functionality")
    
    print(f"\nAll output files saved to: {output_dir}/")
    print("\nThank you for using DataGen!")
    print("=" * 70)

if __name__ == "__main__":
    main()