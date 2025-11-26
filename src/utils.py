"""
Utility Functions
Authors: Alain Kariyanga & Pragya Mishra

Common utility functions for image processing and visualization.
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple
import os


def load_image(path: str, grayscale: bool = False) -> np.ndarray:
    """
    Load an image from file.

    Args:
        path: Path to image file
        grayscale: If True, load as grayscale

    Returns:
        Image as numpy array
    """
    if grayscale:
        image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    else:
        image = cv2.imread(path, cv2.IMREAD_COLOR)

    if image is None:
        raise FileNotFoundError(f"Could not load image from {path}")

    return image


def save_image(image: np.ndarray, path: str) -> None:
    """
    Save an image to file.

    Args:
        image: Image as numpy array
        path: Output path
    """
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(path), exist_ok=True)

    success = cv2.imwrite(path, image)
    if not success:
        raise IOError(f"Failed to save image to {path}")


def display_images(
    images: List[np.ndarray],
    titles: List[str],
    figsize: Tuple[int, int] = (15, 5),
    cmap: str = None
) -> None:
    """
    Display multiple images side by side.

    Args:
        images: List of images to display
        titles: List of titles for each image
        figsize: Figure size
        cmap: Colormap (use 'gray' for grayscale images)
    """
    n = len(images)
    fig, axes = plt.subplots(1, n, figsize=figsize)

    if n == 1:
        axes = [axes]

    for ax, img, title in zip(axes, images, titles):
        # Convert BGR to RGB for display if color image
        if len(img.shape) == 3:
            img_display = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            ax.imshow(img_display)
        else:
            ax.imshow(img, cmap=cmap or 'gray')

        ax.set_title(title)
        ax.axis('off')

    plt.tight_layout()
    plt.show()


def plot_histograms(
    images: List[np.ndarray],
    titles: List[str],
    colors: List[str] = None,
    figsize: Tuple[int, int] = (15, 4)
) -> None:
    """
    Plot histograms for multiple images.

    Args:
        images: List of images
        titles: List of titles
        colors: List of colors for each histogram
        figsize: Figure size
    """
    n = len(images)
    fig, axes = plt.subplots(1, n, figsize=figsize)

    if n == 1:
        axes = [axes]

    if colors is None:
        colors = ['blue'] * n

    for ax, img, title, color in zip(axes, images, titles, colors):
        # Convert to grayscale if color
        if len(img.shape) == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray = img

        # Calculate histogram
        hist = cv2.calcHist([gray], [0], None, [256], [0, 256])

        ax.plot(hist, color=color)
        ax.set_title(title)
        ax.set_xlabel('Pixel Intensity')
        ax.set_ylabel('Frequency')
        ax.set_xlim([0, 256])
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


def create_comparison_grid(
    original: np.ndarray,
    enhanced_dict: dict,
    figsize: Tuple[int, int] = (15, 10)
) -> None:
    """
    Create a grid comparing original with multiple enhanced versions.

    Args:
        original: Original image
        enhanced_dict: Dictionary of {method_name: enhanced_image}
        figsize: Figure size
    """
    n_methods = len(enhanced_dict)
    n_rows = (n_methods + 2) // 3  # +2 for original and rounding up
    n_cols = min(3, n_methods + 1)

    fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
    axes = axes.flatten() if n_methods > 1 else [axes]

    # Display original
    if len(original.shape) == 3:
        original_rgb = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
        axes[0].imshow(original_rgb)
    else:
        axes[0].imshow(original, cmap='gray')
    axes[0].set_title('Original')
    axes[0].axis('off')

    # Display enhanced versions
    for idx, (method, enhanced) in enumerate(enhanced_dict.items(), 1):
        if len(enhanced.shape) == 3:
            enhanced_rgb = cv2.cvtColor(enhanced, cv2.COLOR_BGR2RGB)
            axes[idx].imshow(enhanced_rgb)
        else:
            axes[idx].imshow(enhanced, cmap='gray')
        axes[idx].set_title(method)
        axes[idx].axis('off')

    # Hide unused subplots
    for idx in range(n_methods + 1, len(axes)):
        axes[idx].axis('off')

    plt.tight_layout()
    plt.show()


def get_sample_images() -> List[str]:
    """
    Get list of sample image paths from data/input directory.

    Returns:
        List of image file paths
    """
    input_dir = 'data/input'
    if not os.path.exists(input_dir):
        return []

    valid_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff'}
    images = []

    for filename in os.listdir(input_dir):
        ext = os.path.splitext(filename)[1].lower()
        if ext in valid_extensions:
            images.append(os.path.join(input_dir, filename))

    return sorted(images)


if __name__ == "__main__":
    print("Utility functions for image processing and visualization")
