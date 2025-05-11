from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional

from .services import kmeans_service 

router = APIRouter()

class ClusteringRequest(BaseModel):
    data: List[List[float]]
    n_clusters: int

class ClusteringResponse(BaseModel):
    labels: List[int]

@router.post("/cluster", response_model=ClusteringResponse)
async def cluster(request: ClusteringRequest):
    try:
        labels = kmeans_service.cluster_data(request.data, request.n_clusters)
        return ClusteringResponse(labels=labels)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

class PriceAdjustmentRequest(BaseModel):
    latitude: Optional[float] = Field(None, example=40.7128, description="User's latitude")
    longitude: Optional[float] = Field(None, example=-74.0060, description="User's longitude")
    user_agent: Optional[str] = Field(None, example="Mozilla/5.0 ...", description="User's browser user agent string")
    base_price: float = Field(..., example=50.0, description="The base price to be adjusted")
    device_pixel_ratio: Optional[str] = Field(None, example="2.0", description="User's device pixel ratio")

class PriceAdjustmentResponse(BaseModel):
    original_price: float
    adjusted_price: float
    cluster_assigned: int
    message: str

@router.post("/adjust-price", response_model=PriceAdjustmentResponse)
async def adjust_price(request_data: PriceAdjustmentRequest):
    """
    Adjusts a base price based on user's metadata for dynamic pricing.
    
    ## Description
    This endpoint uses K-means clustering to segment users based on their geographic location, 
    device information, and device pixel ratio. It then applies a price adjustment factor
    according to the assigned segment:
    
    * High Tier (typically USA/Europe users): +10% adjustment
    * Middle Tier (typically Asia users): No adjustment (0%)
    * Low Tier (typically Africa users): -10% adjustment
    
    ## Example Request
    ```json
    {
      "latitude": 40.7128, 
      "longitude": -74.0060,
      "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
      "base_price": 50.0,
      "device_pixel_ratio": "2.0"
    }
    ```
    
    ## Request Data Handling
    - If geolocation (latitude/longitude) is not provided, default coordinates (0,0) are used
    - User agent is parsed to extract device type and OS information
    - All fields except base_price are optional
    """
    try:
        adjusted_price, cluster_label = kmeans_service.get_dynamically_adjusted_price(
            base_price=request_data.base_price,
            latitude=request_data.latitude,
            longitude=request_data.longitude,
            user_agent_string=request_data.user_agent,
            device_pixel_ratio=request_data.device_pixel_ratio
        )
        return PriceAdjustmentResponse(
            original_price=request_data.base_price,
            adjusted_price=adjusted_price,
            cluster_assigned=cluster_label,
            message="Price adjusted successfully based on user profile."
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"An unexpected error occurred: {str(e)}"
        )
