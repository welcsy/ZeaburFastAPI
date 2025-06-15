# Tuya Fingerbot API

This is a FastAPI-based RESTful API for controlling a Tuya Zigbee Fingerbot device using the [tuya-connector-python](https://github.com/tuya/tuya-connector-python) SDK. The API allows you to send commands (e.g., turn on/off, set modes), query device status, and retrieve supported functions. The project is designed to be deployed on [Zeabur](https://zeabur.com/), a platform-as-a-service for easy deployment.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running Locally](#running-locally)
- [API Endpoints](#api-endpoints)
- [Deploying to Zeabur](#deploying-to-zeabur)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Features

- Control Tuya Zigbee Fingerbot via REST API (e.g., turn on/off, set click mode).
- Query device status and supported functions.
- Built with FastAPI for high-performance asynchronous processing.
- Deployable to Zeabur using Docker.
- Environment variable support for secure configuration.

## Prerequisites

- Python 3.12+
- A Tuya IoT Platform account ([Tuya IoT Platform](https://iot.tuya.com/)).
- A Tuya Zigbee Gateway and Fingerbot device paired via the Tuya Smart Life app.
- [Zeabur](https://zeabur.com/) account for deployment.
- Git and Docker installed (for local testing and deployment).

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt 
   ```
   The requirements.txt includes:
   ```text
   tuya-connector-python==0.1.2
   fastapi==0.115.2
   dotenv==1.0.1
   uvicorn==0.34.3
   ```
3. Set up environment variables: Create a .env file in the project root with the following:
   ```env
   TUYA_ACCESS_ID=your_access_id
   TUYA_ACCESS_SECRET=your_access_secret
   TUYA_API_ENDPOINT=https://openapi-sg.iotbing.com
   ```
   - Obtain TUYA_ACCESS_ID and TUYA_ACCESS_SECRET from the Tuya IoT Platform cloud page.
   - Set TUYA_API_ENDPOINT based on your data center (e.g., https://openapi-sg.iotbing.com for Taiwan).

## Configuration

- Tuya IoT Platform:
  - Create a project in the Tuya IoT Platform > cloud > project management.
  - Link your Zigbee Gateway and Fingerbot device in the Tuya Smart app.
  - Note the device_id of your Fingerbot (e.g., a31dsa2454sfvfdd9fdsyo).
- Environment Variables:
  - Do not commit the .env file to GitHub (excluded in .gitignore).
  - Configure these variables in Zeabur's environment settings during deployment.

## Running Locally
1. Start the FastAPI server:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```
2. Access the API:
   - Open http://localhost:8000/docs in a browser to view the interactive Swagger UI.
   - Test endpoints using cURL or tools like Postman.

   Example: Send a command to turn on the Fingerbot:
   ```bash
   curl -X POST http://localhost:8000/devices/a31dsa2454sfvfdd9fdsyo/commands \
   -H "Content-Type: application/json" \
   -d "{\"code\": \"switch_1\", \"value\": true}"
   ```

## API Endpoints

|Method|Endpoint|Description|Request Body|
|---|---|---|---|
|GET|/devices/{device_id}/functions|Get supported device functions|N/A|
|GET|/devices/{device_id}/status|Get current device status|N/A|
|POST|/devices/{device_id}/commands|Send a control command|{"code": "switch_1", "value": true}|

- Replace {device_id} with your Fingerbot's device ID (e.g., a31dsa2454sfvfdd9fdsyo).
- Check the /functions endpoint to confirm valid code values. If switch_1 is not supported, use the correct code from the /functions response.

## Deploying to Zeabur

1. Push to GitHub:
   - Ensure .env is excluded via .gitignore.
   - Push your code to a GitHub repository:
    ```bash
    git add .
    git commit -m "Prepare for Zeabur deployment"
    git push origin main
    ``` 

2. Create a Zeabur project:
   - Log in to https://zeabur.com/.
   - Create a new project and connect your GitHub repository.

3. Set environment variables:
   - In Zeabur's project settings, add:
   ```text
   TUYA_ACCESS_ID=your_access_id
   TUYA_ACCESS_SECRET=your_access_secret
   TUYA_API_ENDPOINT=https://openapi-sg.iotbing.com
   ```

4. Deploy:
   - Zeabur will detect the Dockerfile and requirements.txt.
   - Click "Deploy" to build and deploy the application.
   - Once deployed, Zeabur provides a public URL (e.g., https://your-project.zeabur.app).

5. Test the deployed API:
    ```bash
    curl -X POST https://your-project.zeabur.app/devices/a31dsa2454sfvfdd9fdsyo/commands \
    -H "Content-Type: application/json" \
    -d "{\"code\": \"switch_1\", \"value\": true}"
    ```

## Troubleshooting

- API returns errors:
  - Check Zeabur logs for details.
  - Verify environment variables are correctly set in Zeabur.
  - Ensure the device_id and code (e.g., switch_1) are valid (use /functions endpoint).
- Fingerbot not responding:
  - Confirm the device and Zigbee Gateway are online in the Tuya Smart app.
  - Test commands manually in the Tuya Smart app to isolate issues.
- Deployment fails:
  - Check Dockerfile syntax and requirements.txt for missing dependencies.
  - Test the Docker build locally:
    ```bash
    docker build -t tuya-api .
    docker run -p 8000:8000 tuya-api
    ```

## Contributing

Contributions are welcome! Please:
1. Fork the repository.
2. Create a feature branch (git checkout -b feature/your-feature).
3. Commit changes (git commit -m "Add your feature").
4. Push to the branch (git push origin feature/your-feature).
5. Open a pull request.

## License

Copyright (c) 2025 welcsy
This project is licensed under the BSD 3-Clause License. See [LICENSE](license) file for details.
