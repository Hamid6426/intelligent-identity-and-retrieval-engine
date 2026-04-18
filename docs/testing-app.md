# App Testing Guide

The FastAPI application provides beautiful, live Swagger documentation at `http://localhost:8000/docs`. However, if you prefer using the terminal or Postman, here are the core commands to validate the Hackathon requirements.

## 1. Checking the API Gateway
Verify that the services are online and responding. CURL work with Git Bash

```bash
curl -X GET http://localhost:8000/
# Expected: {"message": "Welcome to Grabpic API", "status": "online"}
```

## 2. Ingesting Raw Photos (Storage Crawler)
Before triggering this, ensure you have placed sample photos into the `/storage` directory on your local machine relative to the project root.

```bash
curl -X POST http://localhost:8000/ingest
# Expected: {"message": "Ingestion started in the background."}
```
*Note: Since DeepFace runs asynchronously here, watch the Docker logs to see when it finishes tagging and storing vectors!*

## 3. Review Generated Identification (Helper)
You can list the generated User Identities (`grab_id`s) to easily grab one.
```bash
curl -X GET http://localhost:8000/identities
# Expected: 
# {
#   "total": 1, 
#   "identities": [{"grab_id": "c138-uuid-here", "face_appearances": 3, "created_at": "..."}]
# }
```

## 4. Selfie Authentication
Upload an image representing the face you want to query. The system runs the `pgvector` nearest neighbor query to act as an authentication gateway.

*(You must replace `@/absolute/path/to/selfie.jpg` with a real path on your local device).*
```bash
curl -X POST http://localhost:8000/authenticate \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/absolute/path/to/selfie.jpg"

# Expected Output:
# {
#   "message": "Authentication successful",
#   "grab_id": "c138-uuid-here",
#   "distance": 0.05
# }
```

## 5. Data Extraction (Asset Fetching)
Once you receive the `grab_id` authorizing the user, supply it as your key to fetch all their mapped raw photos.
```bash
curl -X GET http://localhost:8000/images/YOUR-GRAB-ID
# Expected Output:
# {
#   "grab_id": "c138-uuid-here",
#   "image_count": 2,
#   "images": [
#     "storage/DSC0001.jpg", 
#     "storage/DSC0059_group.jpg"
#   ]
# }
```
