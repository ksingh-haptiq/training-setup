# Prefect Demo Flows

This repository contains two Prefect flows demonstrating how to orchestrate data pipelines and verify a working Prefect setup.

---

## Overview

### **1. demo.py**

A simple ETL (Extract–Transform–Load) pipeline built using Prefect, Pandas, and SQLAlchemy.

#### **Flow Structure**

| Step | Task | Description |
|------|------|--------------|
| 1 | **Extract** | Fetches user data from a public API (`https://jsonplaceholder.typicode.com/users`) and converts it into a Pandas DataFrame. |
| 2 | **Transform** | Cleans the data by removing unnecessary columns (`address`, `company`). |
| 3 | **Load to Postgres** | Writes the transformed data into a PostgreSQL table named `users_api`. |

This flow demonstrates how Prefect can be used to build reliable, observable data workflows that integrate with APIs and databases.

---

### **2. hello.py**

A minimal Prefect flow designed to test a working setup.  
It simply logs a “Hello World” message and confirms that Prefect runs successfully.

---

## Setup

The flows assume the following:
- Python environment with Prefect, Pandas, SQLAlchemy, and Requests installed.  
- A PostgreSQL database accessible using the connection string defined in the flow.  
- Optional Docker setup for local testing of Prefect and Postgres.

---

## Improvement Challenge

The `transform()` task currently removes a fixed set of columns.  
To make it more flexible and reusable, consider extending it with additional functionality such as:

- Accepting a list of columns to drop dynamically.  
- Allowing column renaming through a mapping dictionary.  
- Adding transformations such as filtering, type conversion, or data enrichment.

**Question:**  
*How can you modify the `transform()` task so that it can accept parameters (for example, `drop_columns` or `rename_columns`) and handle different API responses without changing the core flow code? You can create and add your own scenarios too.*


## 🧪 Prefect Exercise: Run dbt Tests

This exercise uses the flow `flows/prefect_dbt_run.py` to seed data, run models.
### 1. Parameters
- `full_refresh` (bool): Pass True to include `--full-refresh` when seeding.
- `seed_name` (str|None): Single seed to run. If omitted, all discovered seeds run (without `--select`)

### 2. Run Inside Prefect Docker Container
```bash
docker compose exec prefect bash -lc "python -m flows.prefect_dbt_run"
```

### 3. Exercise: Implement dbt test task

Open `flows/prefect_dbt_run.py` and locate the stubbed task:
```python
@task
def run_dbt_tests(model_selection: str | None = None):
	"""EXERCISE: Implement dbt test execution."""
	# TODO: build command and run via DbtCoreOperation
	pass
```

Complete the TODO:
1. Accept optional model_selection; if None or '*', run all tests.
2. Construct command:
   - All tests: `dbt test`
   - Selected: `dbt test --select <space-separated-models>`
3. Execute with `DbtCoreOperation(commands=[command], project_dir=..., profiles_dir=...)`.
4. Log command before running.
5. Return the raw result.
6. (Optional) Implement a success heuristic to raise on failure.

Then add a `run_tests: bool = False` parameter to the flow:
```python
@flow
def prefect_dbt_flow_run(run_tests: bool = False, ...):
	...
	if run_tests:
		run_dbt_tests(model_selection)
```

Run examples after implementation:
```bash
python -m flows.prefect_dbt_run
python -m flows.prefect_dbt_run --run-tests true
```


---

````
