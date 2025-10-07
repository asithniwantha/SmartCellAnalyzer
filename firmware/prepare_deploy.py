# Deployment Script for MicroPython
# This script helps prepare files for uploading to Pico

import shutil
import os

def prepare_deployment(source_dir, deploy_dir):
    """
    Copy files from structured source to flat deployment directory.
    
    Args:
        source_dir: Path to firmware/src directory
        deploy_dir: Path to deployment directory
    """
    
    # Create deployment directory
    os.makedirs(deploy_dir, exist_ok=True)
    
    # Files to copy from controllers
    controllers = [
        'src/controllers/battery_charger_controller.py'
    ]
    
    # Files to copy from drivers
    drivers = [
        'src/drivers/ina3221_wrapper.py',
        'src/drivers/adafruit_ina3221.py',
        'src/drivers/pca9685.py'
    ]
    
    # Other files
    other = [
        'main.py',
        'boot.py',
        'src/config.py'
    ]
    
    # Copy all files
    all_files = controllers + drivers + other
    
    print("Preparing deployment files...")
    for file in all_files:
        src_path = os.path.join(source_dir, file)
        if os.path.exists(src_path):
            dest_name = os.path.basename(file)
            dest_path = os.path.join(deploy_dir, dest_name)
            shutil.copy2(src_path, dest_path)
            print(f"  ✓ Copied {file} -> {dest_name}")
        else:
            print(f"  ✗ Warning: {file} not found")
    
    print(f"\nDeployment files ready in: {deploy_dir}")
    print("\nUpload these files to your Pico:")
    for file in os.listdir(deploy_dir):
        print(f"  - {file}")

if __name__ == "__main__":
    import sys
    
    # Adjust these paths as needed
    firmware_dir = os.path.dirname(os.path.abspath(__file__))
    deploy_dir = os.path.join(firmware_dir, "deploy")
    
    prepare_deployment(firmware_dir, deploy_dir)
