"""
Main Script for Histogram Equalization Project
Authors: Alain Kariyanga & Pragya Mishra

This script provides a command-line interface for applying GHE and CLAHE
to images and evaluating the results.
"""

import argparse
import os
import cv2
import numpy as np
from pathlib import Path

# Import our modules
from ghe import apply_ghe
from clahe import apply_clahe
from metrics import evaluate_enhancement, print_metrics
from utils import load_image, save_image, display_images, plot_histograms


def main():
    parser = argparse.ArgumentParser(
        description='Histogram Equalization for Image Enhancement'
    )
    parser.add_argument(
        '--input',
        type=str,
        required=True,
        help='Path to input image'
    )
    parser.add_argument(
        '--method',
        type=str,
        choices=['ghe', 'clahe', 'both'],
        default='both',
        help='Enhancement method to apply'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='data/output',
        help='Output directory'
    )
    parser.add_argument(
        '--clip-limit',
        type=float,
        default=2.0,
        help='CLAHE clip limit (default: 2.0)'
    )
    parser.add_argument(
        '--tile-size',
        type=int,
        default=8,
        help='CLAHE tile grid size (default: 8x8)'
    )
    parser.add_argument(
        '--color-space',
        type=str,
        choices=['YCrCb', 'HSV', 'LAB'],
        default='LAB',
        help='Color space for enhancement (default: LAB)'
    )
    parser.add_argument(
        '--show',
        action='store_true',
        help='Display results'
    )
    parser.add_argument(
        '--grayscale',
        action='store_true',
        help='Process as grayscale image'
    )

    args = parser.parse_args()

    # Load image
    print(f"Loading image: {args.input}")
    image = load_image(args.input, grayscale=args.grayscale)
    print(f"Image shape: {image.shape}")

    # Prepare output directory
    os.makedirs(args.output, exist_ok=True)
    base_name = Path(args.input).stem

    # Store results
    results = {'Original': image}
    metrics_results = []

    # Apply GHE
    if args.method in ['ghe', 'both']:
        print("\nApplying Global Histogram Equalization (GHE)...")
        ghe_result = apply_ghe(image, color_space=args.color_space)
        results['GHE'] = ghe_result

        # Save result
        output_path = os.path.join(args.output, f"{base_name}_ghe.png")
        save_image(ghe_result, output_path)
        print(f"Saved GHE result to: {output_path}")

        # Evaluate
        ghe_metrics = evaluate_enhancement(image, ghe_result, "GHE")
        metrics_results.append(ghe_metrics)
        print_metrics(ghe_metrics)

    # Apply CLAHE
    if args.method in ['clahe', 'both']:
        print("\nApplying Contrast Limited Adaptive Histogram Equalization (CLAHE)...")
        tile_grid_size = (args.tile_size, args.tile_size)
        clahe_result = apply_clahe(
            image,
            clip_limit=args.clip_limit,
            tile_grid_size=tile_grid_size,
            color_space=args.color_space
        )
        results['CLAHE'] = clahe_result

        # Save result
        output_path = os.path.join(
            args.output,
            f"{base_name}_clahe_clip{args.clip_limit}_tile{args.tile_size}.png"
        )
        save_image(clahe_result, output_path)
        print(f"Saved CLAHE result to: {output_path}")

        # Evaluate
        clahe_metrics = evaluate_enhancement(image, clahe_result, "CLAHE")
        metrics_results.append(clahe_metrics)
        print_metrics(clahe_metrics)

    # Display results
    if args.show:
        print("\nDisplaying results...")
        images_list = list(results.values())
        titles_list = list(results.keys())

        # Display images
        display_images(
            images_list,
            titles_list,
            figsize=(5 * len(images_list), 5),
            cmap='gray' if args.grayscale else None
        )

        # Display histograms
        plot_histograms(
            images_list,
            [f"{title} Histogram" for title in titles_list],
            colors=['red', 'blue', 'green'][:len(images_list)]
        )

    # Comparison summary
    if len(metrics_results) > 1:
        print("\n" + "="*60)
        print("COMPARISON SUMMARY")
        print("="*60)
        print(f"{'Metric':<25} {'GHE':<15} {'CLAHE':<15}")
        print("-"*60)

        ghe_m = metrics_results[0]
        clahe_m = metrics_results[1]

        print(f"{'PSNR (dB)':<25} {ghe_m['psnr']:<15.2f} {clahe_m['psnr']:<15.2f}")
        print(f"{'SSIM':<25} {ghe_m['ssim']:<15.4f} {clahe_m['ssim']:<15.4f}")
        print(f"{'Entropy (Enhanced)':<25} {ghe_m['entropy_enhanced']:<15.4f} {clahe_m['entropy_enhanced']:<15.4f}")
        print(f"{'Contrast (Enhanced)':<25} {ghe_m['contrast_enhanced']:<15.2f} {clahe_m['contrast_enhanced']:<15.2f}")
        print(f"{'Brightness (Enhanced)':<25} {ghe_m['brightness_enhanced']:<15.2f} {clahe_m['brightness_enhanced']:<15.2f}")
        print("="*60)

    print("\nProcessing complete!")


if __name__ == "__main__":
    main()
