"""
This scripts demonstrates how to use the salary generator to create
synthetic compensation data across departments and experience levels.
"""

from datagen import generate_salaries, save_data
import pandas as pd

def main():
    print("-" * 60)
    print("Salary Generator Example")
    print("-" * 60)

    # Example 1: Generate 20 salary records in KES
    print("\n1. Generating 20 salary records (KES)...")
    salaries = generate_salaries(n=20, seed=42, currency="KES")
    print(salaries[['job_title', 'level', 'department', 'total_compensation']].to_string(index=False))

    # Example 2: Generate salaries in USD
    print("\n2. Generate 10 salary records (USD)...")
    salaries_usd = generate_salaries(n=10, seed=42, currency="USD")
    print(salaries[['job_title', 'base_salary', 'bonus', 'total_compensation']].to_string(index=False))

    # Example 3: Analyze salary distribution by department
    print("\n3. Generating 100 salaries for analysis...")
    large_salaries = generate_salaries(n=100, seed=42, currency="KES")
    
    print(f"\nSalary Statistics by Department (KES):")
    dept_stats = large_salaries.groupby('department')['total_compensation'].agg(['mean', 'min', 'max', 'count'])
    dept_stats['mean'] = dept_stats['mean'].round(0)
    print(dept_stats.to_string())
    
    # Example 4: Analyze by experience level
    print(f"\nSalary Statistics by Level (KES):")
    level_stats = large_salaries.groupby('level')['base_salary'].agg(['mean', 'min', 'max'])
    level_stats = level_stats.sort_values('mean', ascending=False)
    level_stats['mean'] = level_stats['mean'].round(0)
    print(level_stats.to_string())
    
    # Example 5: Bonus analysis
    print(f"\nBonus Analysis:")
    print(f"  Average bonus percentage: {large_salaries['bonus_percentage'].mean():.2f}%")
    print(f"  Highest bonus percentage: {large_salaries['bonus_percentage'].max():.2f}%")
    print(f"\nBonus by Level:")
    bonus_by_level = large_salaries.groupby('level')['bonus_percentage'].mean().sort_values(ascending=False)
    print(bonus_by_level.to_string())
    
    # Example 6: Years of experience analysis
    print(f"\nExperience Distribution:")
    print(large_salaries.groupby('level')['years_experience'].agg(['mean', 'min', 'max']).to_string())
    
    # Example 7: Save to file
    print("\n7. Saving salary data...")
    save_data(large_salaries, "examples/output/salaries.csv", file_format="csv")
    save_data(large_salaries, "examples/output/salaries.json", file_format="json")
    print("Saved to CSV and JSON formats")
    
    print("\n" + "-" * 60)
    print("Salary generation examples completed successfully!")
    print("-" * 60)

if __name__ == "__main__":
    main()