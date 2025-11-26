#!/usr/bin/env python3
"""
Results Analysis Script
Generates comprehensive comparison tables and statistics for the project report
"""

import json
import pandas as pd
import numpy as np
import cv2
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, 'src')

from metrics import evaluate_enhancement
from utils import load_image

def analyze_all_results(input_dir="data/input", output_dir="data/output"):
    """Analyze all processed images and generate comparison tables."""

    input_path = Path(input_dir)
    output_path = Path(output_dir)

    # Collect all results
    all_results = []

    print("Analyzing all processed images...")
    print("=" * 80)

    for img_file in sorted(input_path.glob("*.jpg")):
        base_name = img_file.stem

        # Load original
        original = load_image(str(img_file))

        # Load GHE result
        ghe_file = output_path / f"{base_name}_ghe.png"
        if not ghe_file.exists():
            print(f"Skipping {base_name}: GHE output not found")
            continue

        ghe_enhanced = load_image(str(ghe_file))

        # Load CLAHE result
        clahe_files = list(output_path.glob(f"{base_name}_clahe_*.png"))
        if not clahe_files:
            print(f"Skipping {base_name}: CLAHE output not found")
            continue

        clahe_enhanced = load_image(str(clahe_files[0]))

        # Calculate metrics
        ghe_metrics = evaluate_enhancement(original, ghe_enhanced, "GHE")
        clahe_metrics = evaluate_enhancement(original, clahe_enhanced, "CLAHE")

        # Extract category from filename
        category = "_".join(base_name.split("_")[:-1])

        # Store results
        all_results.append({
            'image': base_name,
            'category': category,
            'ghe_psnr': ghe_metrics['psnr'],
            'clahe_psnr': clahe_metrics['psnr'],
            'ghe_ssim': ghe_metrics['ssim'],
            'clahe_ssim': clahe_metrics['ssim'],
            'ghe_entropy_improvement': ghe_metrics['entropy_improvement'],
            'clahe_entropy_improvement': clahe_metrics['entropy_improvement'],
            'ghe_contrast_improvement': ghe_metrics['contrast_improvement'],
            'clahe_contrast_improvement': clahe_metrics['contrast_improvement'],
            'ghe_naturalness': ghe_metrics['naturalness_enhanced'],
            'clahe_naturalness': clahe_metrics['naturalness_enhanced'],
            'ghe_sharpness': ghe_metrics['sharpness_enhanced'],
            'clahe_sharpness': clahe_metrics['sharpness_enhanced'],
            'ghe_over_enhanced': ghe_metrics['over_enhancement_detected'],
            'clahe_over_enhanced': clahe_metrics['over_enhancement_detected'],
        })

        print(f"✓ Analyzed: {base_name}")

    # Create DataFrame
    df = pd.DataFrame(all_results)

    # Save detailed results
    df.to_csv('results/detailed_results.csv', index=False)
    print(f"\n✓ Saved detailed results to: results/detailed_results.csv")

    # Generate summary statistics
    print("\n" + "=" * 80)
    print("SUMMARY STATISTICS")
    print("=" * 80)

    # Overall averages
    print("\n--- Overall Averages ---")
    print(f"GHE  - PSNR: {df['ghe_psnr'].mean():.2f} dB, SSIM: {df['ghe_ssim'].mean():.4f}")
    print(f"CLAHE - PSNR: {df['clahe_psnr'].mean():.2f} dB, SSIM: {df['clahe_ssim'].mean():.4f}")

    print(f"\nGHE  - Entropy Improvement: {df['ghe_entropy_improvement'].mean():.2%}")
    print(f"CLAHE - Entropy Improvement: {df['clahe_entropy_improvement'].mean():.2%}")

    print(f"\nGHE  - Contrast Improvement: {df['ghe_contrast_improvement'].mean():.2%}")
    print(f"CLAHE - Contrast Improvement: {df['clahe_contrast_improvement'].mean():.2%}")

    print(f"\nGHE  - Naturalness: {df['ghe_naturalness'].mean():.4f}")
    print(f"CLAHE - Naturalness: {df['clahe_naturalness'].mean():.4f}")

    print(f"\nGHE  - Over-enhancement Rate: {df['ghe_over_enhanced'].mean():.1%}")
    print(f"CLAHE - Over-enhancement Rate: {df['clahe_over_enhanced'].mean():.1%}")

    # By category
    print("\n--- By Category ---")
    category_summary = df.groupby('category').agg({
        'ghe_psnr': 'mean',
        'clahe_psnr': 'mean',
        'ghe_ssim': 'mean',
        'clahe_ssim': 'mean',
        'ghe_naturalness': 'mean',
        'clahe_naturalness': 'mean'
    }).round(3)

    print(category_summary.to_string())

    # Save summary
    category_summary.to_csv('results/category_summary.csv')
    print(f"\n✓ Saved category summary to: results/category_summary.csv")

    # Winner analysis
    print("\n--- Method Comparison (Winner Count) ---")
    ghe_wins = {
        'PSNR': (df['ghe_psnr'] > df['clahe_psnr']).sum(),
        'SSIM': (df['ghe_ssim'] > df['clahe_ssim']).sum(),
        'Naturalness': (df['ghe_naturalness'] > df['clahe_naturalness']).sum(),
    }

    clahe_wins = {
        'PSNR': (df['clahe_psnr'] > df['ghe_psnr']).sum(),
        'SSIM': (df['clahe_ssim'] > df['ghe_ssim']).sum(),
        'Naturalness': (df['clahe_naturalness'] > df['ghe_naturalness']).sum(),
    }

    total_images = len(df)
    print(f"\nTotal images analyzed: {total_images}")
    print("\nGHE wins:")
    for metric, count in ghe_wins.items():
        print(f"  {metric}: {count}/{total_images} ({count/total_images:.1%})")

    print("\nCLAHE wins:")
    for metric, count in clahe_wins.items():
        print(f"  {metric}: {count}/{total_images} ({count/total_images:.1%})")

    print("\n" + "=" * 80)
    print("Analysis complete!")
    print("=" * 80)

    return df


if __name__ == "__main__":
    # Create results directory
    Path("results").mkdir(exist_ok=True)

    # Run analysis
    df = analyze_all_results()

    print("\nNext steps:")
    print("1. Review results/detailed_results.csv")
    print("2. Review results/category_summary.csv")
    print("3. Create visualizations for your report")
