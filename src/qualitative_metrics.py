"""
Qualitative/Perceptual Metrics for Image Enhancement
Author: Alain Kariyanga

This module implements no-reference quality metrics that assess perceptual
aspects of image quality without needing the original image as reference.

Metrics:
- Sharpness (Laplacian variance)
- Naturalness (histogram-based)
- Colorfulness (Hasler & Süsstrunk method)
- Blocking artifacts detection
- Over-enhancement detection
"""

import cv2
import numpy as np
from typing import Dict


def calculate_sharpness(image: np.ndarray) -> float:
    """
    Calculate image sharpness using Laplacian variance.
    Higher values indicate sharper images.

    Args:
        image: Input image

    Returns:
        Sharpness score (higher = sharper)
    """
    # Convert to grayscale if color
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image

    # Calculate Laplacian variance
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    sharpness = laplacian.var()

    return sharpness


def calculate_colorfulness(image: np.ndarray) -> float:
    """
    Calculate colorfulness metric (Hasler and Süsstrunk method).
    Higher values indicate more colorful images.

    Reference: "Measuring Colourfulness in Natural Images" (2003)

    Args:
        image: Input BGR color image

    Returns:
        Colorfulness score (0-100+, higher = more colorful)
    """
    if len(image.shape) != 3:
        return 0.0  # Grayscale image has no color

    # Split into BGR channels
    B, G, R = cv2.split(image.astype(np.float32))

    # Compute rg = R - G
    rg = R - G

    # Compute yb = 0.5 * (R + G) - B
    yb = 0.5 * (R + G) - B

    # Compute standard deviations and means
    std_rg = np.std(rg)
    std_yb = np.std(yb)

    mean_rg = np.mean(rg)
    mean_yb = np.mean(yb)

    # Compute colorfulness metric
    std_root = np.sqrt(std_rg**2 + std_yb**2)
    mean_root = np.sqrt(mean_rg**2 + mean_yb**2)

    colorfulness = std_root + 0.3 * mean_root

    return colorfulness


def calculate_naturalness(image: np.ndarray) -> float:
    """
    Calculate naturalness score based on histogram distribution.
    Natural images have specific statistical properties.

    Args:
        image: Input image

    Returns:
        Naturalness score (0-1, higher = more natural)
    """
    # Convert to grayscale
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image

    # Calculate histogram
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256]).flatten()
    hist = hist / hist.sum()  # Normalize

    # Natural images tend to have:
    # 1. Not too uniform (entropy check)
    entropy = -np.sum(hist[hist > 0] * np.log2(hist[hist > 0]))
    entropy_score = min(entropy / 8.0, 1.0)  # Normalize to [0, 1]

    # 2. Gradual distribution (not too spiky)
    hist_smooth = np.convolve(hist, np.ones(5)/5, mode='same')
    smoothness = 1.0 - np.mean(np.abs(hist - hist_smooth))

    # 3. Moderate contrast (not too flat, not too peaked)
    std = np.std(gray)
    contrast_score = min(std / 64.0, 1.0)  # Normalize

    # Combine scores
    naturalness = (entropy_score * 0.4 + smoothness * 0.3 + contrast_score * 0.3)

    return naturalness


def detect_blocking_artifacts(image: np.ndarray, block_size: int = 8) -> float:
    """
    Detect blocking artifacts (common in CLAHE with large tile sizes).

    Args:
        image: Input image
        block_size: Size of blocks to check

    Returns:
        Blocking artifact score (0-1, lower = fewer artifacts)
    """
    # Convert to grayscale
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image

    # Calculate horizontal and vertical gradients at block boundaries
    h, w = gray.shape
    blocking_score = 0.0
    count = 0

    # Check horizontal boundaries
    for i in range(block_size, h, block_size):
        if i < h - 1:
            diff = np.abs(gray[i, :].astype(float) - gray[i-1, :].astype(float))
            blocking_score += np.mean(diff)
            count += 1

    # Check vertical boundaries
    for j in range(block_size, w, block_size):
        if j < w - 1:
            diff = np.abs(gray[:, j].astype(float) - gray[:, j-1].astype(float))
            blocking_score += np.mean(diff)
            count += 1

    if count > 0:
        blocking_score /= count

    # Normalize to [0, 1]
    blocking_score = min(blocking_score / 20.0, 1.0)

    return blocking_score


