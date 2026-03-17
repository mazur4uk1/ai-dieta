# Food Recognition API Setup

This application now uses free online APIs for food recognition instead of local neural network models to reduce Docker image size and improve performance.

## Primary API: Edamam Food Detection API

### Free Tier Information
- **Free requests per month**: 1,000 requests
- **Rate limit**: 1 request per second
- **API endpoint**: https://api.edamam.com/api/food-detection-parser

### Setup Instructions

1. **Register for API Keys**
   - Go to https://developer.edamam.com/
   - Create a free account
   - Register a new application
   - Get your `APP_ID` and `APP_KEY`

2. **Set Environment Variables**
   ```bash
   # Add to your .env file or set as environment variables
   EDAMAM_APP_ID=your_app_id_here
   EDAMAM_APP_KEY=your_app_key_here
   ```

3. **Test the API**
   ```bash
   # Test endpoint is available
   curl "https://api.edamam.com/api/food-detection-parser?app_id=YOUR_APP_ID&app_key=YOUR_APP_KEY"
   ```

## Alternative Free APIs

If Edamam API is not suitable, you can use these alternatives:

### 1. Google Cloud Vision API
- **Free tier**: 1,000 units per month
- **Setup**: https://cloud.google.com/vision
- **Features**: General image recognition with food labels

### 2. Microsoft Azure Computer Vision
- **Free tier**: 5,000 transactions per month
- **Setup**: https://azure.microsoft.com/en-us/services/cognitive-services/computer-vision/
- **Features**: Image analysis and object detection

### 3. Clarifai API
- **Free tier**: 5,000 predictions per month
- **Setup**: https://www.clarifai.com/
- **Features**: AI-powered image and video recognition

## API Integration

The application automatically tries Edamam API first, then falls back to a simple detection method if the API is not configured or fails.

### API Response Format
```json
{
  "recognized_foods": [
    {
      "name": "Apple",
      "calories": 95,
      "confidence": 0.9
    }
  ]
}
```

### Testing the Endpoint
```bash
# Upload an image for food recognition
curl -X POST "http://localhost:8000/api/vision/recognize" \
  -H "Authorization: Bearer your_token" \
  -F "image=@path/to/food/image.jpg"

# Get available APIs information
curl "http://localhost:8000/api/vision/available-apis"
```

## Benefits of Online APIs

1. **Reduced Docker Image Size**: No need to include large neural network models
2. **Better Accuracy**: Professional APIs are trained on larger datasets
3. **Maintenance**: No need to update local models
4. **Scalability**: Can handle more complex food recognition scenarios
5. **Cost**: Free tiers are sufficient for most applications

## Troubleshooting

### API Key Issues
- Ensure environment variables are set correctly
- Check that API keys haven't expired
- Verify API usage limits haven't been exceeded

### Network Issues
- Ensure internet connectivity
- Check firewall settings
- Verify API endpoint accessibility

### Fallback Mode
If no API is configured, the application will use a fallback method that returns common food items with estimated calories.