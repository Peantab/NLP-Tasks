#!/usr/bin/env bash

PYTHON_INTERPRETER=python3

echo "Executing tasks..."
${PYTHON_INTERPRETER} main.py

echo "Creating markdown..."
{
echo -e "# Results\n\nTop 50 bigrams (in terms of LLR) including noun at the first position and noun or adjective at the second position:\n\n\`\`\`"
cat results.txt
echo -e "\n\`\`\`"
} > results.md

echo "Done."