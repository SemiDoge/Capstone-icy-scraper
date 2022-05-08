#!/bin/bash
mkdir -p local_responses
mkdir -p scraped_data

python -m unittest common_utils_test cambridge_utils_test kitchener_utils_test waterloo_utils_test -v