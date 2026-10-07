import argparse
import sys
from datagen import (
    generate_profiles,
    generate_salaries,
    generate_regions,
    generate_cars,
    save_data
)

def main():
    parser = argparse.ArgumentParser(
        prog="datagen",
        description="DataGen CLI — Synthetic Data Generation Tool"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available generator commands")
    
    # Common arguments helper
    def add_common_args(subparser):
        subparser.add_argument("-n", "--count", type=int, default=100, help="Number of records to generate (default: 100)")
        subparser.add_argument("-s", "--seed", type=int, default=None, help="Random seed for reproducibility")
        subparser.add_argument("-o", "--output", type=str, default=None, help="Output file path (e.g. output.csv)")
        subparser.add_argument("-f", "--format", type=str, choices=["dataframe", "dict", "csv", "json"], default="dataframe", help="Output format")

    # 1. Profiles command
    parser_profiles = subparsers.add_parser("profiles", help="Generate user profiles localized to Kenya")
    add_common_args(parser_profiles)
    parser_profiles.add_argument("-l", "--locale", type=str, default="en_KE", help="Faker locale (default: en_KE)")

    # 2. Salaries command
    parser_salaries = subparsers.add_parser("salaries", help="Generate salary records")
    add_common_args(parser_salaries)
    parser_salaries.add_argument("-c", "--currency", type=str, choices=["KES", "USD"], default="KES", help="Currency code (KES or USD)")

    # 3. Regions command
    parser_regions = subparsers.add_parser("regions", help="Generate global region metadata")
    add_common_args(parser_regions)

    # 4. Cars command
    parser_cars = subparsers.add_parser("cars", help="Generate vehicle data for Kenyan market")
    add_common_args(parser_cars)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Dispatch to appropriate generator
    if args.command == "profiles":
        data = generate_profiles(n=args.count, seed=args.seed, locale=args.locale, output_format=args.format)
    elif args.command == "salaries":
        data = generate_salaries(n=args.count, seed=args.seed, currency=args.currency, output_format=args.format)
    elif args.command == "regions":
        data = generate_regions(n=args.count, seed=args.seed, include_all=True, output_format=args.format)
    elif args.command == "cars":
        data = generate_cars(n=args.count, seed=args.seed, output_format=args.format)

    # Save or print output
    if args.output:
        save_data(data, args.output)
    else:
        print(data)

if __name__ == "__main__":
    main()