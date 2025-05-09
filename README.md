# Technical Test

Deployment URL: http://13.54.34.60:3000/

### Pre-requisites:
Please ensure that the following are installed on your system:
- Python3
- NodeJS
- Docker

(Optional) Create and activate virtual environment
```bash
python -m venv <name of your virtual environment>

./<name of venv>/Scripts/activate # Windows
source <name of venv>/Scripts/activate # MacOS / Linux
```

Install required dependencies
```bash
pip install -r requirements.txt
```

### Task 2
1. Navigate to the asr directory
```bash
cd asr
```

2. Build the Docker Image
```bash
docker build -t asr-api-image .
```

3. Run the Docker container
```bash
docker run -d --name asr-api -p 9200:9200 asr-api-image
```

### Task 4 (Local)
1. Navigate to the elastic-backend directory
```bash
cd elastic-backend
```

2. Build and run Docker container
```bash
docker-compose up
```

### Task 5 (Local)
Note: Unfortunately, I was not able to setup Elastic SearchUI successfully within the stipulated time limit. However, I have instead built a simple frontend in React in its place, which is capable of performing basic filtering of the data in the ElasticSearch index.

1. Navigate to the search-ui directory
```bash
cd search-ui
```

2. Run and build the Docker container
```bash
docker-compose up --build
```