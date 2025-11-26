"""
Test script to verify the installation and setup.
Run this to make sure all dependencies are installed correctly.
"""

import sys

def test_imports():
    """Test if all required packages can be imported."""
    print("Testing package imports...")

    packages = {
        'cv2': 'OpenCV',
        'numpy': 'NumPy',
        'matplotlib': 'Matplotlib',
        'seaborn': 'Seaborn',
        'pandas': 'Pandas',
        'skimage': 'scikit-image',
        'scipy': 'SciPy',
        'PIL': 'Pillow'
    }

    failed = []

    for package, name in packages.items():
        try:
            __import__(package)
            print(f"✓ {name} imported successfully")
        except ImportError as e:
            print(f"✗ {name} import failed: {e}")
            failed.append(name)

    if failed:
        print(f"\n{len(failed)} package(s) failed to import: {', '.join(failed)}")
        return False
    else:
        print("\nAll packages imported successfully!")
        return True


def test_project_modules():
    """Test if project modules can be imported."""
    print("\nTesting project modules...")

    sys.path.insert(0, 'src')

    modules = ['ghe', 'clahe', 'metrics', 'utils']
    failed = []

    for module in modules:
        try:
            __import__(module)
            print(f"✓ {module}.py imported successfully")
        except ImportError as e:
            print(f"✗ {module}.py import failed: {e}")
            failed.append(module)

    if failed:
        print(f"\n{len(failed)} module(s) failed to import: {', '.join(failed)}")
        return False
    else:
        print("\nAll project modules imported successfully!")
        return True


def test_opencv_version():
    """Check OpenCV version and capabilities."""
    print("\nChecking OpenCV...")
    import cv2
    print(f"OpenCV version: {cv2.__version__}")

    # Test CLAHE availability
    try:
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        print("✓ CLAHE functionality available")
    except Exception as e:
        print(f"✗ CLAHE test failed: {e}")
        return False

    return True


def create_test_image():
    """Create a simple test image and apply transformations."""
    print("\nCreating and processing test image...")

    try:
        import numpy as np
        import cv2

        # Create a simple gradient image
        test_image = np.zeros((256, 256), dtype=np.uint8)
        for i in range(256):
            test_image[i, :] = i

        # Test GHE
        ghe_result = cv2.equalizeHist(test_image)
        print("✓ GHE applied successfully")

        # Test CLAHE
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        clahe_result = clahe.apply(test_image)
        print("✓ CLAHE applied successfully")

        print(f"Test image shape: {test_image.shape}")
        print(f"GHE result shape: {ghe_result.shape}")
        print(f"CLAHE result shape: {clahe_result.shape}")

        return True

    except Exception as e:
        print(f"✗ Image processing test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("="*60)
    print("Histogram Equalization Project - Setup Test")
    print("="*60)

    results = []

    # Test imports
    results.append(test_imports())

    # Test project modules
    results.append(test_project_modules())

    # Test OpenCV
    results.append(test_opencv_version())

    # Test image processing
    results.append(create_test_image())

    # Summary
    print("\n" + "="*60)
    if all(results):
        print("SUCCESS! All tests passed. Setup is complete.")
        print("\nYou can now:")
        print("1. Add images to data/input/")
        print("2. Run: python src/main.py --input data/input/your_image.jpg --method both --show")
        print("3. Or use the Jupyter notebook: notebooks/experiments.ipynb")
    else:
        print("FAILED! Some tests did not pass. Please check the errors above.")
    print("="*60)


if __name__ == "__main__":
    main()
