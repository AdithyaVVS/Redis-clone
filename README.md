# Redis Clone API

A robust Redis-based API implementation featuring role-based authentication, advanced Redis operations, and a web UI dashboard. Built with Python Flask and Redis, this project demonstrates key-value store operations with enterprise-grade features.

## 🚀 Features

- **Core Redis Operations**
  - SET, GET, DELETE, LIST_KEYS operations
  - TTL (Time-To-Live) support
  - Hash storage (HSET, HGET)
  - Queue system (ENQUEUE, DEQUEUE)

- **Security**
  - Role-based authentication (Admin/User)
  - API key management
  - Request logging

- **User Interface**
  - Web dashboard for easy interaction
  - Real-time data visualization

## 🛠️ Prerequisites

- Python 3.7+
- Redis server (Windows alternatives available)
- PowerShell (for Windows users)

## 📦 Installation

1. **Clone the repository**
   ```powershell
   git clone https://github.com/your_username/redis-clone.git
   cd redis-clone
   ```

2. **Set up Python environment**
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Install Redis (Windows Options)**

   **Option A: Memurai (Recommended for Windows)**
   - Download and install [Memurai](https://www.memurai.com/)
   - Run with: `memurai.exe`

   **Option B: Redis for Windows**
   - Download [Redis for Windows](https://github.com/microsoftarchive/redis/releases)
   - Extract and run:
     ```powershell
     cd "C:\Program Files\Redis"
     .\redis-server.exe
     ```

## 🚀 Getting Started

1. **Start Redis Server**
   ```powershell
   redis-server
   ```

2. **Launch the API**
   ```powershell
   .\venv\Scripts\activate
   python app.py
   ```
   Access the web UI at: http://127.0.0.1:5000

## 🔑 API Usage

### Authentication

```powershell
# Generate API Key
$body = '{"user_id":"admin123", "role":"admin"}'
Invoke-RestMethod -Uri "http://127.0.0.1:5000/generate_key" -Method POST -Body $body -ContentType "application/json"
```

### Basic Operations

```powershell
# Set Key (Admin)
$body = '{"key":"username", "value":"Adithya"}'
Invoke-RestMethod -Uri "http://127.0.0.1:5000/set" -Method POST -Body $body -ContentType "application/json" -Headers @{"X-API-Key"="your_admin_api_key"}

# Get Key (User/Admin)
Invoke-RestMethod -Uri "http://127.0.0.1:5000/get?key=username" -Method GET -Headers @{"X-API-Key"="your_api_key"}
```

### Advanced Features

```powershell
# Set with TTL
$body = '{"key":"temp", "value":"test", "ttl":10}'
Invoke-RestMethod -Uri "http://127.0.0.1:5000/set" -Method POST -Body $body -ContentType "application/json" -Headers @{"X-API-Key"="your_admin_api_key"}

# Hash Operations
$body = '{"hash":"user:1", "field":"email", "value":"user@example.com"}'
Invoke-RestMethod -Uri "http://127.0.0.1:5000/hset" -Method POST -Body $body -ContentType "application/json" -Headers @{"X-API-Key"="your_admin_api_key"}
```

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| `Invoke-WebRequest: Cannot bind parameter 'Headers'` | Use `Invoke-RestMethod` instead |
| `redis.exceptions.ConnectionError` | Ensure Redis server is running |
| `PermissionError: Running scripts disabled` | Run `Set-ExecutionPolicy Unrestricted -Scope Process` |

## 🌐 Deployment

### Deploy on Railway (Free Tier)

1. Sign up for [Railway](https://railway.app) with GitHub
2. Create a new project and select "Deploy from GitHub repo"
3. Connect your GitHub repository
4. Add Redis plugin from the Railway dashboard
5. Railway will automatically deploy your application

For detailed instructions, see [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md)

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.