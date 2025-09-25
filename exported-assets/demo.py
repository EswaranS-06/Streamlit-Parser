#!/usr/bin/env python3
"""
Demo script to showcase the log parser functionality
"""

import os
import subprocess
import sys
from pathlib import Path

def check_requirements():
    """Check if required packages are installed"""
    try:
        import streamlit
        import pandas
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def run_log_parser():
    """Run the log parser on sample files"""
    print("\n🔧 Running Log Parser...")
    print("-" * 50)

    try:
        from log_parser import LogParser
        parser = LogParser()
        parser.process_all_logs()
        print("✅ Log parsing completed!")

        # Show results
        oplogs_dir = Path("oplogs")
        if oplogs_dir.exists():
            csv_files = list(oplogs_dir.glob("*.csv"))
            print(f"\n📊 Generated {len(csv_files)} CSV files:")
            for csv_file in csv_files:
                print(f"   • {csv_file.name}")

    except Exception as e:
        print(f"❌ Error running log parser: {e}")

def show_file_structure():
    """Display the current file structure"""
    print("\n📁 Current File Structure:")
    print("-" * 30)

    def print_tree(directory, prefix="", max_depth=2, current_depth=0):
        if current_depth >= max_depth:
            return

        items = sorted(Path(directory).iterdir())
        for i, item in enumerate(items):
            is_last = i == len(items) - 1
            current_prefix = "└── " if is_last else "├── "
            print(f"{prefix}{current_prefix}{item.name}")

            if item.is_dir() and current_depth < max_depth - 1:
                extension = "    " if is_last else "│   "
                print_tree(item, prefix + extension, max_depth, current_depth + 1)

    print_tree(".", max_depth=3)

def main():
    print("🎉 Log Parser Demo")
    print("=" * 50)

    # Check requirements
    if not check_requirements():
        return

    # Show file structure
    show_file_structure()

    # Run log parser
    run_log_parser()

    print("\n🚀 Next Steps:")
    print("-" * 20)
    print("1. Run Streamlit app: streamlit run regex_manager_app.py")
    print("2. Add your own .log files to the 'log/' folder")
    print("3. Create custom regex patterns for your log formats")
    print("4. Run the parser again: python log_parser.py")
    print("\n💡 Check the generated CSV files in the 'oplogs/' folder!")

if __name__ == "__main__":
    main()
