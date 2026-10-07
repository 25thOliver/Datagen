# Datagen

A Python package for generating localized synthetic tabular data for development, testing, and analytics prototyping.

## Overview

Datagen provides modular data generators for creating synthetic datasets with local context. It was created to solve common data engineering and development needs, such as:

* Prototyping ETL/ELT pipelines with realistic schema shapes
* Generating seed data for database tables
* Mocking tabular data for analytics dashboards and reports
* Creating deterministic, reproducible test datasets for application development

## Key Features

* **Localized Synthetic Data:** Built-in localization support, with a specific focus on Kenyan domain data (mobile phone numbers, geographic coordinates, cities, automotive market data, and KES currency compensation bands).
* **Command-Line Interface (CLI):** Full CLI tool (`datagen`) for generating datasets directly from the terminal.
* **Relational Foreign Key Support:** Generate linked datasets (e.g. employee salary records referencing valid profile IDs) to maintain referential integrity across tables.
* **Deterministic Reproducibility:** Support for random seed parameters across generators to ensure reproducible outputs across test runs.
* **Multiple Output Formats:** Generates data directly as Pandas DataFrames, Python lists of dictionaries, CSV strings, or JSON strings.
* **Export Utility:** Built-in export helper to write datasets to CSV, JSON, Excel, and Parquet formats.
* **Automated CI/CD & Testing:** Automated test suite with `pytest` and continuous integration via GitHub Actions.

## Generated Datasets

Datagen currently includes four specialized generators:

### Profiles (`generate_profiles`)

Generates synthetic user profile data localized to Kenya.

* **Supported Fields:** `profile_id` (UUID), `first_name`, `last_name`, `full_name`, `email`, `username`, `gender`, `date_of_birth`, `age`, `phone`, `street_address`, `city`, `state`, `postal_code`, `country`, `latitude`, `longitude`, `created_at`.
* **Localization Details:** Phone numbers use Kenyan operator prefixes (+254 7xx/1xx format), addresses default to major Kenyan cities, and coordinates fall within Kenya's geographical bounding box.

### Salaries (`generate_salaries`)

Generates synthetic employee compensation records across departments and experience levels.

* **Supported Fields:** `salary_id`, `employee_id`, `job_title`, `department`, `level`, `years_experience`, `base_salary`, `bonus`, `bonus_percentage`, `total_compensation`, `currency`, `effective_date`.
* **Relational Capability:** Supports foreign keys via the optional `employee_ids` parameter, allowing generated salary records to reference valid primary keys from `generate_profiles`.
* **Implementation Note:** Job titles map to 8 standard organizational departments (Engineering, Product, Data, Marketing, Sales, Operations, Finance, HR). Base salaries and bonus percentages are calculated using predefined ranges per seniority level (`Junior` through `C-Level`) in KES or USD, rather than a fitted statistical distribution model.

### Regions (`generate_regions`)

Generates static business region metadata for organizational and reporting mockups.

* **Supported Fields:** `region_id`, `region_name`, `region_code`, `countries`, `country_count`, `primary_timezone`, `all_timezones`, `hq_city`, `hq_country`, `regional_manager`, `manager_email`, `established_date`.
* **Coverage:** Includes predefined global business regions (North America, South America, Europe, Middle East, Africa, Asia Pacific) with headquarters cities and assigned mock managers.

### Cars (`generate_cars`)

Generates synthetic vehicle inventory data focused on common models in the Kenyan automotive market.

* **Supported Fields:** `car_id`, `make`, `model`, `year`, `color`, `transmission_type`, `fuel_type`, `assembled_in`, `dealer_city`, `price_kes`.
* **Implementation Note:** Includes popular makes and models (Toyota Corolla/Probox, Nissan Note, Mazda Demio, Subaru Forester, Isuzu D-Max, etc.) across major dealer cities. Vehicle prices use a baseline value adjusted by a linear annual depreciation heuristic (`3%` reduction per year relative to 2025), rather than an advanced economic pricing model.

## Relational Data & Foreign Keys

Datagen supports generating relational datasets where child tables reference parent table primary keys:

