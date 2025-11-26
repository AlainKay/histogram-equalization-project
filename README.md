# Histogram Equalization for Image Enhancement

## Project Overview
This project implements and compares Global Histogram Equalization (GHE) and Contrast Limited Adaptive Histogram Equalization (CLAHE) for improving image contrast and visual quality. The project includes comprehensive quantitative and qualitative evaluation metrics.

## Team Members
- **Alain Kariyanga**: GHE implementation, evaluation metrics (PSNR, SSIM, entropy), qualitative metrics, performance analysis
- **Pragya Mishra**: CLAHE implementation, visual evaluations, parameter tuning, documentation

## Project Structure
```
histogram_equalization_project/
├── src/
│   ├── ghe.py                  # Global Histogram Equalization implementation
│   ├── clahe.py                # CLAHE implementation
│   ├── metrics.py              # Quantitative metrics (PSNR, SSIM, Entropy, etc.)
│   ├── qualitative_metrics.py  # Qualitative/perceptual metrics (no-reference)
│   ├── utils.py                # Utility functions (load, save, display)
│   ├── main.py                 # Main execution script
│   └── dataset_builder.py      # API-based dataset builder
├── data/
│   ├── input/                  # Input images
│   └── output/                 # Enhanced images
├── results/                    # Analysis results and CSV files
├── notebooks/
│   └── experiments.ipynb       # Jupyter notebook for experiments
├── docs/                       # Documentation
├── requirements.txt            # Python dependencies
├── process_all.sh              # Batch processing script
├── analyze_results.py          # Results analysis and comparison
├── QUICKSTART.md               # Quick start guide
└── README.md                   # This file
```

## Key Features

### ✓ Implementation
- **GHE (Global Histogram Equalization)** - Fast global contrast enhancement
- **CLAHE (Contrast Limited Adaptive Histogram Equalization)** - Adaptive local enhancement
- Support for both grayscale and color images
- Multiple color space options (YCrCb, HSV, LAB)

### ✓ Evaluation Metrics

**Quantitative (Reference-based):**
- PSNR (Peak Signal-to-Noise Ratio)
- SSIM (Structural Similarity Index)
- Entropy (Information Content)
- Contrast (RMS)
- Brightness

**Qualitative (No-reference):**
- Sharpness (Laplacian variance)
- Naturalness (histogram-based)
- Colorfulness (Hasler & Süsstrunk method)
- Blocking artifacts detection
- Over-enhancement detection

### ✓ Dataset Builder
- Automated image collection via Unsplash API
- Support for Pexels API
- Standard test images (Lena, Baboon, Peppers)
- Curated queries for histogram equalization scenarios

### ✓ Analysis Tools
- Batch processing script
- Automated results analysis
- CSV export for report tables
- Category-wise comparison

## Setup

### Prerequisites
- Python 3.13+ (or Python 3.8+)
- Virtual environment recommended

### Installation

**Option 1: Using venv Python directly (Recommended for school servers)**
```bash
# Navigate to project directory
cd histogram_equalization_project

# Install dependencies
./venv/bin/pip install -r requirements.txt
```

**Option 2: Standard activation**
```bash
# Deactivate conda if active
conda deactivate

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Verify Installation
```bash
./venv/bin/python -c "import cv2; print('OpenCV:', cv2.__version__)"
```

## Usage

### 1. Build Dataset (Optional)

Get free API key from [Unsplash](https://unsplash.com/developers), then:

```bash
./venv/bin/python src/dataset_builder.py
```

This will download ~25 images optimized for histogram equalization testing.

### 2. Process Images

**Single Image:**
```bash
./venv/bin/python src/main.py \
    --input data/input/image.jpg \
    --method both \
    --show
```

**Batch Processing (all images):**
```bash
./process_all.sh
```

**Custom Parameters:**
```bash
./venv/bin/python src/main.py \
    --input data/input/image.jpg \
    --method clahe \
    --clip-limit 3.0 \
    --tile-size 16 \
    --color-space LAB
