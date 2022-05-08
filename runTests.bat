@echo off
if not exist .\local_responses\ mkdir local_responses
if not exist .\scraped_data\ mkdir scraped_data

ECHO Running all tests
.\.venv\Scripts\python.exe -m unittest common_utils_test cambridge_utils_test kitchener_utils_test waterloo_utils_test -v