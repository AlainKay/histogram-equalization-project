#!/bin/bash
# Batch process all images in data/input/

echo "=========================================="
echo "Processing All Images"
echo "=========================================="

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Activate venv and set python
PYTHON="./venv/bin/python"

# Counter
count=0

# Process each jpg in data/input (excluding .gitkeep)
for img in data/input/*.jpg; do
    if [ -f "$img" ]; then
        echo ""
        echo "Processing: $img"
        echo "------------------------------------------"

        $PYTHON src/main.py \
            --input "$img" \
            --method both \
            --clip-limit 2.0 \
            --tile-size 8 \
            --color-space LAB

        count=$((count + 1))
    fi
done

echo ""
echo "=========================================="
echo "Completed! Processed $count images"
echo "Results saved to: data/output/"
echo "=========================================="
