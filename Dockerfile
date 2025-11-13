FROM python:3.11-slim

# Install system deps
RUN apt-get update && apt-get install -y git curl build-essential libpq-dev

# Install Python libs: prefect client (2.x to match server), prefect-dbt compatible, dbt-postgres
# We choose latest Prefect 2 minor; adjust if mismatch reported
RUN pip install --no-cache-dir \
	"prefect>=2.20,<3" \
	"prefect-dbt>=0.4,<0.5" \
	dbt-postgres

# Create workspace
WORKDIR /usr/app
COPY . .

CMD ["bash"]
