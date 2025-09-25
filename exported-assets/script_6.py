# Create a simple usage example script
usage_example = '''#!/usr/bin/env python3
"""
Simple usage example for the log parser system
"""

def main():
    print("🚀 Log Parser System Usage Example")
    print("=" * 50)
    
    print("\\n1. 📝 First, manage your regex patterns:")
    print("   streamlit run regex_manager_app.py")
    print("   - Add new patterns for your specific log formats")
    print("   - Test patterns with sample data")
    print("   - View and edit existing patterns")
    
    print("\\n2. 📁 Place your log files:")
    print("   - Put all .log files in the 'log/' folder")
    print("   - Supported formats: Apache, Nginx, Syslog, Firewall, Custom")
    
    print("\\n3. 🔧 Run the parser:")
    print("   python log_parser.py")
    print("   - Automatically detects log types")
    print("   - Applies appropriate regex patterns") 
    print("   - Extracts IP, timestamp, message + other fields")
    print("   - Saves results as CSV files in 'oplogs/' folder")
    
    print("\\n4. 📊 Analyze results:")
    print("   - Open CSV files in Excel, Pandas, or any data analysis tool")
    print("   - Each CSV contains structured data from the corresponding log file")
    
    print("\\n💡 Tips:")
    print("   - Test your regex patterns before processing large files")
    print("   - Use the Streamlit app to experiment with different patterns")
    print("   - Check the generated CSV files to verify parsing accuracy")
    
    print("\\n🔍 Example workflow:")
    print("   1. Add custom_log.log to log/ folder")
    print("   2. Open Streamlit app and create regex pattern for your format")
    print("   3. Test the pattern with sample lines from your log")
    print("   4. Save the pattern with a descriptive key name")
    print("   5. Run python log_parser.py to process all files")
    print("   6. Find parsed results in oplogs/custom_log.csv")

if __name__ == "__main__":
    main()
'''

with open('usage_example.py', 'w') as f:
    f.write(usage_example)

print("Created usage_example.py")

# Display the final file structure
print("\\n📁 Final Project Structure:")
print("=" * 40)

import os
from pathlib import Path

def display_tree(directory, prefix="", max_files=15, file_count=[0]):
    """Display directory tree with file count limit"""
    if file_count[0] >= max_files:
        return
        
    try:
        items = sorted(Path(directory).iterdir())
        for i, item in enumerate(items):
            if file_count[0] >= max_files:
                print(f"{prefix}└── ... (more files)")
                break
                
            is_last = i == len(items) - 1
            current_prefix = "└── " if is_last else "├── "
            print(f"{prefix}{current_prefix}{item.name}")
            file_count[0] += 1
            
            if item.is_dir() and file_count[0] < max_files:
                extension = "    " if is_last else "│   "
                display_tree(item, prefix + extension, max_files, file_count)
    except PermissionError:
        pass

display_tree(".")

print(f"\\n✅ Complete log parsing system created!")
print(f"Total files and folders: {len(list(Path('.').rglob('*')))}")