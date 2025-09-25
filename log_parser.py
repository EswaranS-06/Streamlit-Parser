
import os
import re
import json
import csv
import glob
from pathlib import Path

class LogParser:
    def __init__(self, log_folder="log", regex_file="regex.json", output_folder="oplogs"):
        self.log_folder = log_folder
        self.regex_file = regex_file
        self.output_folder = output_folder

        # Create output folder if it doesn't exist
        Path(self.output_folder).mkdir(parents=True, exist_ok=True)

    def load_regex_patterns(self):
        """Load regex patterns from JSON file"""
        try:
            with open(self.regex_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Regex file {self.regex_file} not found. Creating empty file.")
            # Create empty regex file if it doesn't exist
            empty_patterns = {
                "apache_access": r'(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - \[(?P<timestamp>[\w:/]+\s[+\-]\d{4})\] "(?P<method>\S+) (?P<path>\S+)\s*(?P<protocol>\S*)" (?P<status>\d{3}) (?P<size>\d+) "(?P<message>.*?)"',
                "nginx_access": r'(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - \[(?P<timestamp>[^\]]+)\] "(?P<method>\w+) (?P<path>[^"]*)" (?P<status>\d+) (?P<size>\d+) "(?P<referer>[^"]*)" "(?P<message>[^"]*)"',
                "syslog": r'(?P<timestamp>\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}) (?P<hostname>\S+) (?P<source>\S+): (?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})? ?(?P<message>.*)',
                "firewall": r'(?P<timestamp>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}) (?P<source>\S+) (?P<action>\w+) (?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) (?P<message>.*)'
            }
            with open(self.regex_file, 'w') as f:
                json.dump(empty_patterns, f, indent=4)
            return empty_patterns
        except json.JSONDecodeError:
            print(f"Error decoding {self.regex_file}. Please check the JSON format.")
            return {}

    def detect_log_type(self, line):
        """Detect log source and type based on line content"""
        line_lower = line.lower()

        # Apache access log detection
        if ' - - [' in line and '"GET ' in line or '"POST ' in line:
            return "apache_access"

        # Nginx access log detection  
        elif '"' in line and ' - - [' in line and 'HTTP/' in line:
            return "nginx_access"

        # Syslog detection (month day time hostname)
        elif re.match(r'^\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}', line):
            return "syslog"

        # Firewall log detection (YYYY-MM-DD HH:MM:SS format)
        elif re.match(r'^\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}', line):
            return "firewall"

        # Default fallback
        return "unknown"

    def parse_log_line(self, line, regex_pattern):
        """Parse a single log line using the provided regex pattern"""
        try:
            match = re.match(regex_pattern, line.strip())
            if match:
                groups = match.groupdict()
                # Extract required fields, set defaults if not found
                result = {
                    'ip': groups.get('ip', 'N/A'),
                    'timestamp': groups.get('timestamp', 'N/A'), 
                    'message': groups.get('message', line.strip())
                }
                # Add any additional fields that were captured
                for key, value in groups.items():
                    if key not in result:
                        result[key] = value
                return result
        except Exception as e:
            print(f"Error parsing line with regex: {e}")

        return None

    def parse_log_file(self, log_file_path):
        """Parse a single log file"""
        regex_patterns = self.load_regex_patterns()
        parsed_logs = []

        print(f"Processing {log_file_path}")

        try:
            with open(log_file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line_num, line in enumerate(f, 1):
                    if line.strip():  # Skip empty lines
                        # Detect log type
                        log_type = self.detect_log_type(line)

                        # Get corresponding regex pattern
                        regex_pattern = regex_patterns.get(log_type)

                        if regex_pattern:
                            parsed_data = self.parse_log_line(line, regex_pattern)
                            if parsed_data:
                                parsed_data['line_number'] = line_num
                                parsed_data['log_type'] = log_type
                                parsed_data['raw_line'] = line.strip()
                                parsed_logs.append(parsed_data)
                            else:
                                # If parsing failed, create a basic entry
                                parsed_logs.append({
                                    'line_number': line_num,
                                    'log_type': log_type,
                                    'ip': 'N/A',
                                    'timestamp': 'N/A',
                                    'message': line.strip(),
                                    'raw_line': line.strip()
                                })
                        else:
                            print(f"No regex pattern found for log type: {log_type}")
                            # Create basic entry for unknown log types
                            parsed_logs.append({
                                'line_number': line_num,
                                'log_type': log_type,
                                'ip': 'N/A',
                                'timestamp': 'N/A',
                                'message': line.strip(),
                                'raw_line': line.strip()
                            })

        except Exception as e:
            print(f"Error reading file {log_file_path}: {e}")
            return []

        return parsed_logs

    def save_to_csv(self, parsed_logs, output_file):
        """Save parsed logs to CSV file"""
        if not parsed_logs:
            print(f"No data to save for {output_file}")
            return

        # Get all unique fieldnames from parsed logs
        fieldnames = set()
        for log in parsed_logs:
            fieldnames.update(log.keys())

        # Ensure required fields come first
        required_fields = ['line_number', 'log_type', 'ip', 'timestamp', 'message']
        ordered_fieldnames = []
        for field in required_fields:
            if field in fieldnames:
                ordered_fieldnames.append(field)
                fieldnames.remove(field)

        # Add remaining fields
        ordered_fieldnames.extend(sorted(fieldnames))

        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=ordered_fieldnames)
                writer.writeheader()
                writer.writerows(parsed_logs)
            print(f"Saved {len(parsed_logs)} parsed log entries to {output_file}")
        except Exception as e:
            print(f"Error saving CSV file {output_file}: {e}")

    def process_all_logs(self):
        """Process all .log files in the log folder"""
        log_files = glob.glob(os.path.join(self.log_folder, "*.log"))

        if not log_files:
            print(f"No .log files found in {self.log_folder} folder")
            return

        for log_file_path in log_files:
            # Get filename without extension
            filename = Path(log_file_path).stem
            output_file = os.path.join(self.output_folder, f"{filename}.csv")

            # Parse the log file
            parsed_logs = self.parse_log_file(log_file_path)

            # Save to CSV
            self.save_to_csv(parsed_logs, output_file)

def main():
    """Main function to run the log parser"""
    parser = LogParser()
    parser.process_all_logs()

if __name__ == "__main__":
    main()
