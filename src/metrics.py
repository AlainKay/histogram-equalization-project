"""
Quantitative Metrics for Image Enhancement
Author: Alain Kariyanga

This module implements reference-based quantitative metrics for evaluating
image enhancement quality by comparing enhanced images to originals.

Metrics:
- PSNR (Peak Signal-to-Noise Ratio)
- SSIM (Structural Similarity Index)
- Entropy (Information Content)
- Contrast (RMS)
- Brightness
"""

import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import peak_signal_noise_ratio as psnr
from typing import Dict

# Import qualitative metrics
try:
    # Try relative import first (when used as package)
    from .qualitative_metrics import (
        calculate_sharpness,
        calculate_naturalness,
        calculate_colorfulness,
        detect_blocking_artifacts,
        detect_over_enhancement
    )
except ImportError:
    # Fall back to direct import (when used as script)
    from qualitative_metrics import (
        calculate_sharpness,
        calculate_naturalness,
        calculate_colorfulness,
        detect_blocking_artifacts,
        detect_over_enhancement
    )


def calculate_psnr(original: np.ndarray, enhanced: np.ndarray) -> float:
    """
    Calculate Peak Signal-to-Noise Ratio (PSNR).
    Higher PSNR indicates better quality.

    Args:
        original: Original image
        enhanced: Enhanced image

    Returns:
        PSNR value in dB
    """
    return psnr(original, enhanced)


def calculate_ssim(original: np.ndarray, enhanced: np.ndarray) -> float:
    """
    Calculate Structural Similarity Index (SSIM).
    SSIM values range from -1 to 1, where 1 indicates perfect similarity.

    Args:
        original: Original image
        enhanced: Enhanced image

    Returns:
        SSIM value
    """
    # Handle grayscale and color images
    if len(original.shape) == 3:
        # For color images, compute SSIM for each channel
        ssim_value = ssim(original, enhanced, channel_axis=2, data_range=255)
    else:
        # For grayscale images
        ssim_value = ssim(original, enhanced, data_range=255)

    return ssim_value


def calculate_entropy(image: np.ndarray) -> float:
    """
    Calculate entropy (information content) of an image.
    Higher entropy indicates more information/detail.

    Args:
        image: Input image

    Returns:
        Entropy value
    """
    # Convert to grayscale if color
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image

    # Calculate histogram
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
    hist = hist.flatten()

    # Normalize histogram to get probability distribution
    hist = hist / hist.sum()

    # Remove zeros to avoid log(0)
    hist = hist[hist > 0]

    # Calculate entropy: -sum(p * log2(p))
    entropy = -np.sum(hist * np.log2(hist))

    return entropy


def calculate_contrast(image: np.ndarray) -> float:
    """
    Calculate RMS (Root Mean Square) contrast.

    Args:
        image: Input image

    Returns:
        RMS contrast value
    """
    # Convert to grayscale if color
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image

    # Calculate RMS contrast
    mean_intensity = np.mean(gray)
    rms_contrast = np.sqrt(np.mean((gray - mean_intensity) ** 2))

    return rms_contrast


def calculate_brightness(image: np.ndarray) -> float:
    """
    Calculate average brightness of an image.

    Args:
        image: Input image

    Returns:
        Average brightness value (0-255)
    """
    # Convert to grayscale if color
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image

    return np.mean(gray)


def evaluate_enhancement(
    original: np.ndarray,
    enhanced: np.ndarray,
    method_name: str = ""
) -> Dict[str, float]:
    """
    Comprehensive evaluation of image enhancement.
    Includes both quantitative (reference-based) and qualitative (perceptual) metrics.

    Args:
        original: Original image
        enhanced: Enhanced image
        method_name: Name of enhancement method (for display)

    Returns:
        Dictionary containing all metrics
    """
    # ========================================================================
    # QUANTITATIVE METRICS (Reference-based)
    # ========================================================================
    metrics = {
        'method': method_name,
        'psnr': calculate_psnr(original, enhanced),
        'ssim': calculate_ssim(original, enhanced),
        'entropy_original': calculate_entropy(original),
        'entropy_enhanced': calculate_entropy(enhanced),
        'contrast_original': calculate_contrast(original),
        'contrast_enhanced': calculate_contrast(enhanced),
        'brightness_original': calculate_brightness(original),
        'brightness_enhanced': calculate_brightness(enhanced)
    }

    # Calculate improvement ratios
    metrics['entropy_improvement'] = (
        metrics['entropy_enhanced'] / metrics['entropy_original']
    )
    metrics['contrast_improvement'] = (
        metrics['contrast_enhanced'] / metrics['contrast_original']
    )

    # ========================================================================
    # QUALITATIVE METRICS (Perceptual, No-reference)
    # ========================================================================

    # Sharpness (calculate for both for comparison)
    metrics['sharpness_original'] = calculate_sharpness(original)
    metrics['sharpness_enhanced'] = calculate_sharpness(enhanced)

    # Naturalness (calculate for both for comparison)
    metrics['naturalness_original'] = calculate_naturalness(original)
    metrics['naturalness_enhanced'] = calculate_naturalness(enhanced)

    # Blocking artifacts (only for enhanced image)
    metrics['blocking_artifacts'] = detect_blocking_artifacts(enhanced)

    # Color metrics (only for color images)
    if len(enhanced.shape) == 3:
        metrics['colorfulness_original'] = calculate_colorfulness(original)
        metrics['colorfulness_enhanced'] = calculate_colorfulness(enhanced)
    else:
        metrics['colorfulness_original'] = 0.0
        metrics['colorfulness_enhanced'] = 0.0

    # Over-enhancement detection (hybrid: uses reference for comparison)
    over_enh = detect_over_enhancement(original, enhanced)
    metrics.update({
        'over_enhancement_detected': over_enh['is_over_enhanced'],
        'brightness_change': over_enh['brightness_change_ratio'],
        'contrast_change': over_enh['contrast_change_ratio'],
        'saturation_ratio': over_enh['saturation_ratio']
    })

    return metrics


