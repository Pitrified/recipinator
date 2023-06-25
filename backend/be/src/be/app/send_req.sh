curl -X 'POST' \
  'http://localhost:8000/recipe/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "string",
  "caption_original": "string",
  "caption_clean": "string",
  "has_url_media": true,
  "has_video_url_media": true,
  "author_id": 1,
  "author": {
    "id": 1,
    "name": "string"
  }
}'