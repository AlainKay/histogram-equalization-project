# Quick Start Guide

Get up and running with histogram equalization in 5 minutes!

## Prerequisites

- Python 3.8+ installed
- Virtual environment already created (`venv/`)
- Terminal access

## Step 1: Setup (2 minutes)

### For School Servers (Recommended)

```bash
# Navigate to project
cd histogram_equalization_project

# Install dependencies using venv Python directly
./venv/bin/pip install -r requirements.txt

# Verify installation
./venv/bin/python -c "import cv2; print('✓ OpenCV installed:', cv2.__version__)"
```

### For Local Machines

```bash
# Navigate to project
cd histogram_equalization_project

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "import cv2; print('✓ OpenCV installed:', cv2.__version__)"
```

## Step 2: Build Your Dataset (5 minutes)

### Get API Key

1. Go to [Unsplash Developers](https://unsplash.com/developers)
2. Sign up / Log in
3. Create a new app
4. Copy your **Access Key**

### Download Images

```bash
./venv/bin/python src/dataset_builder.py
```

When prompted:
1. **Unsplash API Key**: Paste your key
2. **Pexels API Key**: Press Enter to skip
3. **Standard images**: Type `y`

**Result:** ~25 images downloaded to `data/input/`

## Step 3: Process Images (5 minutes)

### Quick Test (One Image)

```bash
./venv/bin/python src/main.py \
    --input data/input/dark_portrait_01.jpg \
    --method both
```

**Output:**
- Enhanced images in `data/output/`
- Metrics printed to console

### Batch Process (All Images)

```bash
./process_all.sh
```

**Result:** All images processed with GHE and CLAHE

## Step 4: Analyze Results (2 minutes)

```bash
./venv/bin/python analyze_results.py
```

**Output:**
- `results/detailed_results.csv` - Complete metrics table
- `results/category_summary.csv` - Averages by category
- Console summary with GHE vs CLAHE comparison

## Step 5: View Results

### Command Line

```bash
# List enhanced images
ls data/output/

# View CSV results
cat results/category_summary.csv
```

### Visual Comparison

```bash
# Compare original vs GHE vs CLAHE
eog data/input/dark_portrait_01.jpg \
    data/output/dark_portrait_01_ghe.png \
    data/output/dark_portrait_01_clahe_clip2.0_tile8.png
```

## Common Commands

### Process Single Image with Custom Settings

```bash
./venv/bin/python src/main.py \
    --input data/input/foggy_landscape_01.jpg \
    --method clahe \
    --clip-limit 3.0 \
    --tile-size 16 \
    --color-space LAB
```

### Process Specific Category

```bash
# Process only dark portraits
for img in data/input/dark_portrait_*.jpg; do
    ./venv/bin/python src/main.py --input "$img" --method both
done
```

### Re-analyze Results

```bash
./venv/bin/python analyze_results.py
```

## Troubleshooting

### Problem: `ModuleNotFoundError: No module named 'cv2'`

**Solution:** Use venv Python directly:
```bash
./venv/bin/python src/main.py --input data/input/image.jpg --method both
```

### Problem: `command not found: process_all.sh`

**Solution:** Make script executable:
```bash
chmod +x process_all.sh
./process_all.sh
```

### Problem: Conda interfering with venv

**Solution:** Deactivate conda first:
```bash
conda deactivate
source venv/bin/activate
```

## Project Workflow Summary

```
1. Setup
   ↓
2. Build Dataset (dataset_builder.py)
   ↓
3. Process Images (process_all.sh)
   ↓
4. Analyze Results (analyze_results.py)
   ↓
5. Generate Report (use CSV files)
```

## What You Get

### Metrics (for each image)

**Quantitative:**
- PSNR (quality)
- SSIM (similarity)
- Entropy (information)
- Contrast improvement
- Brightness change

**Qualitative:**
- Sharpness
- Naturalness
- Colorfulness
- Blocking artifacts
- Over-enhancement detection

### Output Files

```
data/output/
├── [image]_ghe.png                    # GHE result
└── [image]_clahe_clip2.0_tile8.png   # CLAHE result

results/
├── detailed_results.csv               # All metrics
└── category_summary.csv               # Category averages
```

## Next Steps

### For Your Report

1. **Open CSV files** in Excel/Google Sheets
2. **Create tables** from category_summary.csv
3. **Select best examples** for visual comparison
4. **Analyze** which method works better for each scenario

### For Further Experimentation

Try different CLAHE parameters:

```bash
# Conservative (less aggressive)
./venv/bin/python src/main.py \
    --input data/input/image.jpg \
    --method clahe \
    --clip-limit 1.5 \
    --tile-size 4

# Aggressive (more enhancement)
./venv/bin/python src/main.py \
    --input data/input/image.jpg \
    --method clahe \
    --clip-limit 4.0 \
    --tile-size 32
```

## Command Reference

| Task | Command |
|------|---------|
| Build dataset | `./venv/bin/python src/dataset_builder.py` |
| Process one image | `./venv/bin/python src/main.py --input IMAGE --method both` |
| Process all images | `./process_all.sh` |
| Analyze results | `./venv/bin/python analyze_results.py` |
| View images | `eog data/output/*.png` |
| View results | `cat results/category_summary.csv` |

## Tips

- **Use LAB color space** for best color preservation
- **clip_limit=2.0, tile_size=8** are good defaults for CLAHE
- **Process different categories** separately for better analysis
- **Save terminal output** to capture all metrics
- **Compare visually** before relying only on numbers

## Getting Help

- Check [README.md](README.md) for detailed documentation
- Review project paper for algorithm details
- Check troubleshooting section above

## Full Example Session

```bash
# 1. Setup
cd histogram_equalization_project
./venv/bin/pip install -r requirements.txt

# 2. Build dataset
./venv/bin/python src/dataset_builder.py
# Paste Unsplash API key when prompted

# 3. Process all images
./process_all.sh

# 4. Analyze results
./venv/bin/python analyze_results.py

# 5. View results
cat results/category_summary.csv
ls data/output/

# Done! Use CSV files for your report.
```

---

**Ready to start?** Run the first command and follow along! 🚀