```

### 3. Analyze Results

```bash
./venv/bin/python analyze_results.py
```

**Outputs:**
- `results/detailed_results.csv` - All metrics for each image
- `results/category_summary.csv` - Averages by category
- Console summary with method comparison

### Command-Line Options

**main.py:**
- `--input` - Path to input image (required)
- `--method` - Enhancement method: `ghe`, `clahe`, or `both` (default: both)
- `--output` - Output directory (default: data/output/)
- `--clip-limit` - CLAHE clip limit (default: 2.0)
- `--tile-size` - CLAHE tile grid size (default: 8)
- `--color-space` - Color space: YCrCb, HSV, or LAB (default: LAB)
- `--show` - Display results
- `--grayscale` - Process as grayscale

## Algorithms

### Global Histogram Equalization (GHE)
- Redistributes pixel intensity values globally using CDF
- Simple and computationally efficient
- Works well for uniformly underexposed images
- May over-enhance regions with non-uniform lighting

**Implementation:** `src/ghe.py`

### CLAHE (Contrast Limited Adaptive Histogram Equalization)
- Applies histogram equalization to local regions (tiles)
- Limits contrast amplification via clip limit
- Better preserves local details and prevents noise amplification
- Requires parameter tuning (clip_limit, tile_grid_size)

**Implementation:** `src/clahe.py`

## Evaluation Metrics

### Quantitative Metrics (`src/metrics.py`)
| Metric | Description | Range | Better Value |
|--------|-------------|-------|--------------|
| PSNR | Peak Signal-to-Noise Ratio | 0-∞ dB | Higher |
| SSIM | Structural Similarity Index | 0-1 | Closer to 1 |
| Entropy | Information content | 0-8 bits | Higher |
| Contrast | RMS contrast | 0-255 | Higher (for enhancement) |
| Brightness | Average intensity | 0-255 | Context-dependent |

### Qualitative Metrics (`src/qualitative_metrics.py`)
| Metric | Description | Range | Better Value |
|--------|-------------|-------|--------------|
| Sharpness | Edge definition (Laplacian variance) | 0-∞ | Higher |
| Naturalness | Natural appearance | 0-1 | Higher |
| Colorfulness | Color saturation | 0-100+ | Context-dependent |
| Blocking Artifacts | Tile boundary artifacts | 0-1 | Lower |
| Over-enhancement | Detects unnatural enhancement | Boolean | False |

## Results Structure

After processing, your results will be organized as:

```
data/output/
├── dark_portrait_01_ghe.png
├── dark_portrait_01_clahe_clip2.0_tile8.png
├── foggy_landscape_01_ghe.png
├── foggy_landscape_01_clahe_clip2.0_tile8.png
└── ...

results/
├── detailed_results.csv      # All metrics for each image
└── category_summary.csv      # Averages by image category
```

## Troubleshooting

### Import Errors
If you see `ModuleNotFoundError: No module named 'cv2'`:
```bash
# Use venv Python directly
./venv/bin/python src/main.py --input data/input/image.jpg --method both
```

### Conda Interference
If using a school server with conda:
```bash
# Deactivate conda first
conda deactivate

# Then activate venv
source venv/bin/activate
```

### Permission Issues
```bash
# Make scripts executable
chmod +x process_all.sh
chmod +x analyze_results.py
```

## Project Workflow

1. **Setup** - Install dependencies and verify installation
2. **Build Dataset** - Use `dataset_builder.py` to fetch test images
3. **Process Images** - Run `process_all.sh` for batch processing
4. **Analyze Results** - Run `analyze_results.py` for comparison tables
5. **Generate Report** - Use CSV files and images for your paper

## References

1. R. C. Gonzalez and R. E. Woods, *Digital Image Processing*, 4th ed. Pearson, 2018.
2. S. M. Pizer et al., "Adaptive histogram equalization and its variations," *Computer Vision, Graphics, and Image Processing*, vol. 39, no. 3, pp. 355–368, 1987.
3. M. Zuiderveld, "Contrast Limited Adaptive Histogram Equalization," in *Graphics Gems IV*, Academic Press, 1994, pp. 474–485.
4. D. Hasler and S. Süsstrunk, "Measuring Colourfulness in Natural Images," *Human Vision and Electronic Imaging VIII*, 2003.

## License

This project is for academic purposes as part of the CS course at Kennesaw State University.

## Contact

- Alain Kariyanga - akayiran@students.kennesaw.edu
- Pragya Mishra - pmishra1@students.kennesaw.edu
