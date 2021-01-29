#!/bin/bash

poetry run pytest tests
poetry run pytest integration_tests
# poetry run pytest e2e_tests