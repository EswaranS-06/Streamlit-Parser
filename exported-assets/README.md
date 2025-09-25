# Log Parser with Streamlit Regex Manager

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
  "my_custom_log": "(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}) (?P<level>\w+) (?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) (?P<message>.*)"
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
3. **Escape Special Characters**: Use `\\` for literal backslashes in JSON
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
