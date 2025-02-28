Redis Clone: Key-Value Store API with Advanced Features
📌 Overview
This project is a Redis-based API built using:

Python (Flask for API)
Redis (For storage & caching)
Role-Based Authentication (Admin/User API keys)
Advanced Redis Features (TTL, Hashes, Queues, Increment/Decrement)
Web UI Dashboard (For easy access)
🔹 Admins can: Set, delete, and manage all keys.
🔹 Users can: Read data but cannot modify it.

📌 Features Implemented
✅ Basic Redis Operations: SET, GET, DELETE, LIST_KEYS
✅ TTL Expiration Handling (EXPIRE, TTL)
✅ Hash Storage (HSET, HGET)
✅ Queue System (ENQUEUE, DEQUEUE)
✅ Role-Based API Authentication (Admin/User)
✅ API Logging (Admins can view logs)
✅ Web UI Dashboard for Interactions

📌 1️⃣ Installation & Setup
✅ Step 1: Clone the Repository
sh
Copy
Edit
git clone https://github.com/your_username/redis-clone.git
cd redis-clone
✅ Step 2: Create a Virtual Environment (Windows)
powershell
Copy
Edit
python -m venv venv
venv\Scripts\activate
✅ Step 3: Install Dependencies
sh
Copy
Edit
pip install -r requirements.txt
✅ Step 4: Install Redis (Windows)
Redis is not natively available on Windows, so follow one of these options:

Option 1: Use Memurai (Easiest for Windows)
1️⃣ Download Memurai
2️⃣ Install & Run:

sh
Copy
Edit
memurai.exe
Option 2: Use Redis for Windows
1️⃣ Download Redis for Windows
2️⃣ Extract & Run:

sh
Copy
Edit
cd "C:\Program Files\Redis"
redis-server.exe
🔹 Check if Redis is Running:

sh
Copy
Edit
redis-cli ping
✅ Expected Output: PONG

📌 2️⃣ Running the Project
✅ Step 1: Start Redis Server
Make sure Redis is running before starting Flask.

sh
Copy
Edit
redis-server
✅ Step 2: Run Flask API
powershell
Copy
Edit
venv\Scripts\activate
python app.py
✅ API should now be running at:
📌 http://127.0.0.1:5000/

✅ Step 3: Open Web UI
Visit:
📌 http://127.0.0.1:5000/

📌 3️⃣ API Endpoints & Usage
🛠 Authentication (API Keys)
🔹 Generate an API Key:

powershell
Copy
Edit
$body = '{"user_id":"admin123", "role":"admin"}'
Invoke-RestMethod -Uri "http://127.0.0.1:5000/generate_key" -Method POST -Body $body -ContentType "application/json"
✅ Response:

json
Copy
Edit
{
    "api_key": "your_admin_api_key",
    "role": "admin"
}
🔹 Basic Redis Operations
✅ Store a Key-Value Pair (Admin Only)

powershell
Copy
Edit
$body = '{"key":"username", "value":"Adithya"}'
Invoke-RestMethod -Uri "http://127.0.0.1:5000/set" -Method POST -Body $body -ContentType "application/json" -Headers @{"X-API-Key"="your_admin_api_key"}
✅ Retrieve a Key (User Can Access)

powershell
Copy
Edit
Invoke-RestMethod -Uri "http://127.0.0.1:5000/get?key=username" -Method GET -Headers @{"X-API-Key"="your_user_api_key"}
✅ Delete a Key (Admin Only)

powershell
Copy
Edit
$body = '{"key":"username"}'
Invoke-RestMethod -Uri "http://127.0.0.1:5000/delete" -Method DELETE -Body $body -ContentType "application/json" -Headers @{"X-API-Key"="your_admin_api_key"}
🔹 Advanced Features
✅ Set Key with TTL (10 seconds)

powershell
Copy
Edit
$body = '{"key":"temp", "value":"test", "ttl":10}'
Invoke-RestMethod -Uri "http://127.0.0.1:5000/set" -Method POST -Body $body -ContentType "application/json" -Headers @{"X-API-Key"="your_admin_api_key"}
✅ Store & Retrieve Hash Values

powershell
Copy
Edit
$body = '{"hash":"user:1", "field":"email", "value":"adithya@example.com"}'
Invoke-RestMethod -Uri "http://127.0.0.1:5000/hset" -Method POST -Body $body -ContentType "application/json" -Headers @{"X-API-Key"="your_admin_api_key"}
powershell
Copy
Edit
Invoke-RestMethod -Uri "http://127.0.0.1:5000/hget?hash=user:1&field=email" -Method GET -Headers @{"X-API-Key"="your_admin_api_key"}
✅ Enqueue & Dequeue

powershell
Copy
Edit
$body = '{"queue":"orders", "value":"Order123"}'
Invoke-RestMethod -Uri "http://127.0.0.1:5000/enqueue" -Method POST -Body $body -ContentType "application/json" -Headers @{"X-API-Key"="your_admin_api_key"}
powershell
Copy
Edit
Invoke-RestMethod -Uri "http://127.0.0.1:5000/dequeue?queue=orders" -Method GET -Headers @{"X-API-Key"="your_admin_api_key"}
📌 4️⃣ Common Errors & Fixes
Error	Fix
Invoke-WebRequest : Cannot bind parameter 'Headers'	Use Invoke-RestMethod instead
Invoke-WebRequest : Not Found	Ensure Redis & Flask API are running
redis.exceptions.ConnectionError	Start Redis using redis-server
PermissionError: Running scripts is disabled on this system	Run Set-ExecutionPolicy Unrestricted -Scope Process in PowerShell
Redis command wrong number of arguments for 'hset'	Update hset to store key-value pairs separately
📌 5️⃣ Deployment
Option 1: Deploy on Render (Free)
1️⃣ Create a Render Web Service
2️⃣ Connect GitHub Repo
3️⃣ Add Redis as a Redis Instance
4️⃣ Set Start Command:

sh
Copy
Edit
gunicorn -w 4 -b 0.0.0.0:5000 app:app
✅ Live API URL: https://your-app.onrender.com

📌 Final Thoughts
This project implements:
✔ Key-Value Store with Redis
✔ Authentication & Role-Based Access
✔ Web UI for Interactions
✔ Deployment-Ready Setup