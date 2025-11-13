import os
from prefect import flow, task
from prefect.logging import get_run_logger
from prefect_dbt.cli import DbtCoreOperation

PROJECT_DIR = os.path.join(os.path.dirname(__file__), "..", "dbt_demo")
DBT_PROFILES_DIR = os.path.join(os.path.dirname(__file__), "..", "dbt_demo")
MODELS_DIR = os.path.join(PROJECT_DIR, "models")
SEEDS_DIR = os.path.join(PROJECT_DIR, "seeds")

@task
def discover_dbt_paths():
    logger = get_run_logger()
    models = []
    seeds = []

    if os.path.exists(MODELS_DIR):
        for name in os.listdir(MODELS_DIR):
            if name.endswith(".sql"):
                models.append(os.path.splitext(name)[0])
    
    if os.path.exists(SEEDS_DIR):
        for name in os.listdir(SEEDS_DIR):
            if name.endswith(".csv"):
                seeds.append(os.path.splitext(name)[0])
    logger.info(f"DBT Project Directory: {PROJECT_DIR}")
    logger.info(f"DBT Profiles Directory: {DBT_PROFILES_DIR}")
    logger.info(f"DBT Models Directory: {MODELS_DIR}")
    logger.info(f"DBT Seeds Directory: {SEEDS_DIR}")

    model_selection = ", ".join(models) if models else "*"
    seed_selection = ", ".join(seeds) if seeds else "*"

    return model_selection, seed_selection

@task
def run_dbt_seeds(model: None, full_refresh: bool = False):
    logger = get_run_logger()
    logger.info(f"Running DBT seeds for: {model}")
    commands = ["dbt seed"]
    if model:
        commands.append(f"--select {model}")
    if full_refresh:
        commands.append("--full-refresh")
    commands = " ".join(commands)
    logger.info(f"DBT Seed Commands: {' '.join(commands)}")
    dbt_task = DbtCoreOperation(commands=[commands],
                                   project_dir=PROJECT_DIR, profiles_dir=DBT_PROFILES_DIR, log_print=True)

    result = dbt_task.run()
    return result

@task
def run_dbt_models(model_selection: str):
    logger = get_run_logger()
    logger.info(f"Running DBT models for: {model_selection}")

    dbt_task = DbtCoreOperation(commands=["dbt run"], select=model_selection,
                                   project_dir=PROJECT_DIR, profiles_dir=DBT_PROFILES_DIR)

    result = dbt_task.run()
    return result

# Exercise Task Stub: Implement dbt tests
@task
def run_dbt_tests(model_selection: str | None = None):
        """EXERCISE: Implement dbt test execution.

        TODO:
            1. Accept an optional model_selection (space-separated model names or '*').
            2. Build a single command string using the pattern:
                 - 'dbt test' OR 'dbt test --select <models>' when selection provided.
            3. Use DbtCoreOperation to run the command (similar to run_dbt_models).
            4. Log the command before execution.
            5. Return the raw result object.
            6. (Stretch) Add simple success heuristic to raise on failure.

        Starter template below—replace pass with working code.
        """
        logger = get_run_logger()
        logger.info("(Exercise) dbt test task invoked with selection: %s", model_selection)
        # Your implementation here:
        # command = "dbt test" if not model_selection or model_selection == "*" else f"dbt test --select {model_selection}"
        # op = DbtCoreOperation(commands=[command], project_dir=PROJECT_DIR, profiles_dir=DBT_PROFILES_DIR, log_print=True)
        # result = op.run()
        # return result
        pass

@flow(name="prefect_dbt_subflow_run", log_prints=True)
def prefect_dbt_subflow_run(model_selection):

    logger = get_run_logger()
    logger.info("Starting DBT models run subflow...")
    run_dbt_models(model_selection)

@flow(name="prefect_dbt_run", log_prints=True)
def prefect_dbt_flow_run(full_refresh: bool = False, seed_name: str = "test.csv"):

    model_selection, seed_selection = discover_dbt_paths()
    if seed_name:
        run_dbt_seeds(model = seed_name, full_refresh = True)
    else:
        run_dbt_seeds(seed_selection)

    #run_dbt_models(model_selection)
    prefect_dbt_subflow_run(model_selection)

if __name__ == "__main__":
    prefect_dbt_flow_run()