```python
from datagen import generate_profiles, generate_salaries

# 1. Generate parent profiles table
profiles = generate_profiles(n=10, seed=42)
profile_ids = profiles['profile_id'].tolist()

# 2. Generate child salaries table referencing parent profile IDs
salaries = generate_salaries(n=10, employee_ids=profile_ids, seed=42)

# Verify referential integrity
assert set(salaries['employee_id']).issubset(set(profiles['profile_id']))
```

## Reproducible Generation

All generator functions accept an optional `seed` parameter. Passing a seed sets the random state for both Python's standard `random` module and `faker`, producing identical outputs across runs:

```python
from datagen import generate_profiles

# Same seed produces identical DataFrames
df1 = generate_profiles(n=50, seed=42)
df2 = generate_profiles(n=50, seed=42)

assert df1.equals(df2)
```

## Export Formats

Datagen provides a `save_data` helper in `datagen.utils.io` to persist generated datasets to disk. Supported file formats include:

* **CSV** (`.csv`)
* **JSON** (`.json`)
* **Excel** (`.xlsx`)
* **Parquet** (`.parquet`)

```python
from datagen import generate_profiles, save_data

df = generate_profiles(n=100, seed=42)

# Save to CSV
save_data(df, "output/profiles.csv", file_format="csv")

# Save to Parquet
save_data(df, "output/profiles.parquet", file_format="parquet")
```

## Installation

### From PyPI

```bash
pip install sami-datagen
```

### From Source

```bash
git clone https://github.com/25thOliver/Datagen.git
cd Datagen
pip install -e .
```

## Command-Line Interface (CLI)

Datagen includes a command-line interface (`datagen`) for generating datasets directly from your terminal:

```bash
# View CLI help menu
datagen --help

# Generate user profiles
datagen profiles --count 50 --seed 42 --output profiles.csv

# Generate salaries in KES
datagen salaries --count 50 --currency KES --output salaries.json

# Generate global region metadata
datagen regions --output regions.csv

# Generate vehicle inventory
datagen cars --count 25 --output cars.parquet
```

## Usage

Here is a basic Python script demonstrating how to import generators, create datasets, and save them:

```python
from datagen import (
    generate_profiles,
    generate_salaries,
    generate_regions,
    generate_cars,
    save_data
)

# Generate 50 Kenya user profiles
profiles = generate_profiles(n=50, seed=42, locale="en_KE")
profile_ids = profiles['profile_id'].tolist()

# Generate 50 salary records linked to the generated profiles
salaries = generate_salaries(n=50, employee_ids=profile_ids, seed=42, currency="KES")

# Generate global region metadata
regions = generate_regions(seed=42, include_all=True)

# Generate 50 car records for the Kenyan market
cars = generate_cars(n=50, seed=42)

# Save datasets to disk
save_data(profiles, "output/profiles.csv")
save_data(salaries, "output/salaries.json")
save_data(cars, "output/cars.parquet")
```

## Testing & CI/CD

Datagen includes an automated test suite managed by `pytest` and continuous integration via GitHub Actions.

### Running Tests Locally

```bash
pip install -e ".[dev]"
pytest
```

## Docker / Local Development

DataGen includes a `Dockerfile` and `docker-compose.yml` configured as a local development environment.

### Using Docker for Local Development

```bash
# Build and run interactive development container
docker-compose up -d

# Access container terminal
docker-compose exec datagen bash

# Inside container:
pytest
python examples/complete_demo.py
```

## Current Limitations

Key considerations for current usage:

* **In-Memory Processing:** Datasets are generated entirely in memory before export. Large dataset generation is constrained by available RAM.
* **Rule-Based Modeling:** Salary bands use fixed ranges per job level, and car prices use a basic linear depreciation heuristic rather than fitted statistical distributions or economic market models.

## Future Roadmap

Planned enhancements for future releases:

* **Batch & Streaming Generation:** Implement chunked generator streaming to write multi-million row datasets directly to disk without memory constraints.
* **Statistical Distribution Models:** Replace fixed salary/price ranges with log-normal or beta probability distributions for enhanced statistical realism.
* **Performance Benchmarking:** Publish benchmark suites measuring generation throughput (records/sec) and memory footprints across dataset sizes.
