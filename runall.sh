#!/usr/bin/env bash

PYTHON_INTERPRETER=python3

echo "Preparing data... (this may take some time)"
$PYTHON_INTERPRETER main.py init

echo "Waiting 2s for ElasticSearch to process data..."
sleep 2s

echo "Doing tasks..."
$PYTHON_INTERPRETER main.py > results.txt

echo "Clean up..."
$PYTHON_INTERPRETER main.py stop

echo "Creating markdown..."
{
echo -e "# Results\n\n\`\`\`plaintext"
cat results.txt
echo -e "\`\`\`"
} > results.md

echo "Done."