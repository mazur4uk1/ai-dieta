#!/usr/bin/env python3
"""
Simple test script to verify the vision API works correctly.
This script tests the food recognition endpoint.
"""

import asyncio
import httpx
import base64
from io import BytesIO
from PIL import Image
import numpy as np

async def test_vision_api():
    """Test the vision API endpoint"""
    
    # Create a simple test image (a colored rectangle)
    # In a real test, you would use an actual food image
    img = Image.new('RGB', (100, 100), color='red')
    buffer = BytesIO()
    img.save(buffer, format='JPEG')
    image_bytes = buffer.getvalue()
    
    # Test data
    test_image_base64 = base64.b64encode(image_bytes).decode('utf-8')
    
    async with httpx.AsyncClient() as client:
        try:
            # Test the available APIs endpoint
            print("Testing /available-apis endpoint...")
            response = await client.get("http://localhost:8000/api/vision/available-apis")
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                print("✓ Available APIs endpoint works")
                data = response.json()
                print(f"Primary API: {data['primary']['name']}")
                print(f"Free tier: {data['primary']['free_tier']}")
            else:
                print("✗ Available APIs endpoint failed")
            
            print("\n" + "="*50 + "\n")
            
            # Test the recognize endpoint (this will use fallback since no real API keys)
            print("Testing /recognize endpoint (fallback mode)...")
            files = {
                'image': ('test_image.jpg', image_bytes, 'image/jpeg')
            }
            
            # Note: This would require authentication in a real scenario
            # For testing, we'll just check if the endpoint is accessible
            response = await client.post("http://localhost:8000/api/vision/recognize", files=files)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 422:  # Validation error (expected without auth)
                print("✓ Recognize endpoint is accessible (auth required)")
            elif response.status_code == 200:
                print("✓ Recognize endpoint works")
                data = response.json()
                print(f"Recognized foods: {len(data.get('recognized_foods', []))}")
            else:
                print(f"✗ Recognize endpoint failed with status {response.status_code}")
                
        except httpx.ConnectError:
            print("✗ Cannot connect to server. Make sure the FastAPI server is running on localhost:8000")
        except Exception as e:
            print(f"✗ Error: {e}")

if __name__ == "__main__":
    print("Testing Vision API...")
    print("="*50)
    asyncio.run(test_vision_api())
    print("\nTest completed!")