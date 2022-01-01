ARG BASE
FROM $BASE as base-builder
RUN apt-get update && apt-get install --no-install-recommends -y wget curl python3-dev gnupg2 build-essential && apt-get clean
RUN pip install poetry

FROM base-builder as builder
# Install python dependencies in /.venv
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
COPY src/pyproject.toml pyproject.toml
COPY src/poetry.lock poetry.lock
RUN poetry install --no-dev --no-root

# Build Actual Image
ARG BASE
FROM $BASE
ENV UID fastapi
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
# Copy the venv files
COPY --from=builder /.venv /.venv
ENV PATH="/.venv/bin:$PATH"
RUN addgroup --gid 10001 $UID && adduser --disabled-password --gecos ""  --ingroup $UID --uid 10001 $UID
# Add the application files
COPY src/app /app
RUN chown $UID:$UID -R /app
WORKDIR /app
USER $UID
