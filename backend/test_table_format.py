#!/usr/bin/env python3
"""
Test table format generation
"""

from enhanced_agentic_agent import EnhancedAgenticInferrixAgent

def test_table_format():
    """Test the table format generation"""
    agent = EnhancedAgenticInferrixAgent()
    
    print("🧪 Testing Table Format Generation")
    print("=" * 50)
    
    # Test headers and rows
    headers = ["Time", "Device Name", "Location", "Type", "Severity", "Status"]
    rows = [
        ["2025-06-13 19:24", "RH/T Sensor - 150002", "", "Sensors Status Alert", "CRITICAL", "ACTIVE_UNACK"],
        ["2025-05-16 15:02", "Distance Sensor - 112001", "", "Sensors Status Alert", "CRITICAL", "ACTIVE_UNACK"],
        ["2025-04-28 00:25", "Lighting Controller V4 - 1040", "", "Sensors Status Alert", "CRITICAL", "ACTIVE_UNACK"]
    ]
    
    print("Headers:", headers)
    print("Rows:", rows)
    print()
    
    # Generate table
    table = agent._format_markdown_table(headers, rows)
    
    print("Generated Table:")
    print("-" * 50)
    print(table)
    print("-" * 50)
    
    # Check if it's valid markdown
    lines = table.strip().split('\n')
    print(f"Number of lines: {len(lines)}")
    print(f"First line starts with |: {lines[0].startswith('|')}")
    print(f"Second line contains ---: {'---' in lines[1]}")
    print(f"Has data rows: {len(lines) > 2}")
    
    return table

if __name__ == "__main__":
    test_table_format() 