def detect_over_enhancement(original: np.ndarray, enhanced: np.ndarray) -> Dict[str, float]:
    """
    Detect over-enhancement artifacts by comparing original and enhanced images.

    Note: This is a hybrid metric - uses original as reference but detects
    qualitative issues (unnatural appearance, saturation, etc.)

    Args:
        original: Original image
        enhanced: Enhanced image

    Returns:
        Dictionary with over-enhancement indicators
    """
    # Helper function for brightness
    def get_brightness(img):
        if len(img.shape) == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray = img
        return np.mean(gray)

    # Helper function for contrast
    def get_contrast(img):
        if len(img.shape) == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray = img
        mean_intensity = np.mean(gray)
        return np.sqrt(np.mean((gray - mean_intensity) ** 2))

    # Calculate brightness change
    brightness_orig = get_brightness(original)
    brightness_enh = get_brightness(enhanced)
    brightness_change = abs(brightness_enh - brightness_orig) / brightness_orig

    # Calculate contrast change
    contrast_orig = get_contrast(original)
    contrast_enh = get_contrast(enhanced)
    contrast_change = (contrast_enh - contrast_orig) / contrast_orig if contrast_orig > 0 else 0

    # Check for histogram clipping (saturation)
    if len(enhanced.shape) == 3:
        gray_enh = cv2.cvtColor(enhanced, cv2.COLOR_BGR2GRAY)
    else:
        gray_enh = enhanced

    saturated_pixels = np.sum((gray_enh <= 5) | (gray_enh >= 250))
    saturation_ratio = saturated_pixels / gray_enh.size

    # Check for unnatural contrast (gradient analysis)
    grad_x = cv2.Sobel(gray_enh, cv2.CV_64F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(gray_enh, cv2.CV_64F, 0, 1, ksize=3)
    gradient_magnitude = np.sqrt(grad_x**2 + grad_y**2)
    edge_strength = np.mean(gradient_magnitude)

    return {
        'brightness_change_ratio': brightness_change,
        'contrast_change_ratio': contrast_change,
        'saturation_ratio': saturation_ratio,
        'edge_strength': edge_strength,
        'is_over_enhanced': (brightness_change > 0.3 or
                            contrast_change > 2.0 or
                            saturation_ratio > 0.05)
    }


def evaluate_perceptual_quality(
    image: np.ndarray,
    original: np.ndarray = None
) -> Dict[str, float]:
    """
    Evaluate perceptual quality of an image using no-reference metrics.

    Args:
        image: Image to evaluate
        original: Optional original image for comparison metrics

    Returns:
        Dictionary of perceptual quality metrics
    """
    metrics = {
        'sharpness': calculate_sharpness(image),
        'naturalness': calculate_naturalness(image),
        'blocking_artifacts': detect_blocking_artifacts(image)
    }

    # Add color metrics for color images
    if len(image.shape) == 3:
        metrics['colorfulness'] = calculate_colorfulness(image)
    else:
        metrics['colorfulness'] = 0.0

    # Add over-enhancement detection if original is provided
    if original is not None:
        over_enh = detect_over_enhancement(original, image)
        metrics.update({
            'over_enhancement_detected': over_enh['is_over_enhanced'],
            'brightness_change': over_enh['brightness_change_ratio'],
            'contrast_change': over_enh['contrast_change_ratio'],
            'saturation_ratio': over_enh['saturation_ratio']
        })

    return metrics


if __name__ == "__main__":
    print("Qualitative/Perceptual Image Quality Metrics module")
    print("Provides no-reference quality assessment metrics")
