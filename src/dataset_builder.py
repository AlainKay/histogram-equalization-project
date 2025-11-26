"""
Dataset Builder for Histogram Equalization Project
Authors: Alain Kariyanga & Pragya Mishra

This script fetches images from various sources to build a comprehensive
test dataset for evaluating GHE and CLAHE methods.
"""

import requests
import cv2
import numpy as np
from pathlib import Path
import time
from typing import List, Dict
import json


class DatasetBuilder:
    """Build a curated dataset for histogram equalization testing."""

    def __init__(self, save_dir: str = "data/input"):
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(parents=True, exist_ok=True)
        self.metadata = []

    def fetch_from_unsplash(
        self,
        access_key: str,
        queries: List[str],
        per_query: int = 3
    ) -> None:
        """
        Fetch images from Unsplash API.

        Args:
            access_key: Your Unsplash API access key
            queries: List of search queries
            per_query: Number of images per query
        """
        print("Fetching from Unsplash API...")
        url = "https://api.unsplash.com/search/photos"

        for query in queries:
            print(f"\nSearching for: '{query}'")

            params = {
                'query': query,
                'client_id': access_key,
                'per_page': per_query,
                'orientation': 'landscape'  # Better for visualization
            }

            try:
                response = requests.get(url, params=params)
                response.raise_for_status()
                data = response.json()

                if 'results' not in data:
                    print(f"No results found for '{query}'")
                    continue

                for idx, photo in enumerate(data['results']):
                    try:
                        # Get image URL
                        img_url = photo['urls']['regular']

                        # Download image
                        img_response = requests.get(img_url, timeout=10)
                        img_response.raise_for_status()

                        # Convert to numpy array
                        nparr = np.frombuffer(img_response.content, np.uint8)
                        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

                        if img is None:
                            print(f"Failed to decode image {idx+1}")
                            continue

                        # Create filename
                        category = query.replace(' ', '_').lower()
                        filename = f"{category}_{idx+1:02d}.jpg"
                        filepath = self.save_dir / filename

                        # Save image
                        cv2.imwrite(str(filepath), img)

                        # Save metadata
                        self.metadata.append({
                            'filename': filename,
                            'category': category,
                            'source': 'unsplash',
                            'query': query,
                            'photographer': photo['user']['name'],
                            'url': photo['links']['html'],
                            'dimensions': f"{img.shape[1]}x{img.shape[0]}"
                        })

                        print(f"  ✓ Saved: {filename}")

                    except Exception as e:
                        print(f"  ✗ Error downloading image {idx+1}: {e}")

                    # Be nice to the API
                    time.sleep(0.5)

            except requests.exceptions.RequestException as e:
                print(f"Error with query '{query}': {e}")

            # Respect rate limits
            time.sleep(1)

    def fetch_from_pexels(
        self,
        api_key: str,
        queries: List[str],
        per_query: int = 3
    ) -> None:
        """
        Fetch images from Pexels API.

        Args:
            api_key: Your Pexels API key
            queries: List of search queries
            per_query: Number of images per query
        """
        print("Fetching from Pexels API...")
        url = "https://api.pexels.com/v1/search"
        headers = {'Authorization': api_key}

        for query in queries:
            print(f"\nSearching for: '{query}'")

            params = {
                'query': query,
                'per_page': per_query,
                'orientation': 'landscape'
            }

            try:
                response = requests.get(url, headers=headers, params=params)
                response.raise_for_status()
                data = response.json()

                if 'photos' not in data or len(data['photos']) == 0:
                    print(f"No results found for '{query}'")
                    continue

                for idx, photo in enumerate(data['photos']):
                    try:
                        # Get image URL
                        img_url = photo['src']['large']

                        # Download image
                        img_response = requests.get(img_url, timeout=10)
                        img_response.raise_for_status()

                        # Convert to numpy array
                        nparr = np.frombuffer(img_response.content, np.uint8)
                        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

                        if img is None:
                            print(f"Failed to decode image {idx+1}")
                            continue

                        # Create filename
                        category = query.replace(' ', '_').lower()
                        filename = f"{category}_{idx+1:02d}_pexels.jpg"
                        filepath = self.save_dir / filename

                        # Save image
                        cv2.imwrite(str(filepath), img)

                        # Save metadata
                        self.metadata.append({
                            'filename': filename,
                            'category': category,
                            'source': 'pexels',
                            'query': query,
                            'photographer': photo['photographer'],
                            'url': photo['url'],
                            'dimensions': f"{img.shape[1]}x{img.shape[0]}"
                        })

                        print(f"  ✓ Saved: {filename}")

                    except Exception as e:
                        print(f"  ✗ Error downloading image {idx+1}: {e}")

                    time.sleep(0.5)

            except requests.exceptions.RequestException as e:
                print(f"Error with query '{query}': {e}")

            time.sleep(1)

    def download_standard_datasets(self) -> None:
        """Download standard test images (no API needed)."""
        print("\nDownloading standard test images...")

        # Standard test images from public sources
        standard_images = {
            'lena': 'https://upload.wikimedia.org/wikipedia/en/7/7d/Lenna_%28test_image%29.png',
            'baboon': 'https://homepages.cae.wisc.edu/~ece533/images/baboon.png',
            'peppers': 'https://homepages.cae.wisc.edu/~ece533/images/peppers.png',
        }

        for name, url in standard_images.items():
            try:
                print(f"Downloading {name}...")
                response = requests.get(url, timeout=10)
                response.raise_for_status()

                nparr = np.frombuffer(response.content, np.uint8)
                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

                if img is not None:
                    filename = f"standard_{name}.png"
                    filepath = self.save_dir / filename
                    cv2.imwrite(str(filepath), img)

                    self.metadata.append({
                        'filename': filename,
                        'category': 'standard_test',
                        'source': 'public_domain',
                        'query': name,
                        'photographer': 'N/A',
                        'url': url,
                        'dimensions': f"{img.shape[1]}x{img.shape[0]}"
                    })

                    print(f"  ✓ Saved: {filename}")
                else:
                    print(f"  ✗ Failed to decode {name}")

            except Exception as e:
                print(f"  ✗ Error downloading {name}: {e}")

            time.sleep(0.5)

    def save_metadata(self, filename: str = "dataset_metadata.json") -> None:
        """Save metadata about the dataset."""
        metadata_path = self.save_dir / filename

        with open(metadata_path, 'w') as f:
            json.dump({
                'total_images': len(self.metadata),
                'images': self.metadata
            }, f, indent=2)

        print(f"\n✓ Metadata saved to: {metadata_path}")

    def print_summary(self) -> None:
        """Print dataset summary."""
        print("\n" + "="*60)
        print("DATASET SUMMARY")
        print("="*60)
        print(f"Total images downloaded: {len(self.metadata)}")

        # Count by category
        categories = {}
        for item in self.metadata:
            cat = item['category']
            categories[cat] = categories.get(cat, 0) + 1

        print("\nImages by category:")
        for cat, count in sorted(categories.items()):
            print(f"  {cat}: {count}")

        # Count by source
        sources = {}
        for item in self.metadata:
            src = item['source']
            sources[src] = sources.get(src, 0) + 1

        print("\nImages by source:")
        for src, count in sorted(sources.items()):
            print(f"  {src}: {count}")

        print("="*60)


