"""

This script demonstrates how to use the car generator to create
synthetic vehicle data for the Kenyan automotive market.

"""

from datagen import generate_cars, save_data
import pandas as pd

def main():
    print("-" * 60)
    print("Car Generator Example")
    print("-" * 60)
    
    # Example 1: Generate 20 cars
    print("\n1. Generating 20 cars...")
    cars = generate_cars(n=20, seed=42)
    print(cars[['make', 'model', 'year', 'color', 'price_kes']].to_string(index=False))
    
    # Example 2: View detailed car information
    print("\n2. Detailed information for first 20 cars:")
    for idx, car in cars.head(20).iterrows():
        print(f"\nCar {idx + 1}:")
        print(f"  {car['year']} {car['make']} {car['model']}")
        print(f"  Color: {car['color']}")
        print(f"  Transmission: {car['transmission_type']}")
        print(f"  Fuel Type: {car['fuel_type']}")
        print(f"  Price: KES {car['price_kes']:,.0f}")
        print(f"  Dealer: {car['dealer_city']}")
    
    # Example 3: Generate larger dataset for analysis
    print("\n3. Generating 100 cars for analysis...")
    large_cars = generate_cars(n=100, seed=42)
    
    print(f"\nCar Market Statistics:")
    print(f"  Total vehicles: {len(large_cars)}")
    
    # Example 4: Analyze by make
    print(f"\nVehicles by Make:")
    make_counts = large_cars['make'].value_counts()
    print(make_counts.to_string())
    
    print(f"\nAverage Price by Make (KES):")
    price_by_make = large_cars.groupby('make')['price_kes'].mean().sort_values(ascending=False)
    for make, price in price_by_make.items():
        print(f"  {make}: KES {price:,.0f}")
    
    # Example 5: Analyze by year
    print(f"\nVehicles by Year Range:")
    large_cars['year_range'] = pd.cut(large_cars['year'], bins=[2007, 2012, 2017, 2022, 2026], 
                                       labels=['2008-2012', '2013-2017', '2018-2022', '2023-2025'])
    print(large_cars['year_range'].value_counts().sort_index().to_string())
    
    # Example 6: Transmission and fuel type analysis
    print(f"\nTransmission Type Distribution:")
    print(large_cars['transmission_type'].value_counts().to_string())
    
    print(f"\nFuel Type Distribution:")
    print(large_cars['fuel_type'].value_counts().to_string())
    
    # Example 7: Price statistics
    print(f"\nPrice Statistics (KES):")
    print(f"  Minimum: KES {large_cars['price_kes'].min():,.0f}")
    print(f"  Maximum: KES {large_cars['price_kes'].max():,.0f}")
    print(f"  Average: KES {large_cars['price_kes'].mean():,.0f}")
    print(f"  Median: KES {large_cars['price_kes'].median():,.0f}")
    
    # Example 8: Dealer city distribution
    print(f"\nInventory by Dealer City:")
    print(large_cars['dealer_city'].value_counts().to_string())
    
    # Example 9: Color preferences
    print(f"\nMost Popular Colors:")
    print(large_cars['color'].value_counts().head().to_string())
    
    # Example 10: Get cars as dictionary
    print("\n10. Getting cars as dictionary format...")
    cars_dict = generate_cars(n=20, seed=42, output_format="dict")
    print(f"  Retrieved {len(cars_dict)} cars as list of dictionaries")
    print(f"  Sample car: {cars_dict[0]['year']} {cars_dict[0]['make']} {cars_dict[0]['model']}")
    
    # Example 11: Save to file
    print("\n11. Saving car data...")
    save_data(large_cars, "examples/output/cars.csv", file_format="csv")
    save_data(large_cars, "examples/output/cars.json", file_format="json")
    print("✓ Saved to CSV and JSON formats")
    
    # Example 12: Reproducibility test
    print("\n12. Testing reproducibility...")
    cars_a = generate_cars(n=20, seed=777)
    cars_b = generate_cars(n=20, seed=777)
    are_equal = cars_a.equals(cars_b)
    print(f"  Same seed produces identical output: {are_equal}")
    
    print("\n" + "-" * 60)
    print("Car generation examples completed successfully!")
    print("-" * 60)

if __name__ == "__main__":
    main()