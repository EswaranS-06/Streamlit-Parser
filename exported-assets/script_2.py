# Create a sample regex.json file with common log patterns
sample_regex_patterns = {
    "apache_access": r'(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - \[(?P<timestamp>[\w:/]+\s[+\-]\d{4})\] "(?P<method>\S+) (?P<path>\S+)\s*(?P<protocol>\S*)" (?P<status>\d{3}) (?P<size>\d+) "(?P<referer>.*?)" "(?P<message>.*?)"',
    "nginx_access": r'(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - \[(?P<timestamp>[^\]]+)\] "(?P<method>\w+) (?P<path>[^"]*)" (?P<status>\d+) (?P<size>\d+) "(?P<referer>[^"]*)" "(?P<message>[^"]*)"',
    "syslog": r'(?P<timestamp>\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}) (?P<hostname>\S+) (?P<source>\S+): (?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})? ?(?P<message>.*)',
    "firewall": r'(?P<timestamp>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}) (?P<source>\S+) (?P<action>\w+) (?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) (?P<message>.*)',
    "custom_app": r'(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z) \[(?P<level>\w+)\] (?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - (?P<message>.*)'
}

# Save sample regex patterns
with open('regex.json', 'w') as f:
    import json
    json.dump(sample_regex_patterns, f, indent=4)

print("Created regex.json with sample patterns")

# Create sample log files for testing
import os
os.makedirs('log', exist_ok=True)

# Apache access log sample
apache_log = '''192.168.1.1 - - [25/May/2023:10:15:32 +0000] "GET /index.html HTTP/1.1" 200 2326 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
10.0.0.1 - - [25/May/2023:10:16:45 +0000] "POST /api/login HTTP/1.1" 200 1234 "https://example.com/login" "curl/7.68.0"
192.168.1.100 - - [25/May/2023:10:17:02 +0000] "GET /dashboard HTTP/1.1" 404 512 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"'''

with open('log/apache_access.log', 'w') as f:
    f.write(apache_log)

# Nginx access log sample
nginx_log = '''172.16.0.1 - - [01/Jan/2023:12:00:00 +0000] "GET /home" 200 1500 "http://example.com" "Mozilla/5.0 Safari/537.36"
203.0.113.1 - - [01/Jan/2023:12:01:15 +0000] "POST /api/data" 201 800 "-" "Python-requests/2.28.1"
10.1.1.50 - - [01/Jan/2023:12:02:30 +0000] "DELETE /api/user/123" 204 0 "https://admin.example.com" "PostmanRuntime/7.29.2"'''

with open('log/nginx_access.log', 'w') as f:
    f.write(nginx_log)

# Syslog sample
syslog_content = '''Jan 22 16:14:23 web-server sshd[1203]: 192.168.1.195 Failed login attempt for user admin
Jan 22 16:15:45 web-server httpd[2456]: 10.0.0.25 GET request to /secure-area denied
Jan 22 16:16:12 web-server firewall[3789]: 203.0.113.50 Connection blocked from suspicious IP'''

with open('log/syslog.log', 'w') as f:
    f.write(syslog_content)

# Custom application log sample
custom_log = '''2023-12-01T14:30:15.123Z [INFO] 192.168.1.10 - User authentication successful
2023-12-01T14:31:22.456Z [WARN] 10.0.0.55 - Rate limit exceeded for API calls
2023-12-01T14:32:08.789Z [ERROR] 172.16.0.100 - Database connection failed'''

with open('log/custom_app.log', 'w') as f:
    f.write(custom_log)

print("Created sample log files in 'log' folder")

# Create requirements.txt
requirements = '''streamlit>=1.28.0
pandas>=1.5.0
pathlib2>=2.3.0
'''

with open('requirements.txt', 'w') as f:
    f.write(requirements)

print("Created requirements.txt")

# Create oplogs folder
os.makedirs('oplogs', exist_ok=True)
print("Created 'oplogs' folder for output CSV files")