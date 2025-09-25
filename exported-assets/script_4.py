# Let's test the log parser with our sample files
from log_parser import LogParser

print("Testing the log parser with sample files...")
print("=" * 50)

# Create an instance of the parser
parser = LogParser()

# Process all log files
parser.process_all_logs()

print("\n" + "=" * 50)
print("Demo completed! Check the oplogs folder for CSV outputs.")