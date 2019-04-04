#!/usr/bin/env bash

PYTHON_INTERPRETER=python3

echo "Executing tasks..."
${PYTHON_INTERPRETER} main.py > output.md

echo "Creating markdown..."
{
echo -e "# Results\n\n## Results for measures\n\n\`\`\`"
cat output.md
echo -e "\`\`\`\n## Answers for questions\n\n"
cat answers.md
} > results.md

echo "Done."