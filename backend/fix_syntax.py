#!/usr/bin/env python3

# Fix the syntax error in agentic_agent.py
with open('agentic_agent.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the problematic string with properly escaped quotes
# The original has unescaped quotes inside a double-quoted string
fixed_content = content.replace(
    '"Acknowledge alarm ALM123"',
    '\\"Acknowledge alarm ALM123\\"'
).replace(
    '"Acknowledge alarm for Device 150002"',
    '\\"Acknowledge alarm for Device 150002\\"'
).replace(
    '"Show active alarms"',
    '\\"Show active alarms\\"'
)

# Also fix the malformed escaping that was created
fixed_content = fixed_content.replace(
    '\\"\\"Acknowledge alarm ALM123\\"\\"',
    '\\"Acknowledge alarm ALM123\\"'
).replace(
    '\\"\\"Acknowledge alarm for Device 150002\\"\\"',
    '\\"Acknowledge alarm for Device 150002\\"'
).replace(
    '\\"\\"Show active alarms\\"\\"',
    '\\"Show active alarms\\"'
)

with open('agentic_agent.py', 'w', encoding='utf-8') as f:
    f.write(fixed_content)

print("✅ Fixed syntax error in agentic_agent.py") 