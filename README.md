# Datagen

A Python package for generating localized synthetic tabular data for development, testing, and analytics prototyping.

## Overview

Datagen provides modular data generators for creating synthetic datasets with local context. It was created to solve common data engineering and development needs, such as:

* Prototyping ETL/ELT pipelines with realistic schema shapes
* Generating seed data for database tables
* Mocking tabular data for analytics dashboards and reports
* Creating deterministic, reproducible test datasets for application development

## Current Features

* **Localized Synthetic Data:** Built-in localization support, with a specific focus on Kenyan domain data (mobile phone numbers, geographic coordinates, cities, automotive market data, and KES currency compensation bands).
* **Deterministic Reproducibility:** Support for random seed parameters across generators to ensure reproducible outputs across test runs.
* **Multiple Output Formats:** Generates data directly as Pandas DataFrames, Python lists of dictionaries, CSV strings, or JSON strings.
* **Export Utility:** Built-in export helper to write datasets to CSV, JSON, Excel, and Parquet formats.

## Generated Datasets

Datagen currently includes four specialized generators:

### Profiles (`generate_profiles`)

Generates synthetic user profile data localized to Kenya.

* **Supported Fields:** `profile_id` (UUID), `first_name`, `last_name`, `full_name`, `email`, `username`, `gender`, `date_of_birth`, `age`, `phone`, `street_address`, `city`, `state`, `postal_code`, `country`, `latitude`, `longitude`, `created_at`.
* **Localization Details:** Phone numbers use Kenyan operator prefixes (+254 7xx/1xx format), addresses default to major Kenyan cities, and coordinates fall within Kenya's geographical bounding box.

### Salaries (`generate_salaries`)

Generates synthetic employee compensation records across departments and experience levels.

* **Supported Fields:** `salary_id`, `employee_id`, `job_title`, `department`, `level`, `years_experience`, `base_salary`, `bonus`, `bonus_percentage`, `total_compensation`, `currency`, `effective_date`.
* **Implementation Note:** Job titles map to 8 standard organizational departments (Engineering, Product, Data, Marketing, Sales, Operations, Finance, HR). Base salaries and bonus percentages are calculated using predefined ranges per seniority level (`Junior` through `C-Level`) in KES or USD, rather than a fitted statistical distribution model.

### Regions (`generate_regions`)

Generates static business region metadata for organizational and reporting mockups.

* **Supported Fields:** `region_id`, `region_name`, `region_code`, `countries`, `country_count`, `primary_timezone`, `all_timezones`, `hq_city`, `hq_country`, `regional_manager`, `manager_email`, `established_date`.
* **Coverage:** Includes predefined global business regions (North America, South America, Europe, Middle East, Africa, Asia Pacific) with headquarters cities and assigned mock managers.

### Cars (`generate_cars`)

Generates synthetic vehicle inventory data focused on common models in the Kenyan automotive market.

* **Supported Fields:** `car_id`, `make`, `model`, `year`, `color`, `transmission_type`, `fuel_type`, `assembled_in`, `dealer_city`, `price_kes`.
* **Implementation Note:** Includes popular makes and models (Toyota Corolla/Probox, Nissan Note, Mazda Demio, Subaru Forester, Isuzu D-Max, etc.) across major dealer cities. Vehicle prices use a baseline value adjusted by a linear annual depreciation heuristic (`3%` reduction per year relative to 2025), rather than an advanced economic pricing model.

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

*Note: The project packaging currently has version metadata differences across files (`0.1.1` in `pyproject.toml` vs `0.1.0` in `setup.py`).*

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
print(profiles.head())

# Generate 50 salary records in KES
salaries = generate_salaries(n=50, seed=42, currency="KES")
print(salaries.head())

# Generate global region metadata
regions = generate_regions(seed=42, include_all=True)
print(regions.head())

# Generate 50 car records for the Kenyan market
cars = generate_cars(n=50, seed=42)
print(cars.head())

# Save datasets to disk
save_data(profiles, "output/profiles.csv")
save_data(salaries, "output/salaries.json")
save_data(cars, "output/cars.parquet")
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
python examples/complete_demo.py
```

*Note: Docker in this project provides an isolated container environment for development. It is not currently configured as a production service or background worker system.*

## Current Limitations

This project is in early-stage development. Key limitations of the current codebase include:

* **CLI Unavailable:** A command-line entry point is registered in packaging config, but `datagen/cli.py` is not yet implemented. CLI commands (`datagen ...`) do not work currently.
* **No Automated Test Suite:** Unit tests and automated test execution (`pytest`) are not yet implemented.
* **No CI/CD Pipeline:** GitHub Actions automated build/test workflows are not yet configured.
* **No Relational Integrity / Foreign Keys:** Generators create isolated datasets. Primary keys (such as `profile_id` and `employee_id`) are independent UUIDs and do not maintain cross-table relationships.
* **In-Memory Processing:** Datasets are generated entirely in memory before export. Large dataset generation is constrained by available RAM.
* **Rule-Based Modeling:** Salary bands use fixed ranges per job level, and car prices use a basic linear depreciation heuristic rather than fitted statistical distributions or economic market models.
* **Version Metadata Mismatch:** Package versions differ between `pyproject.toml` (`0.1.1`), `setup.py` (`0.1.0`), and `datagen/__init__.py` (`0.1.0`).

## Planned Improvements

Future development on Datagen is planned across the following priorities:

### Priority 1 — Core Package Quality
* Implement `datagen/cli.py` to fix the broken CLI entry point.
* Add an automated unit test suite using `pytest` to cover generators, seed reproducibility, and file exports.
* Harmonize package version metadata across `pyproject.toml`, `setup.py`, and `datagen/__init__.py`.
* Set up a GitHub Actions CI workflow to run tests and linters automatically on pull requests.

### Priority 2 — Functionality & Refactoring
* Introduce relational data generation to support foreign keys and referential integrity between generated entities.
* Refactor shared generator logic (input validation, seed setting, format conversion) into reusable base utilities.
* Transition print statements to standard Python `logging`.
* Improve Docker development practices (add `.dockerignore` and non-root user execution).

### Future Roadmap
* Implement streaming/batch generation to write large datasets directly to disk.
* Add statistical probability distributions (e.g. log-normal distributions for salary and price modeling).
* Establish performance benchmarks for generation throughput and RAM usage.
