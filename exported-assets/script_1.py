# Now let's create the Streamlit app for managing regex patterns
streamlit_app_code = '''
import streamlit as st
import json
import os
import re
from pathlib import Path

class RegexManager:
    def __init__(self, regex_file="regex.json"):
        self.regex_file = regex_file
        
    def load_regex_patterns(self):
        """Load existing regex patterns from JSON file"""
        try:
            with open(self.regex_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Create empty file if it doesn't exist
            empty_patterns = {}
            self.save_regex_patterns(empty_patterns)
            return empty_patterns
        except json.JSONDecodeError:
            st.error(f"Error decoding {self.regex_file}. Please check the JSON format.")
            return {}
    
    def save_regex_patterns(self, patterns):
        """Save regex patterns to JSON file"""
        try:
            with open(self.regex_file, 'w') as f:
                json.dump(patterns, f, indent=4)
            return True
        except Exception as e:
            st.error(f"Error saving regex patterns: {e}")
            return False
    
    def validate_regex(self, pattern):
        """Validate if the regex pattern is valid"""
        try:
            re.compile(pattern)
            return True, "Valid regex pattern"
        except re.error as e:
            return False, f"Invalid regex pattern: {e}"
    
    def test_regex_pattern(self, pattern, test_string):
        """Test regex pattern against a sample string"""
        try:
            match = re.match(pattern, test_string)
            if match:
                return True, match.groupdict() if match.groups() else match.group(0)
            else:
                return False, "No match found"
        except Exception as e:
            return False, f"Error testing regex: {e}"

def main():
    st.set_page_config(
        page_title="Log Parser Regex Manager", 
        page_icon="🔧",
        layout="wide"
    )
    
    st.title("🔧 Log Parser Regex Manager")
    st.markdown("Manage regex patterns for log parsing")
    
    # Initialize regex manager
    regex_manager = RegexManager()
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["📝 Add/Edit Patterns", "📋 View Patterns", "🧪 Test Patterns"])
    
    # Tab 1: Add/Edit Patterns
    with tab1:
        st.header("Add New Regex Pattern")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Input fields
            key_name = st.text_input(
                "Pattern Key Name", 
                placeholder="e.g., apache_access, nginx_error, custom_app",
                help="Unique identifier for this regex pattern"
            )
            
            regex_pattern = st.text_area(
                "Regex Pattern", 
                placeholder="Enter your regex pattern with named groups like (?P<ip>\\d+\\.\\d+\\.\\d+\\.\\d+)",
                height=150,
                help="Use named groups to capture specific fields: (?P<field_name>pattern)"
            )
            
        with col2:
            st.markdown("### Pattern Guidelines")
            st.markdown("""
            **Required Named Groups:**
            - `(?P<ip>...)` - IP address
            - `(?P<timestamp>...)` - Timestamp
            - `(?P<message>...)` - Log message
            
            **Common Patterns:**
            - IP: `\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}`
            - Date: `\\d{4}-\\d{2}-\\d{2}`
            - Time: `\\d{2}:\\d{2}:\\d{2}`
            - Any text: `.*?`
            - Non-whitespace: `\\S+`
            """)
        
        # Validation and testing
        if regex_pattern:
            is_valid, validation_msg = regex_manager.validate_regex(regex_pattern)
            if is_valid:
                st.success(f"✅ {validation_msg}")
            else:
                st.error(f"❌ {validation_msg}")
        
        # Test section
        st.subheader("Test Your Pattern")
        test_string = st.text_area(
            "Sample Log Line", 
            placeholder="Paste a sample log line to test your regex pattern",
            help="This will help you verify that your regex pattern works correctly"
        )
        
        if test_string and regex_pattern:
            test_success, test_result = regex_manager.test_regex_pattern(regex_pattern, test_string)
            if test_success:
                st.success("✅ Pattern matches!")
                if isinstance(test_result, dict):
                    st.json(test_result)
                else:
                    st.code(test_result)
            else:
                st.warning(f"⚠️ {test_result}")
        
        # Save button
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            if st.button("💾 Save Pattern", type="primary"):
                if key_name and regex_pattern:
                    is_valid, _ = regex_manager.validate_regex(regex_pattern)
                    if is_valid:
                        patterns = regex_manager.load_regex_patterns()
                        patterns[key_name] = regex_pattern
                        if regex_manager.save_regex_patterns(patterns):
                            st.success(f"✅ Pattern '{key_name}' saved successfully!")
                            st.rerun()
                    else:
                        st.error("❌ Please fix the regex pattern before saving")
                else:
                    st.error("❌ Please provide both key name and regex pattern")
        
        with col2:
            if st.button("🗑️ Clear Form"):
                st.rerun()
    
    # Tab 2: View Patterns
    with tab2:
        st.header("Existing Regex Patterns")
        
        patterns = regex_manager.load_regex_patterns()
        
        if patterns:
            # Search functionality
            search_term = st.text_input("🔍 Search patterns", placeholder="Enter key name to search...")
            
            filtered_patterns = {
                k: v for k, v in patterns.items() 
                if search_term.lower() in k.lower() if search_term
            } if search_term else patterns
            
            for key, pattern in filtered_patterns.items():
                with st.expander(f"🔧 {key}"):
                    st.code(pattern, language="regex")
                    
                    col1, col2 = st.columns([1, 1])
                    
                    with col1:
                        if st.button(f"📋 Copy", key=f"copy_{key}"):
                            st.write("Pattern copied to clipboard!")  # Note: Actual clipboard copy requires JS
                    
                    with col2:
                        if st.button(f"🗑️ Delete", key=f"delete_{key}"):
                            if st.session_state.get(f"confirm_delete_{key}"):
                                patterns = regex_manager.load_regex_patterns()
                                del patterns[key]
                                if regex_manager.save_regex_patterns(patterns):
                                    st.success(f"Pattern '{key}' deleted!")
                                    st.rerun()
                            else:
                                st.session_state[f"confirm_delete_{key}"] = True
                                st.warning("Click again to confirm deletion")
        else:
            st.info("No regex patterns found. Add some patterns in the 'Add/Edit Patterns' tab.")
    
    # Tab 3: Test Patterns
    with tab3:
        st.header("Test Regex Patterns")
        
        patterns = regex_manager.load_regex_patterns()
        
        if patterns:
            # Pattern selection
            selected_pattern = st.selectbox(
                "Select Pattern to Test",
                options=list(patterns.keys()),
                format_func=lambda x: f"{x}"
            )
            
            if selected_pattern:
                st.subheader(f"Testing Pattern: {selected_pattern}")
                st.code(patterns[selected_pattern], language="regex")
                
                # Multiple test strings
                st.subheader("Test Cases")
                
                # Load sample log lines for testing
                sample_logs = {
                    "apache_access": '192.168.1.1 - - [25/May/2023:10:15:32 +0000] "GET /index.html HTTP/1.1" 200 54321',
                    "nginx_access": '10.0.0.1 - - [01/Jan/2023:12:00:00 +0000] "POST /api/data HTTP/1.1" 201 1234 "http://example.com" "Mozilla/5.0"',
                    "syslog": 'Jan 22 16:14:23 server sshd[1203]: 192.168.1.100 Failed login attempt',
                    "firewall": '2023-01-01 10:30:45 firewall DENY 192.168.1.50 Blocked connection attempt'
                }
                
                # Show relevant sample
                if selected_pattern in sample_logs:
                    st.text_area(
                        "Sample Log (you can modify this)",
                        value=sample_logs[selected_pattern],
                        key=f"sample_{selected_pattern}"
                    )
                
                # Custom test input
                test_input = st.text_area(
                    "Your Test Log Line",
                    height=100,
                    placeholder="Enter your log line to test...",
                    key=f"test_input_{selected_pattern}"
                )
                
                if test_input:
                    test_success, test_result = regex_manager.test_regex_pattern(
                        patterns[selected_pattern], 
                        test_input
                    )
                    
                    if test_success:
                        st.success("✅ Pattern matches successfully!")
                        st.subheader("Captured Groups:")
                        if isinstance(test_result, dict):
                            for group_name, group_value in test_result.items():
                                st.text(f"{group_name}: {group_value}")
                        else:
                            st.text(f"Match: {test_result}")
                    else:
                        st.error(f"❌ {test_result}")
        else:
            st.info("No patterns available for testing. Please add some patterns first.")
    
    # Sidebar with information
    with st.sidebar:
        st.header("ℹ️ Information")
        st.markdown("""
        ### About This Tool
        This tool helps you manage regex patterns for the log parser.
        
        ### How to Use:
        1. **Add Patterns**: Create new regex patterns with named groups
        2. **View Patterns**: Browse and manage existing patterns
        3. **Test Patterns**: Verify your patterns work with sample data
        
        ### Tips:
        - Use named groups like `(?P<field_name>pattern)`
        - Always include ip, timestamp, and message groups
        - Test your patterns with real log samples
        - Use escape characters (\\\\) for special regex characters
        """)
        
        st.header("📊 Statistics")
        patterns = regex_manager.load_regex_patterns()
        st.metric("Total Patterns", len(patterns))
        
        if patterns:
            st.header("🏷️ Pattern Types")
            for pattern_name in patterns.keys():
                st.text(f"• {pattern_name}")

if __name__ == "__main__":
    main()
'''

# Save the Streamlit app code to a file
with open('regex_manager_app.py', 'w') as f:
    f.write(streamlit_app_code)

print("Created regex_manager_app.py")