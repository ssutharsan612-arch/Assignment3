# SaruganSutharsan_SWS212Lab3

## How to run backend locally
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

## How to run frontend locally
cd frontend
npm install
npm run dev

## Environment variables required
MONGO_URI - my db's login data
SECRET_KEY - generated 32 key

## How to deploy to Render
Backend: Web Service, root directory = backend
Start command: uvicorn main:app --host 0.0.0.0 --port $PORT

Frontend: Static Site, root directory = frontend
Build command: npm install && npm run build
Publish directory: dist
Environment variable: VITE_API_URL = https://assignment3-psvh.onrender.com/

## Example login request
POST /token
username: moo
password: cow
Returns: curl -X 'POST' \
  'https://assignment3-psvh.onrender.com/token' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=password&username=moo&password=cow&scope=&client_id=string&client_secret=********'