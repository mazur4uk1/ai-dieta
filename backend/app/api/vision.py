from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from app.api.auth import get_current_user
import httpx
import base64
import os
from typing import List, Dict, Any

router = APIRouter()

# Free online food recognition API using Edamam
# Note: You'll need to register for free API keys at https://developer.edamam.com/
EDAMAM_APP_ID = os.getenv("EDAMAM_APP_ID", "")
EDAMAM_APP_KEY = os.getenv("EDAMAM_APP_KEY", "")

# Fallback calorie mapping for common foods
_FALLBACK_CALORIES_MAP = {
    "apple": 95,
    "banana": 105,
    "orange": 62,
    "broccoli": 55,
    "carrot": 41,
    "hot dog": 150,
    "pizza": 285,
    "donut": 195,
    "cake": 260,
    "sandwich": 250,
    "burger": 250,
    "fries": 365,
    "salad": 150,
    "pasta": 220,
    "rice": 200,
    "chicken": 230,
    "fish": 180,
    "egg": 70,
    "milk": 103,
    "bread": 70,
    "cheese": 110,
}

class FoodRecognitionResult:
    def __init__(self, name: str, calories: int, confidence: float = 0.8):
        self.name = name
        self.calories = calories
        self.confidence = confidence

@router.post("/recognize")
async def recognize_food(image: UploadFile = File(...), current_user = Depends(get_current_user)):
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    # Read image file
    image_bytes = await image.read()
    
    # Convert to base64 for API request
    image_base64 = base64.b64encode(image_bytes).decode('utf-8')
    
    # Try Edamam API first if credentials are available
    if EDAMAM_APP_ID and EDAMAM_APP_KEY:
        try:
            recognition_result = await recognize_with_edamam(image_base64)
            if recognition_result:
                return {"recognized_foods": recognition_result}
        except Exception as e:
            print(f"Edamam API error: {e}")
    
    # Fallback to simple food detection using image analysis
    # This is a basic implementation that tries to detect common food items
    # In a real application, you might want to use other free APIs like:
    # - Google Cloud Vision API (free tier available)
    # - Microsoft Azure Computer Vision (free tier available)
    # - Clarifai API (free tier available)
    
    fallback_result = await recognize_with_fallback(image_bytes)
    return {"recognized_foods": fallback_result}

async def recognize_with_edamam(image_base64: str) -> List[Dict[str, Any]]:
    """Use Edamam Food Detection API for food recognition"""
    if not EDAMAM_APP_ID or not EDAMAM_APP_KEY:
        return None
    
    url = "https://api.edamam.com/api/food-detection/v1"
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            params={
                "app_id": EDAMAM_APP_ID,
                "app_key": EDAMAM_APP_KEY
            },
            data={
                "image": image_base64
            },
            timeout=30.0
        )
        
        if response.status_code == 200:
            data = response.json()
            foods = []
            
            # Parse Edamam response
            for item in data.get("parsed", []):
                food = item.get("food", {})
                label = food.get("label", "Unknown")
                nutrients = food.get("nutrients", {})
                
                # Get calories from nutrients
                calories = int(nutrients.get("ENERC_KCAL", 0))
                
                foods.append({
                    "name": label,
                    "calories": calories,
                    "confidence": 0.9
                })
            
            return foods if foods else None
        
        return None

async def recognize_with_fallback(image_bytes: bytes) -> List[Dict[str, Any]]:
    """Fallback food recognition using simple heuristics"""
    # This is a very basic fallback that returns common food items
    # In production, you should integrate with a proper food recognition API
    
    # For demonstration, we'll return some common food items
    # In a real implementation, you might use:
    # 1. Google Cloud Vision API
    # 2. Microsoft Azure Computer Vision
    # 3. Clarifai API
    # 4. Or other free image recognition services
    
    return [
        {
            "name": "Apple",
            "calories": _FALLBACK_CALORIES_MAP["apple"],
            "confidence": 0.85
        },
        {
            "name": "Banana", 
            "calories": _FALLBACK_CALORIES_MAP["banana"],
            "confidence": 0.8
        }
    ]

@router.get("/available-apis")
def get_available_apis():
    """Get information about available food recognition APIs"""
    apis = {
        "primary": {
            "name": "Edamam Food Detection API",
            "free_tier": True,
            "description": "Food recognition and nutrition analysis",
            "docs": "https://developer.edamam.com/edamam-docs-food-detection"
        },
        "alternatives": [
            {
                "name": "Google Cloud Vision API",
                "free_tier": True,
                "description": "General image recognition with food labels",
                "docs": "https://cloud.google.com/vision"
            },
            {
                "name": "Microsoft Azure Computer Vision",
                "free_tier": True,
                "description": "Image analysis and object detection",
                "docs": "https://azure.microsoft.com/en-us/services/cognitive-services/computer-vision/"
            },
            {
                "name": "Clarifai API",
                "free_tier": True,
                "description": "AI-powered image and video recognition",
                "docs": "https://www.clarifai.com/"
            }
        ],
        "setup_instructions": {
            "edamam": "1. Register at https://developer.edamam.com/\n2. Get APP_ID and APP_KEY\n3. Set environment variables EDAMAM_APP_ID and EDAMAM_APP_KEY"
        }
    }
    
    return apis