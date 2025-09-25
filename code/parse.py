import re
import json
import csv
import os
from datetime import datetime
import logging
from pathlib import Path
from typing import Dict, List, Optional

class EnhancedLogParser:
    def __init__(self, regex_file: str = "regex_patterns.json"):
        """Initialize LogParser with regex patterns from JSON file"""
        self.regex_patterns = self._load_regex_patterns(regex_file)
        self.logger = self._setup_logger()

    def _load_regex_patterns(self, regex_file: str) -> Dict:
        """Load regex patterns from JSON file"""
        try:
            with open(regex_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Regex pattern file {regex_file} not found")

    def _setup_logger(self) -> logging.Logger:
        """Setup logging configuration"""
        logger = logging.getLogger('EnhancedLogParser')
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def detect_log_type(self, line: str) -> Optional[str]:
        """Automatically detect log type based on line content"""
        for log_type, config in self.regex_patterns.items():
            pattern = config['pattern']
            if pattern and re.match(pattern, line):
                return log_type
        return None

    def parse_log_line(self, line: str, log_type: str) -> Optional[Dict]:
        """Parse a single log line using the appropriate regex pattern"""
        if log_type not in self.regex_patterns:
            self.logger.error(f"Unknown log type: {log_type}")
            return None

        config = self.regex_patterns[log_type]
        pattern = config['pattern']
        timestamp_format = config['timestamp_format']
        
        if not pattern:
            self.logger.error(f"No pattern found for log type: {log_type}")
            return None

        match = re.match(pattern, line)
        if not match:
            self.logger.warning(f"Line does not match pattern for {log_type}: {line}")
            return None

        try:
            parsed_data = match.groupdict()
            if 'timestamp' in parsed_data and timestamp_format:
                try:
                    timestamp = datetime.strptime(parsed_data['timestamp'], timestamp_format)
                    parsed_data['timestamp'] = timestamp.strftime('%Y-%m-%d %H:%M:%S')
                except ValueError as e:
                    self.logger.warning(f"Could not parse timestamp: {e}")
            
            # Ensure all expected fields are present
            for field in ['hostname', 'process', 'pid', 'level', 'message']:
                if field not in parsed_data:
                    parsed_data[field] = ''
            
            return parsed_data
        except Exception as e:
            self.logger.error(f"Error parsing line: {line}. Error: {str(e)}")
            return None

    def process_logs(self, logs_dir: str, output_dir: str):
        """Process all logs in the directory and save results as CSV"""
        # Create output directory if it doesn't exist
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        # Process each log file
        for log_file in Path(logs_dir).glob('*.log'):
            self.logger.info(f"Processing {log_file}")
            parsed_entries = []
            
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    for line_num, line in enumerate(f, 1):
                        line = line.strip()
                        if not line:
                            continue
                            
                        # Auto-detect log type
                        log_type = self.detect_log_type(line)
                        if log_type:
                            parsed_line = self.parse_log_line(line, log_type)
                            if parsed_line:
                                # Add line number for reference
                                parsed_line['line_num'] = line_num
                                parsed_entries.append(parsed_line)
                        else:
                            # Store unparseable lines with basic info
                            parsed_entries.append({
                                'timestamp': '',
                                'hostname': '',
                                'process': '',
                                'pid': '',
                                'level': '',
                                'message': line,
                                'line_num': line_num
                            })

                if parsed_entries:
                    # Create output CSV file
                    output_file = Path(output_dir) / f"{log_file.stem}_parsed.csv"
                    self._save_to_csv(parsed_entries, output_file)
                    self.logger.info(f"Saved parsed results to {output_file}")
                    self.logger.info(f"Processed {len(parsed_entries)} lines")

            except Exception as e:
                self.logger.error(f"Error processing {log_file}: {str(e)}")

    def _save_to_csv(self, entries: List[Dict], output_file: Path):
        """Save parsed entries to CSV file"""
        if not entries:
            return

        # Define fixed field order
        fieldnames = ['timestamp', 'hostname', 'process', 'pid', 'level', 'message', 'line_num']

        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(entries)

if __name__ == "__main__":
    # Initialize the parser
    parser = EnhancedLogParser()
    
    # Process logs
    parser.process_logs("logs", "oplogs")