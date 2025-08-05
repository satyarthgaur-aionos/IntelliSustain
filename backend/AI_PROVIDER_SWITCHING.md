# AI Provider Switching Guide

This guide explains how to switch between OpenAI and Google Gemini Pro AI providers in the Inferrix AI Agent.

## Quick Switch

To switch AI providers, simply change the `AI_PROVIDER` environment variable:

### For OpenAI (Default)
```
AI_PROVIDER=openai
OPENAI_API_KEY=your_openai_api_key_here
```

### For Google Gemini Pro
```
AI_PROVIDER=gemini
GEMINI_API_KEY=your_gemini_api_key_here
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `AI_PROVIDER` | AI provider to use (`openai` or `gemini`) | Yes |
| `OPENAI_API_KEY` | OpenAI API key | Required if using OpenAI |
| `GEMINI_API_KEY` | Google Gemini API key | Required if using Gemini |

## Setup Instructions

### 1. OpenAI Setup
1. Get your OpenAI API key from OpenAI Platform
2. Add to your `.env` file:
   ```
   AI_PROVIDER=openai
   OPENAI_API_KEY=sk-your-key-here
   ```

### 2. Google Gemini Setup
1. Get your Gemini API key from Google AI Studio
2. Add to your `.env` file:
   ```
   AI_PROVIDER=gemini
   GEMINI_API_KEY=your-gemini-key-here
   ```

## Testing Providers

Run the test script to verify both providers work:

```bash
python test_ai_providers.py
```

## Features Comparison

| Feature | OpenAI GPT-4o | Google Gemini Pro |
|---------|---------------|-------------------|
| Function Calling | Native | Custom Implementation |
| Response Quality | Excellent | Excellent |
| Speed | Fast | Fast |
| Cost | Higher | Lower |
| Rate Limits | Strict | Generous |

## Important Notes

1. **Restart Required**: After changing `AI_PROVIDER`, restart your application
2. **API Keys**: Ensure the corresponding API key is set for your chosen provider
3. **Function Calling**: OpenAI has native function calling, Gemini uses custom detection
4. **Compatibility**: All scenarios work with both providers

## Troubleshooting

### Common Issues

1. **"No valid AI provider configured"**
   - Check that `AI_PROVIDER` is set correctly
   - Ensure the corresponding API key is set

2. **"OpenAI client not initialized"**
   - Verify `OPENAI_API_KEY` is set
   - Check API key validity

3. **"Gemini API error"**
   - Verify `GEMINI_API_KEY` is set
   - Check API key validity

## Use Cases

### Choose OpenAI when:
- You need advanced function calling
- You have complex multi-step scenarios
- Cost is not a primary concern
- You need the highest accuracy

### Choose Gemini when:
- You want to optimize costs
- You have high-volume usage
- You need generous rate limits
- You prefer Google's AI ecosystem 