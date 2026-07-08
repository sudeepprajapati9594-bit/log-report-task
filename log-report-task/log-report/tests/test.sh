#!/bin/bash

# pytest is baked into the environment image (environment/Dockerfile).
pytest /tests/test_outputs.py -rA
exit_code=$?

mkdir -p /logs/verifier
if [ "$exit_code" -eq 0 ]; then
  echo 1 > /logs/verifier/reward.txt
else
  echo 0 > /logs/verifier/reward.txt
fi