def print_metrics(metrics: Dict[str, float]) -> None:
    """
    Print metrics in a formatted way.

    Args:
        metrics: Dictionary of metrics from evaluate_enhancement
    """
    print(f"\n{'='*70}")
    print(f"Enhancement Evaluation: {metrics['method']}")
    print(f"{'='*70}")

    # ========================================================================
    # QUANTITATIVE METRICS (Reference-based)
    # ========================================================================
    print(f"\n{'QUANTITATIVE METRICS (Reference-based)':^70}")
    print(f"{'-'*70}")
    print(f"PSNR: {metrics['psnr']:.2f} dB (higher is better)")
    print(f"SSIM: {metrics['ssim']:.4f} (closer to 1.0 is better)")

    print(f"\nEntropy (Information Content):")
    print(f"  Original: {metrics['entropy_original']:.4f}")
    print(f"  Enhanced: {metrics['entropy_enhanced']:.4f}")
    print(f"  Improvement: {metrics['entropy_improvement']:.2%}")

    print(f"\nContrast (RMS):")
    print(f"  Original: {metrics['contrast_original']:.2f}")
    print(f"  Enhanced: {metrics['contrast_enhanced']:.2f}")
    print(f"  Improvement: {metrics['contrast_improvement']:.2%}")

    print(f"\nBrightness:")
    print(f"  Original: {metrics['brightness_original']:.2f}")
    print(f"  Enhanced: {metrics['brightness_enhanced']:.2f}")
    print(f"  Change: {metrics['brightness_change']:.2%}")

    # ========================================================================
    # QUALITATIVE METRICS (Perceptual Quality)
    # ========================================================================
    print(f"\n{'QUALITATIVE METRICS (Perceptual Quality)':^70}")
    print(f"{'-'*70}")

    print(f"Sharpness (Laplacian Variance):")
    print(f"  Original: {metrics['sharpness_original']:.2f}")
    print(f"  Enhanced: {metrics['sharpness_enhanced']:.2f}")

    print(f"\nNaturalness (0-1, higher is better):")
    print(f"  Original: {metrics['naturalness_original']:.4f}")
    print(f"  Enhanced: {metrics['naturalness_enhanced']:.4f}")

    if metrics['colorfulness_enhanced'] > 0:
        print(f"\nColorfulness:")
        print(f"  Original: {metrics['colorfulness_original']:.2f}")
        print(f"  Enhanced: {metrics['colorfulness_enhanced']:.2f}")

    print(f"\nBlocking Artifacts: {metrics['blocking_artifacts']:.4f} (lower is better)")
    print(f"Saturation Ratio: {metrics['saturation_ratio']:.4f} (lower is better)")

    # ========================================================================
    # QUALITY ASSESSMENT
    # ========================================================================
    print(f"\n{'QUALITY ASSESSMENT':^70}")
    print(f"{'-'*70}")
    if metrics['over_enhancement_detected']:
        print(f"⚠ WARNING: Over-enhancement detected!")
        print(f"  - Brightness change: {metrics['brightness_change']:.2%}")
        print(f"  - Contrast change: {metrics['contrast_change']:.2%}")
        print(f"  - Saturation: {metrics['saturation_ratio']:.2%}")
    else:
        print(f"✓ Enhancement appears natural (no over-enhancement detected)")

    print(f"{'='*70}\n")


if __name__ == "__main__":
    print("Image Enhancement Evaluation Metrics module")
    print("Provides PSNR, SSIM, Entropy, Contrast, and Brightness metrics")
    print("Also integrates qualitative/perceptual metrics from qualitative_metrics.py")
