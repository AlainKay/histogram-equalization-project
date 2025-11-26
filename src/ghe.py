"""
Global Histogram Equalization (GHE) Implementation
Author: Alain Kariyanga

This module implements Global Histogram Equalization for image enhancement.
GHE redistributes pixel intensity values globally using the cumulative
distribution function (CDF) to enhance contrast.
"""

import cv2
import numpy as np
from typing import Tuple


def apply_ghe_grayscale(image: np.ndarray) -> np.ndarray:
    """
    Apply Global Histogram Equalization to a grayscale image.

    Args:
        image: Input grayscale image (H x W)

    Returns:
        Enhanced grayscale image
    """
    if len(image.shape) != 2:
        raise ValueError("Input must be a grayscale image")

    # Apply histogram equalization
    equalized = cv2.equalizeHist(image)

    return equalized


def apply_ghe_color(image: np.ndarray, color_space: str = 'YCrCb') -> np.ndarray:
    """
    Apply Global Histogram Equalization to a color image.

    Args:
        image: Input BGR color image (H x W x 3)
        color_space: Color space for equalization ('YCrCb', 'HSV', or 'LAB')

    Returns:
        Enhanced BGR color image
    """
    if len(image.shape) != 3 or image.shape[2] != 3:
        raise ValueError("Input must be a BGR color image")

    # Convert to appropriate color space
    if color_space == 'YCrCb':
        img_converted = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
        # Equalize only the Y channel (luminance)
        img_converted[:, :, 0] = cv2.equalizeHist(img_converted[:, :, 0])
        # Convert back to BGR
        equalized = cv2.cvtColor(img_converted, cv2.COLOR_YCrCb2BGR)

    elif color_space == 'HSV':
        img_converted = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        # Equalize only the V channel (value/brightness)
        img_converted[:, :, 2] = cv2.equalizeHist(img_converted[:, :, 2])
        # Convert back to BGR
        equalized = cv2.cvtColor(img_converted, cv2.COLOR_HSV2BGR)

    elif color_space == 'LAB':
        img_converted = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        # Equalize only the L channel (lightness)
        img_converted[:, :, 0] = cv2.equalizeHist(img_converted[:, :, 0])
        # Convert back to BGR
        equalized = cv2.cvtColor(img_converted, cv2.COLOR_LAB2BGR)

    else:
        raise ValueError(f"Unsupported color space: {color_space}")

    return equalized


def apply_ghe(image: np.ndarray, color_space: str = 'YCrCb') -> np.ndarray:
    """
    Apply Global Histogram Equalization to an image.
    Automatically detects if image is grayscale or color.

    Args:
        image: Input image (grayscale or BGR color)
        color_space: Color space for color images ('YCrCb', 'HSV', or 'LAB')

    Returns:
        Enhanced image
    """
    if len(image.shape) == 2:
        return apply_ghe_grayscale(image)
    elif len(image.shape) == 3:
        return apply_ghe_color(image, color_space)
    else:
        raise ValueError("Invalid image shape")


def compute_histogram(image: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Compute histogram of grayscale image.

    Args:
        image: Grayscale image

    Returns:
        Tuple of (histogram values, bin edges)
    """
    hist = cv2.calcHist([image], [0], None, [256], [0, 256])
    return hist.flatten(), np.arange(257)


def compute_cdf(histogram: np.ndarray) -> np.ndarray:
    """
    Compute cumulative distribution function from histogram.

    Args:
        histogram: Histogram values

    Returns:
        Normalized CDF
    """
    cdf = histogram.cumsum()
    cdf_normalized = cdf / cdf[-1]  # Normalize to [0, 1]
    return cdf_normalized


if __name__ == "__main__":
    # Test code
    print("Global Histogram Equalization module")
    print("This module provides functions for GHE image enhancement")
