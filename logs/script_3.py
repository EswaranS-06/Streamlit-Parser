# Create a comprehensive README file
readme_content = '''# Log Parser with Streamlit Regex Manager

A comprehensive log parsing system that automatically detects log types, applies appropriate regex patterns, and extracts structured data (IP addresses, timestamps, and messages) from various log file formats.

## Features

- **Automatic Log Type Detection**: Automatically identifies Apache, Nginx, Syslog, Firewall, and custom log formats
- **Flexible Regex Pattern Management**: Add, edit, and test regex patterns through a user-friendly Streamlit interface
- **Structured Data Extraction**: Extracts IP addresses, timestamps, messages, and other fields from log files
- **CSV Output**: Saves parsed data in CSV format for easy analysis
- **Pattern Testing**: Test regex patterns against sample log lines before saving

## File Structure

```
├── log_parser.py              # Main log parsing script
├── regex_manager_app.py       # Streamlit app for managing regex patterns
├── regex.json                 # JSON file containing regex patterns
├── requirements.txt           # Python dependencies
├── log/                       # Input folder for .log files
│   ├── apache_access.log
│   ├── nginx_access.log
│   ├── syslog.log
│   └── custom_app.log
└── oplogs/                    # Output folder for .csv files
    ├── apache_access.csv
    ├── nginx_access.csv
    └── ...
```

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure you have Python 3.7+ installed

## Usage

### 1. Managing Regex Patterns (Streamlit App)

Run the Streamlit app to manage regex patterns:

```bash
streamlit run regex_manager_app.py
```

The app provides three main tabs:

#### Add/Edit Patterns
- Add new regex patterns with unique key names
- Test patterns against sample log lines
- Validate regex syntax before saving

#### View Patterns  
- Browse existing patterns
- Search through patterns
- Delete patterns you no longer need

#### Test Patterns
- Test existing patterns against sample data
- See what fields are captured by each pattern
- Verify patterns work with your actual log data

### 2. Running the Log Parser

Execute the log parser to process all .log files:

```bash
python log_parser.py
```

The parser will:
1. Scan the `log/` folder for all `.log` files
2. Detect the log type for each line
3. Apply the appropriate regex pattern from `regex.json`
4. Extract structured data (IP, timestamp, message, etc.)
5. Save results as CSV files in the `oplogs/` folder

### 3. Adding New Log Files

1. Place your `.log` files in the `log/` folder
2. If needed, add custom regex patterns using the Streamlit app
3. Run the parser to process the new files

## Regex Pattern Format

Regex patterns must use named groups to capture specific fields:

### Required Named Groups:
- `(?P<ip>...)` - IP address
- `(?P<timestamp>...)` - Timestamp  
- `(?P<message>...)` - Log message

### Example Pattern:
```regex
(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - \[(?P<timestamp>[\w:/]+\s[+\-]\d{4})\] "(?P<method>\S+) (?P<path>\S+)" (?P<status>\d{3}) (?P<size>\d+) "(?P<message>.*)"
```

### Supported Log Types:

1. **Apache Access Logs**
   - Format: `IP - - [timestamp] "method path protocol" status size "referer" "user-agent"`
   - Key: `apache_access`

2. **Nginx Access Logs** 
   - Format: `IP - - [timestamp] "method path" status size "referer" "user-agent"`
   - Key: `nginx_access`

3. **Syslog**
   - Format: `timestamp hostname service: IP message`
   - Key: `syslog`

4. **Firewall Logs**
   - Format: `timestamp source action IP message`
   - Key: `firewall`

5. **Custom Application Logs**
   - Format: `timestamp [level] IP - message`
   - Key: `custom_app`

## Output Format

The parser generates CSV files with the following columns:

- `line_number`: Original line number in the log file
- `log_type`: Detected log type  
- `ip`: Extracted IP address
- `timestamp`: Extracted timestamp
- `message`: Extracted message/description
- `raw_line`: Original unparsed log line
- Additional fields based on the regex pattern used

## Customization

### Adding New Log Types:

1. **Via Streamlit App** (Recommended):
   - Open the regex manager app
   - Add your pattern with a unique key name
   - Test the pattern with sample data
   - Save the pattern

2. **Manual JSON Edit**:
   - Edit `regex.json` directly
   - Add your pattern with appropriate named groups
   - Ensure the pattern includes `ip`, `timestamp`, and `message` groups

3. **Modify Detection Logic**:
   - Edit the `detect_log_type()` method in `log_parser.py`
   - Add detection rules for your new log format

### Example Custom Pattern:

```json
{
  "my_custom_log": "(?P<timestamp>\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}) (?P<level>\\w+) (?P<ip>\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}) (?P<message>.*)"
}
```

## Error Handling

- **Invalid Regex**: The system validates patterns before saving
- **Missing Files**: Creates necessary directories automatically
- **Parse Failures**: Lines that don't match patterns are saved with basic information
- **Encoding Issues**: Handles different text encodings gracefully

## Tips for Success

1. **Test Your Patterns**: Always test regex patterns with real log samples
2. **Use Named Groups**: Essential for structured data extraction
3. **Escape Special Characters**: Use `\\\\` for literal backslashes in JSON
4. **Start Simple**: Begin with basic patterns and add complexity as needed
5. **Backup Patterns**: Keep a backup of your `regex.json` file

## Troubleshooting

### Common Issues:

1. **No matches found**: Check if your regex pattern matches the actual log format
2. **JSON decode error**: Verify `regex.json` has valid JSON syntax  
3. **Permission errors**: Ensure write permissions for `oplogs/` folder
4. **Import errors**: Install all requirements from `requirements.txt`

### Debug Steps:

1. Test patterns using the Streamlit app's test functionality
2. Check the console output for parsing errors
3. Verify log files are in the correct `log/` directory
4. Ensure `regex.json` contains patterns for your log types

## Contributing

Feel free to extend this system with:
- Additional log format support
- Enhanced pattern detection
- More robust error handling
- Additional output formats (JSON, XML, etc.)

## License

This project is open source and available under the MIT License.
'''

