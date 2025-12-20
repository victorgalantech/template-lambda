# Use AWS Lambda Python 3.12 base image
FROM public.ecr.aws/lambda/python:3.12

# Update OS packages to patch security vulnerabilities
# Fixes CVE-2025-13601 in glib2 and other security issues
RUN dnf makecache --refresh && \
    dnf upgrade -y --security && \
    dnf clean all

# Set working directory
WORKDIR ${LAMBDA_TASK_ROOT}

# Copy requirements or use poetry to export requirements
COPY pyproject.toml poetry.lock* ./

# Install poetry
RUN pip install poetry==1.7.1

# Configure poetry to not create virtual environment
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --only main --no-interaction --no-ansi

# Copy source code
COPY src/ ${LAMBDA_TASK_ROOT}/src/

# Copy entrypoint
COPY entrypoint.py ${LAMBDA_TASK_ROOT}/

# Set the CMD to your handler
CMD ["entrypoint.lambda_handler"]
