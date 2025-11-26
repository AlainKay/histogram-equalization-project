"""
Contrast Limited Adaptive Histogram Equalization (CLAHE) Implementation
Author: Pragya Mishra

This module implements CLAHE for image enhancement.
CLAHE applies histogram equalization to local regions (tiles) and limits
contrast amplification to prevent noise over-enhancement.
"""

import cv2
import numpy as np
from typing import Tuple


def apply_clahe_grayscale(
    image: np.ndarray,
    clip_limit: float = 2.0,
    tile_grid_size: Tuple[int, int] = (8, 8)
) -> np.ndarray:
    """
    Apply CLAHE to a grayscale image.

    Args:
        image: Input grayscale image (H x W)
        clip_limit: Threshold for contrast limiting (default: 2.0)
        tile_grid_size: Size of grid for histogram equalization (default: 8x8)

    Returns:
        Enhanced grayscale image
    """
    if len(image.shape) != 2:
        raise ValueError("Input must be a grayscale image")

    # Create CLAHE object
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)

    # Apply CLAHE
    enhanced = clahe.apply(image)

    return enhanced


def apply_clahe_color(
    image: np.ndarray,
    clip_limit: float = 2.0,
    tile_grid_size: Tuple[int, int] = (8, 8),
    color_space: str = 'LAB'
) -> np.ndarray:
    """
    Apply CLAHE to a color image.

    Args:
        image: Input BGR color image (H x W x 3)
        clip_limit: Threshold for contrast limiting (default: 2.0)
        tile_grid_size: Size of grid for histogram equalization (default: 8x8)
        color_space: Color space for equalization ('LAB', 'HSV', or 'YCrCb')

    Returns:
        Enhanced BGR color image
    """
    if len(image.shape) != 3 or image.shape[2] != 3:
        raise ValueError("Input must be a BGR color image")

    # Create CLAHE object
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)

    # Convert to appropriate color space
    if color_space == 'LAB':
        img_converted = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        # Apply CLAHE only to the L channel (lightness)
        img_converted[:, :, 0] = clahe.apply(img_converted[:, :, 0])
        # Convert back to BGR
        enhanced = cv2.cvtColor(img_converted, cv2.COLOR_LAB2BGR)

    elif color_space == 'HSV':
        img_converted = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        # Apply CLAHE only to the V channel (value/brightness)
        img_converted[:, :, 2] = clahe.apply(img_converted[:, :, 2])
        # Convert back to BGR
        enhanced = cv2.cvtColor(img_converted, cv2.COLOR_HSV2BGR)

    elif color_space == 'YCrCb':
        img_converted = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
        # Apply CLAHE only to the Y channel (luminance)
        img_converted[:, :, 0] = clahe.apply(img_converted[:, :, 0])
        # Convert back to BGR
        enhanced = cv2.cvtColor(img_converted, cv2.COLOR_YCrCb2BGR)

    else:
        raise ValueError(f"Unsupported color space: {color_space}")

    return enhanced


def apply_clahe(
    image: np.ndarray,
    clip_limit: float = 2.0,
    tile_grid_size: Tuple[int, int] = (8, 8),
    color_space: str = 'LAB'
) -> np.ndarray:
    """
    Apply CLAHE to an image.
    Automatically detects if image is grayscale or color.

    Args:
        image: Input image (grayscale or BGR color)
        clip_limit: Threshold for contrast limiting (default: 2.0)
        tile_grid_size: Size of grid for histogram equalization (default: 8x8)
        color_space: Color space for color images ('LAB', 'HSV', or 'YCrCb')

    Returns:
        Enhanced image
    """
    if len(image.shape) == 2:
        return apply_clahe_grayscale(image, clip_limit, tile_grid_size)
    elif len(image.shape) == 3:
        return apply_clahe_color(image, clip_limit, tile_grid_size, color_space)
    else:
        raise ValueError("Invalid image shape")


def tune_clahe_parameters(
    image: np.ndarray,
    clip_limits: list = [1.0, 2.0, 3.0, 4.0],
    tile_sizes: list = [(4, 4), (8, 8), (16, 16)]
) -> dict:
    """
    Experiment with different CLAHE parameters.

    Args:
        image: Input image
        clip_limits: List of clip limit values to try
        tile_sizes: List of tile grid sizes to try

    Returns:
        Dictionary of results with different parameter combinations
    """
    results = {}

    for clip_limit in clip_limits:
        for tile_size in tile_sizes:
            key = f"clip_{clip_limit}_tile_{tile_size[0]}x{tile_size[1]}"
            enhanced = apply_clahe(image, clip_limit, tile_size)
            results[key] = {
                'image': enhanced,
                'clip_limit': clip_limit,
                'tile_size': tile_size
            }

    return results


if __name__ == "__main__":
    # Test code
    print("CLAHE (Contrast Limited Adaptive Histogram Equalization) module")
    print("This module provides functions for CLAHE image enhancement")
