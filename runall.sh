#!/usr/bin/env bash

PYTHON_INTERPRETER=python3

echo "Doing task 1..."
$PYTHON_INTERPRETER main.py 1 > task1.csv

echo "Doing task 2..."
$PYTHON_INTERPRETER main.py 2 > task2.csv

echo "Doing task 3..."
$PYTHON_INTERPRETER main.py 3 > task3.txt

echo "Done."