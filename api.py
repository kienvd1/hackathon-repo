from fastapi import FastAPI, HTTPException
from _model import ImageRequest, ResultRequest, FaceSwapRequest
import requests


app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}


FLUX_GEN_API = "039af3b8-53c9-4c61-91a7-88be17323c98"

FACE_SWAP_API = "723298c0b51238c378c47e45dec26e5e7a533cb12c69ef8f0e459964706f80c1"


@app.post("/generate-image")
async def generate_image(request: ImageRequest):
    url = "https://api.bfl.ml/v1/flux-pro-1.1-ultra"
    headers = {
        "Content-Type": "application/json",
        "X-Key": FLUX_GEN_API
    }
    
    # Convert width and length to aspect ratio
    aspect_ratio = f"{request.width}:{request.height}"
    
    # Prepare payload for the external API
    payload = {
        "prompt": request.prompt,
        "seed": request.seed,
        "aspect_ratio": aspect_ratio,
        "safety_tolerance": request.safety_tolerance,
        "output_format": request.output_format,
        "raw": request.raw
    }
    
    try:
        # Call the external API
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()  # Return the API response
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/face-swap")
async def face_swap(request: FaceSwapRequest):
    """
    Perform a face swap using the Qubico image toolkit API.
    """
    url = "https://api.piapi.ai/api/v1/task"
    headers = {
        'x-api-key': FACE_SWAP_API,
        'Content-Type': 'application/json'
    }
    payload = {
        "model": "Qubico/image-toolkit",
        "task_type": "face-swap",
        "input": {
            "target_image": request.target_image,
            "swap_image": request.swap_image
        }
    }
    
    try:
        # Send a POST request to the API
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()  # Return the API response as JSON
    except requests.exceptions.RequestException as e:
        # Handle and return any errors
        raise HTTPException(status_code=500, detail=f"Error calling face-swap API: {str(e)}")


@app.get("/get-faceswap-result/{task_id}")
def get_faceswap_result(task_id: str):
    """
    Retrieve the result of a face-swap task using the Qubico image toolkit API.
    
    Parameters:
    - task_id (str): The ID of the face-swap task.

    Returns:
    - JSON response from the API with the task result.
    """
    url = f"https://api.piapi.ai/api/v1/task/{task_id}"
    headers = {
        'x-api-key': FACE_SWAP_API
    }
    
    try:
        # Send a GET request to the API
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()  # Return the API response as JSON
    except requests.exceptions.RequestException as e:
        # Handle and return any errors
        raise HTTPException(status_code=500, detail=f"Error retrieving face-swap result: {str(e)}")



@app.get("/download-result")
def download_result(request: ResultRequest):
    """
    Endpoint to download the result from the external API.
    
    Parameters:
    - id (str): The ID of the result to fetch.

    Returns:
    - JSON response from the external API.
    """
    url = "https://api.bfl.ml/v1/get_result"
    querystring = {"id": request.id}
    
    try:
        # Call the external API
        response = requests.get(url, params=querystring)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()  # Return the JSON response
    except requests.exceptions.RequestException as e:
        # Handle errors and return a proper HTTP exception
        raise HTTPException(status_code=500, detail=str(e))