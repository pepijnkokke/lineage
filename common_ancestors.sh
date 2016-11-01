#!/bin/bash

# Check if we have two arguments.
if [ "$#" -ne 2 ]; then
    echo "usage: common_ancestors <MGP id 1> <MGP id 2>"
fi

# Collect ancestry of $1 (unless it exists).
if [ ! -f "$1.jl" ]; then
    echo "Collecting ancestry of $1..."
    scrapy runspider -LERROR ancestor_scraper.py -o "$1.jl" -a start-id="$1"
fi

# Collect ancestry of $1 (unless it exists).
if [ ! -f "$2.jl" ]; then
    echo "Collecting ancestry of $2..."
    scrapy runspider -LERROR ancestor_scraper.py -o "$2.jl" -a start-id="$2"
fi

# Compute the first common ancestors.
python common_ancestors.py "$1.jl" "$2.jl"
