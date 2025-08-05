#!/usr/bin/env python3
"""
Test exact response format from backend
"""

from enhanced_agentic_agent import EnhancedAgenticInferrixAgent

def test_exact_response_format():
    """Test the exact response format"""
    agent = EnhancedAgenticInferrixAgent()
    
    print("🧪 Testing Exact Response Format")
    print("=" * 50)
    
    # Test the exact query
    query = "show me critical alarms for past"
    
    print(f"Query: {query}")
    print()
    
    try:
        # Get response
        response = agent.process_query(query)
        
        print("Response:")
        print("-" * 50)
        print(repr(response))  # Show exact characters
        print("-" * 50)
        print("Formatted response:")
        print(response)
        print("-" * 50)
        
        # Check if it contains table markers
        lines = response.split('\n')
        print(f"Number of lines: {len(lines)}")
        print(f"First line: {repr(lines[0])}")
        print(f"Second line: {repr(lines[1])}")
        print(f"Third line: {repr(lines[2])}")
        
        # Check for table structure
        has_pipe_start = any(line.strip().startswith('|') for line in lines)
        has_separator = any('---' in line for line in lines)
        has_time_header = '| Time |' in response
        
        print(f"Has pipe start: {has_pipe_start}")
        print(f"Has separator: {has_separator}")
        print(f"Has time header: {has_time_header}")
        
        return response
        
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    test_exact_response_format() 