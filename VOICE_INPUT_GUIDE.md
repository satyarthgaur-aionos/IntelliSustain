# 🎤 Voice Input Accuracy Guide

## Overview
This guide provides tips and best practices for achieving better speech-to-text accuracy with the IntelliSustain AI Agent voice input feature.

## 🚀 Recent Improvements

### Enhanced Speech Recognition Configuration
- **Multiple Alternatives**: System now captures 5 alternative interpretations
- **Confidence Scoring**: Real-time confidence level display
- **Post-Processing**: Automatic correction of common speech recognition errors
- **Language Selection**: Support for multiple English variants and Hindi
- **Pause Handling**: Automatically handles pauses up to 3 seconds without losing context
- **Accent Support**: Optimized for various Indian English accents and speech patterns

### Smart Corrections
The system automatically corrects common speech recognition errors for Indian English accents:
- `miner`/`myner`/`meener`/`minar` → `minor`
- `temperatures`/`temprature`/`tempature` → `temperature`
- `thermostats`/`thermostate`/`thermo` → `thermostat`
- `alarms`/`alerm`/`alert` → `alarm`
- `floors`/`flor`/`level` → `floor`
- `rooms`/`rum`/`chamber` → `room`
- `rightnow`/`right-now` → `right now`
- `atpresent`/`at-present` → `at present`
- And many more Indian English accent variations...

### Filler Word Removal
The system automatically removes common thinking and speaking filler words:
- **Thinking words**: `hmm`, `um`, `uh`, `ah`, `err`, `er`, `erm`
- **Speaking fillers**: `actually`, `basically`, `you know`, `like`, `so`
- **Thinking phrases**: `let me think`, `i mean`, `i think`, `sort of`, `kind of`
- **Response words**: `yeah`, `yep`, `nope`, `sure`, `alright`

## 📋 Best Practices for Better Accuracy

### 1. **Speaking Technique**
- **Clear Pronunciation**: Speak clearly and at a normal pace
- **Pause Handling**: System automatically handles pauses up to 3 seconds
- **Natural Rhythm**: Don't speak too fast or too slow
- **Volume**: Speak at normal conversation volume
- **Accent Flexibility**: Works with all Indian English accent variations

### 2. **Environment Setup**
- **Quiet Environment**: Minimize background noise
- **Good Microphone**: Use a quality microphone if possible
- **Browser Choice**: Use Chrome, Edge, or Firefox for best results
- **Microphone Permissions**: Ensure microphone access is granted

### 3. **Language Selection**
Choose the appropriate language setting:
- **English (India)**: Best for Indian English accents
- **English (US)**: For American English
- **English (UK)**: For British English
- **Hindi (India)**: For Hindi speech

### 4. **Query Structure**
- **Simple Phrases**: Use clear, simple sentences
- **Key Words**: Emphasize important words (temperature, alarm, room, etc.)
- **Natural Language**: Speak as you would to a person

## 🎯 Example Voice Commands

### Temperature Queries
- ✅ "What is the temperature in room 50 second floor"
- ✅ "Show temperature for 2F room 50"
- ✅ "Room 50 2nd floor ka tapmaan kya hai"
- ❌ "What's the temp in room fifty second floor" (avoid abbreviations)

### Alarm Queries
- ✅ "Show critical alarms right now"
- ✅ "What are the highest severity alarms today"
- ✅ "Display minor alarms from yesterday"
- ❌ "Show me all the alarms" (too vague)

### Energy Queries
- ✅ "Show energy consumption for all devices"
- ✅ "What is the power usage in room 50"
- ✅ "Display energy data for second floor"
- ❌ "Energy" (too short)

### Device Control
- ✅ "Set temperature to 22 degrees in room 50"
- ✅ "Increase fan speed to high in second floor"
- ✅ "Turn off HVAC in room 33"
- ❌ "Make it colder" (too vague)

## 🔧 Troubleshooting

### Common Issues and Solutions

#### 1. **"No speech detected"**
- **Solution**: Speak louder and more clearly
- **Check**: Microphone permissions and browser settings

#### 2. **Poor accuracy with specific words**
- **Solution**: Use the language selector to match your accent
- **Try**: Different phrasing for the same request

#### 3. **System stops listening after pause**
- **Solution**: System now automatically handles pauses up to 3 seconds
- **Alternative**: If longer pause needed, click the microphone button again

#### 4. **Wrong word recognition (e.g., "miner" instead of "minor")**
- **Solution**: The system automatically corrects Indian English accent variations
- **If persistent**: Try rephrasing or using synonyms
- **Accent Support**: Works with all Indian English accent patterns

#### 5. **Filler words in transcript (e.g., "um", "hmm", "you know")**
- **Solution**: The system automatically removes common filler words
- **Result**: Clean, professional queries without thinking words
- **Examples**: "um... hmm... temperature" → "temperature"

### Browser-Specific Tips

#### Chrome/Edge (Recommended)
- Best speech recognition accuracy
- Full feature support
- Automatic language detection

#### Firefox
- Good support
- May require manual language selection

#### Safari
- Limited support
- Consider using Chrome/Edge for voice input

## 📊 Confidence Levels

The system shows confidence levels during voice input:
- **90-100%**: Excellent recognition
- **70-89%**: Good recognition
- **50-69%**: Fair recognition
- **Below 50%**: Poor recognition - try rephrasing

## 🎤 Voice Input Tips Summary

1. **Speak Clearly**: Enunciate words properly
2. **Use Simple Phrases**: Avoid complex sentences
3. **Choose Right Language**: Match your accent
4. **Pause Handling**: System handles pauses up to 3 seconds automatically
5. **Accent Flexibility**: Works with all Indian English accent variations
6. **Good Environment**: Reduce background noise
7. **Quality Microphone**: Use a decent microphone
8. **Browser Choice**: Use Chrome/Edge for best results
9. **Practice**: Try different phrasings for the same request

## 🔄 Continuous Improvement

The voice recognition system learns and improves over time. If you encounter persistent issues:

1. **Try Different Phrasing**: Use synonyms or alternative word orders
2. **Use Language Settings**: Switch between language variants
3. **Report Issues**: Let us know about specific problems
4. **Practice**: Regular use improves recognition accuracy

## 📞 Support

If you continue to experience issues with voice input:
- Check microphone permissions
- Try a different browser
- Ensure a quiet environment
- Use the text input as an alternative

---

*Last Updated: December 2024*
*Version: 2.0 - Enhanced with smart corrections and confidence scoring*
