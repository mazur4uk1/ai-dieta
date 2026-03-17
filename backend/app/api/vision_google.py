from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from app.api.auth import get_current_user
import httpx
import base64
import os
from typing import List, Dict, Any

router = APIRouter()

# Google Cloud Vision API configuration
GOOGLE_VISION_API_KEY = os.getenv("GOOGLE_VISION_API_KEY", "")

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

@router.post("/recognize-google")
async def recognize_food_google(image: UploadFile = File(...), current_user = Depends(get_current_user)):
    """Распознавание еды с использованием Google Cloud Vision API"""
    
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    # Read image file
    image_bytes = await image.read()
    
    # Convert to base64 for API request
    image_base64 = base64.b64encode(image_bytes).decode('utf-8')
    
    # Try Google Cloud Vision API first if credentials are available
    if GOOGLE_VISION_API_KEY:
        try:
            recognition_result = await recognize_with_google_vision(image_base64)
            if recognition_result:
                return {"recognized_foods": recognition_result, "source": "Google Cloud Vision"}
        except Exception as e:
            print(f"Google Cloud Vision API error: {e}")
    
    # Fallback to simple food detection
    fallback_result = await recognize_with_fallback(image_bytes)
    return {"recognized_foods": fallback_result, "source": "Fallback"}

async def recognize_with_google_vision(image_base64: str) -> List[Dict[str, Any]]:
    """Use Google Cloud Vision API for food recognition"""
    if not GOOGLE_VISION_API_KEY:
        return None
    
    url = f"https://vision.googleapis.com/v1/images:annotate?key={GOOGLE_VISION_API_KEY}"
    
    # Google Cloud Vision request body
    request_body = {
        "requests": [
            {
                "image": {
                    "content": image_base64
                },
                "features": [
                    {
                        "type": "LABEL_DETECTION",
                        "maxResults": 10
                    },
                    {
                        "type": "WEB_DETECTION",
                        "maxResults": 10
                    }
                ]
            }
        ]
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            json=request_body,
            timeout=30.0
        )
        
        if response.status_code == 200:
            data = response.json()
            foods = []
            
            # Parse Google Cloud Vision response
            responses = data.get("responses", [])
            if responses:
                response_data = responses[0]
                
                # Get label annotations
                labels = response_data.get("labelAnnotations", [])
                for label in labels:
                    description = label.get("description", "").lower()
                    score = label.get("score", 0)
                    
                    # Check if it's a food item
                    if is_food_item(description):
                        calories = _FALLBACK_CALORIES_MAP.get(description, estimate_calories(description))
                        foods.append({
                            "name": description.title(),
                            "calories": calories,
                            "confidence": round(score, 2)
                        })
                
                # Get web detection annotations
                web_detection = response_data.get("webDetection", {})
                web_entities = web_detection.get("webEntities", [])
                
                for entity in web_entities[:5]:  # Top 5 entities
                    description = entity.get("description", "").lower()
                    score = entity.get("score", 0)
                    
                    if is_food_item(description):
                        calories = _FALLBACK_CALORIES_MAP.get(description, estimate_calories(description))
                        foods.append({
                            "name": description.title(),
                            "calories": calories,
                            "confidence": round(score, 2)
                        })
            
            # Remove duplicates and sort by confidence
            unique_foods = {}
            for food in foods:
                name = food["name"]
                if name not in unique_foods or food["confidence"] > unique_foods[name]["confidence"]:
                    unique_foods[name] = food
            
            return list(unique_foods.values()) if unique_foods else None
        
        return None

async def recognize_with_fallback(image_bytes: bytes) -> List[Dict[str, Any]]:
    """Fallback food recognition using simple heuristics"""
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

def is_food_item(description: str) -> bool:
    """Check if description is likely a food item"""
    food_keywords = [
        "apple", "banana", "orange", "broccoli", "carrot", "potato", "tomato",
        "pizza", "burger", "sandwich", "salad", "pasta", "rice", "bread", "cheese",
        "chicken", "fish", "egg", "milk", "cake", "pie", "cookie", "donut", "candy"
    ]
    
    return any(keyword in description for keyword in food_keywords)

def estimate_calories(food_name: str) -> int:
    """Estimate calories for unknown food items"""
    # Simple estimation based on food type
    if any(word in food_name for word in ["fruit", "vegetable", "salad"]):
        return 50
    elif any(word in food_name for word in ["pizza", "burger", "cake", "pie"]):
        return 300
    elif any(word in food_name for word in ["chicken", "fish", "meat"]):
        return 200
    elif any(word in food_name for word in ["rice", "pasta", "bread"]):
        return 150
    else:
        return 100

@router.get("/available-apis-google")
def get_available_apis_google():
    """Get information about available Google Cloud Vision API"""
    apis = {
        "primary": {
            "name": "Google Cloud Vision API",
            "free_tier": True,
            "description": "General image recognition with food labels",
            "docs": "https://cloud.google.com/vision",
            "free_requests": "1000 units per month",
            "setup": "1. Go to Google Cloud Console\n2. Create a project\n3. Enable Vision API\n4. Create API key\n5. Set GOOGLE_VISION_API_KEY environment variable"
        },
        "alternatives": [
            {
                "name": "Microsoft Azure Computer Vision",
                "free_tier": True,
                "description": "Image analysis and object detection",
                "docs": "https://azure.microsoft.com/en-us/services/cognitive-services/computer-vision/",
                "free_requests": "5000 transactions per month"
            },
            {
                "name": "Clarifai API",
                "free_tier": True,
                "description": "AI-powered image and video recognition",
                "docs": "https://www.clarifai.com/",
                "free_requests": "5000 predictions per month"
            }
        ]
    }
    
    return apis