with open('README.md', 'w') as f:
    f.write(readme_content)

print("Created comprehensive README.md")

# Create a demo script to show how everything works together
demo_script = '''#!/usr/bin/env python3
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
    print("\\n🔧 Running Log Parser...")
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
            print(f"\\n📊 Generated {len(csv_files)} CSV files:")
            for csv_file in csv_files:
                print(f"   • {csv_file.name}")
        
    except Exception as e:
        print(f"❌ Error running log parser: {e}")

def show_file_structure():
    """Display the current file structure"""
    print("\\n📁 Current File Structure:")
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
    
    print("\\n🚀 Next Steps:")
    print("-" * 20)
    print("1. Run Streamlit app: streamlit run regex_manager_app.py")
    print("2. Add your own .log files to the 'log/' folder")
    print("3. Create custom regex patterns for your log formats")
    print("4. Run the parser again: python log_parser.py")
    print("\\n💡 Check the generated CSV files in the 'oplogs/' folder!")

if __name__ == "__main__":
    main()
'''

with open('demo.py', 'w') as f:
    f.write(demo_script)

print("Created demo.py script")

# Make demo script executable (on Unix systems)
try:
    import stat
    st = os.stat('demo.py')
    os.chmod('demo.py', st.st_mode | stat.S_IEXEC)
except:
    pass  # Ignore on Windows

print("\\n✅ All files created successfully!")
print("\\nFiles created:")
print("- log_parser.py (Main parsing script)")
print("- regex_manager_app.py (Streamlit interface)")  
print("- regex.json (Pattern definitions)")
print("- requirements.txt (Dependencies)")
print("- README.md (Documentation)")
print("- demo.py (Demo script)")
print("- log/ folder with sample log files")
print("- oplogs/ folder for CSV outputs")