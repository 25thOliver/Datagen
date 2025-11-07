"""

This script demonstrates how to use the region generator to create
global region data with countries, timezones, and management information.

"""

from datagen import generate_regions, save_data
import pandas as pd

def main():
    print("-" * 60)
    print("Region Generator Example")
    print("-" * 60)
    
    # Example 1: Generate all predefined regions
    print("\n1. Generating all global regions...")
    regions = generate_regions(seed=42, include_all=True)
    print(regions[['region_name', 'region_code', 'country_count', 'hq_city']].to_string(index=False))
    
    # Example 2: View detailed region information
    print("\n2. Detailed information for each region:")
    for idx, region in regions.iterrows():
        print(f"\n{region['region_name']} ({region['region_code']}):")
        print(f"  Headquarters: {region['hq_city']}, {region['hq_country']}")
        print(f"  Countries: {region['country_count']}")
        print(f"  Primary Timezone: {region['primary_timezone']}")
        print(f"  Regional Manager: {region['regional_manager']}")
        print(f"  Manager Email: {region['manager_email']}")
    
    # Example 3: Generate random subset of regions
    print("\n3. Generating random subset (5 regions)...")
    random_regions = generate_regions(n=5, seed=123, include_all=False)
    print(random_regions[['region_name', 'hq_city', 'regional_manager']].to_string(index=False))
    
    # Example 4: Analyze region data
    print("\n4. Region Analysis:")
    print(f"  Total regions: {len(regions)}")
    print(f"  Total countries covered: {regions['country_count'].sum()}")
    print(f"  Average countries per region: {regions['country_count'].mean():.1f}")
    print(f"\nCountries by Region:")
    print(regions[['region_name', 'country_count']].sort_values('country_count', ascending=False).to_string(index=False))
    
    # Example 5: Timezone information
    print("\n5. Timezone Information:")
    for idx, region in regions.iterrows():
        timezones = region['all_timezones'].split(', ')
        print(f"  {region['region_name']}: {len(timezones)} timezones")
    
    # Example 6: Get regions as dictionary
    print("\n6. Getting regions as dictionary format...")
    regions_dict = generate_regions(seed=42, output_format="dict")
    print(f"  Retrieved {len(regions_dict)} regions as list of dictionaries")
    print(f"  Sample region keys: {list(regions_dict[0].keys())}")
    
    # Example 7: Save to file
    print("\n7. Saving region data...")
    save_data(regions, "examples/output/regions.csv", file_format="csv")
    save_data(regions, "examples/output/regions.json", file_format="json")
    print("✓ Saved to CSV and JSON formats")
    
    # Example 8: Reproducibility test
    print("\n8. Testing reproducibility...")
    regions_a = generate_regions(seed=555)
    regions_b = generate_regions(seed=555)
    are_equal = regions_a.equals(regions_b)
    print(f"  Same seed produces identical output: {are_equal}")
    
    print("\n" + "-" * 60)
    print("Region generation examples completed successfully!")
    print("-" * 60)

if __name__ == "__main__":
    main()