def main():
    """Main function to build the dataset."""

    # Initialize builder
    builder = DatasetBuilder(save_dir="data/input")

    # Define search queries optimized for histogram equalization testing
    queries = [
        # Low contrast scenarios
        "foggy landscape",
        "misty mountain",
        "overcast sky",

        # Underexposed scenarios
        "dark portrait",
        "low light interior",
        "night street",

        # Backlit scenarios
        "backlit silhouette",
        "sunset portrait",

        # High contrast scenarios
        "bright sunlight shadow",
        "indoor window light",

        # Medical-like scenarios
        "xray aesthetic",
        "monochrome texture",
    ]

    print("="*60)
    print("HISTOGRAM EQUALIZATION DATASET BUILDER")
    print("="*60)

    # Option 1: Using Unsplash (RECOMMENDED)
    print("\n[OPTION 1] Using Unsplash API")
    print("Get your free API key at: https://unsplash.com/developers")
    unsplash_key = input("Enter your Unsplash Access Key (or press Enter to skip): ").strip()

    if unsplash_key:
        builder.fetch_from_unsplash(
            access_key=unsplash_key,
            queries=queries,
            per_query=2  # 2 images per query
        )
    else:
        print("Skipping Unsplash...")

    # Option 2: Using Pexels (ALTERNATIVE)
    print("\n[OPTION 2] Using Pexels API")
    print("Get your free API key at: https://www.pexels.com/api/")
    pexels_key = input("Enter your Pexels API Key (or press Enter to skip): ").strip()

    if pexels_key:
        builder.fetch_from_pexels(
            api_key=pexels_key,
            queries=queries[:5],  # Fewer queries
            per_query=2
        )
    else:
        print("Skipping Pexels...")

    # Option 3: Download standard test images (NO API NEEDED)
    print("\n[OPTION 3] Downloading standard test images (no API needed)")
    download_standard = input("Download standard test images? (y/n): ").strip().lower()

    if download_standard == 'y':
        builder.download_standard_datasets()

    # Save metadata and print summary
    if builder.metadata:
        builder.save_metadata()
        builder.print_summary()
        print("\n✓ Dataset ready! Images saved to: data/input/")
    else:
        print("\n✗ No images were downloaded. Please provide at least one API key.")


if __name__ == "__main__":
    main()
