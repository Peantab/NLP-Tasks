#!/usr/bin/env bash

PYTHON_INTERPRETER=python3

echo "Preparing data... (this may take some time)"
${PYTHON_INTERPRETER} main.py init

echo "Waiting 2s for ElasticSearch to process data..."
sleep 2s

echo "Executing tasks..."
${PYTHON_INTERPRETER} main.py > results.txt

echo "Clean up..."
${PYTHON_INTERPRETER} main.py stop

echo "Creating markdown..."
{
echo -e "# Results\n\n"
echo -e "A plot in a logarithmic scale, where X-axis contains the rank of a term and Y-axis contains the number of occurrences of the term with given rank.\n\n![Plot in a logarithmic scale](plot.png)"
echo -e "\n\`\`\`"
cat results.txt
echo -e "\`\`\`"
} > results.md

echo "Done."