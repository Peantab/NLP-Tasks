#!/usr/bin/env bash

PYTHON_INTERPRETER=python3

echo "Doing task 1..."
$PYTHON_INTERPRETER main.py 1 > task1.csv

echo "Doing task 2..."
$PYTHON_INTERPRETER main.py 2 > task2.csv

echo "Doing task 3..."
$PYTHON_INTERPRETER main.py 3 > task3.txt

echo "Creating markdown..."
{
echo -e "# Results\n\n* [Task 1](#task-1)\n* [Task 2](#task-2)\n* [Task 3](#task-3)\n\n## Task 1\nExternal references to bills:\n\`\`\`csv"
cat task1.csv
echo -e "\`\`\`\n## Task 2\nInternal references to regulations:\n\`\`\`csv"
cat task2.csv
echo -e "\`\`\`\n## Task 3\nOccurrences of the word *ustawa*\n\`\`\`plaintext"
cat task3.txt
echo -e "\`\`\`"
} > results.md

echo "Done."