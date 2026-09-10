# Python Flask CI/CD with Docker and GitHub Actions

A Python Flask application demonstrating a complete CI/CD workflow using **Docker**, **Docker Hub**, and **GitHub Actions**.

## Project Overview

This project demonstrates:

- Python Flask application development
- Docker containerization
- Docker image building and execution
- `/health` endpoint for health checks
- Automated smoke testing with `curl`
- GitHub Actions CI
- Publishing Docker images to Docker Hub
- GitHub Actions CD
- Pulling and running the published image
- Container and application verification

## Project Structure

```text
python-flask-project/
│
├── app.py
├── Dockerfile
├── requirements.txt
│
└── .github/
    └── workflows/
        ├── python-ci.yaml
        └── python-cd.yaml
```

## Architecture

```text
GitHub Repository
       |
       | git push
       v
python-ci.yaml
       |
       +--> Build Docker Image
       |
       +--> Run Container
       |
       +--> Smoke Test
       |
       +--> Test Application
       |
       +--> Push Image
       |
       v
Docker Hub
       |
       | docker pull
       v
python-cd.yaml
       |
       +--> Run Container
       |
       +--> Verify Application
```

## 1. Flask Application

The main application is in `app.py`.

It provides two endpoints:

### `/`

Displays the Flask CI/CD demonstration web page.

### `/health`

Returns JSON health information and is used by the CI smoke test.

Example response:

```json
{
  "status": "healthy",
  "application": "Flask CI/CD Demo",
  "framework": "Flask",
  "runtime": "Python",
  "container": "Docker",
  "ci_cd": "GitHub Actions"
}
```

## 2. Requirements

`requirements.txt` contains:

```text
flask==3.1.1
```

Install dependencies locally with:

```bash
pip install -r requirements.txt
```

## 3. Dockerfile

The application is containerized with:

```dockerfile
FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]
```

### Dockerfile Instructions

| Instruction | Purpose |
|---|---|
| `FROM` | Selects the Python base image |
| `WORKDIR` | Sets the working directory |
| `COPY` | Copies files into the image |
| `RUN` | Installs dependencies |
| `EXPOSE` | Documents port 5000 |
| `CMD` | Starts Flask |

Flask listens on:

```text
0.0.0.0:5000
```

## 4. Run Locally Without Docker

```bash
python app.py
```

Open:

```text
http://localhost:5000
```

Health endpoint:

```text
http://localhost:5000/health
```

## 5. Build the Docker Image

```bash
docker build -t flask-app:v1.0.0 .
```

Check images:

```bash
docker images
```

## 6. Run the Docker Container

```bash
docker run -p 4000:5000 flask-app:v1.0.0
```

The mapping is:

```text
HOST PORT : CONTAINER PORT
    4000  :       5000
```

Open:

```text
http://localhost:4000
```

Health endpoint:

```text
http://localhost:4000/health
```

### Port Mapping

Docker uses:

```text
-p HOST_PORT:CONTAINER_PORT
```

Examples:

```bash
docker run -p 4000:5000 flask-app:v1.0.0
```

means:

```text
localhost:4000 → container:5000
```

The container port must be `5000` because Flask listens on port `5000`.

## 7. Docker Hub

The Docker image is stored in:

```text
sahsatyajeet/python-flask-app
```

Example image:

```text
sahsatyajeet/python-flask-app:v1.0.0
```

Docker Hub provides persistent storage for the image.

This is important because GitHub-hosted runners are temporary.

## 8. Continuous Integration

The CI workflow is:

```text
.github/workflows/python-ci.yaml
```

The CI pipeline performs:

```text
Checkout
   ↓
Build Docker Image
   ↓
Run Container
   ↓
Verify Container
   ↓
Smoke Test /health
   ↓
Test /
   ↓
Display Logs
   ↓
Cleanup
   ↓
Login to Docker Hub
   ↓
Tag Image
   ↓
Push Image
```

### CI Responsibility

CI answers:

> Does the application build and work correctly?

It verifies that:

- The Docker image can be built.
- The container starts.
- `/health` returns HTTP 200.
- `/` returns HTTP 200.
- The image can be pushed to Docker Hub.

## 9. Smoke Testing

The CI workflow uses `curl`.

Example:

```bash
response=$(curl -s -w "\n%{http_code}" http://localhost:5000/health)
```

The response contains the body and HTTP status code.

Example:

```text
{"status":"healthy", ...}
200
```

The workflow verifies:

```text
HTTP Status Code = 200
```

and that the response contains:

```text
healthy
```

A smoke test is a basic test that confirms the application is running and responding correctly.

## 10. Continuous Deployment

The CD workflow is:

```text
.github/workflows/python-cd.yaml
```

The CD pipeline performs:

```text
CI Successful
      ↓
Login to Docker Hub
      ↓
Pull Docker Image
      ↓
Run Container
      ↓
Verify Container
      ↓
Test Application
      ↓
Display Logs
      ↓
Cleanup
```

### CD Responsibility

CD answers:

> Can the tested Docker image be pulled and run successfully?

## 11. Why Docker Hub Is Used Between CI and CD

GitHub-hosted runners are temporary.

The CI runner builds the image:

```text
CI Runner
    |
    v
Docker Image
    |
    | push
    v
Docker Hub
```

After CI finishes, its runner is discarded.

The CD workflow therefore pulls the image from Docker Hub:

```text
Docker Hub
    |
    | pull
    v
CD Runner
    |
    v
Docker Container
```

Docker Hub acts as the persistent bridge between CI and CD.

## 12. CI vs CD

| CI | CD |
|---|---|
| Continuous Integration | Continuous Deployment |
| Builds application/image | Deploys application/image |
| Runs tests | Runs deployment verification |
| Pushes image | Pulls image |
| Validates code | Validates deployment |

For this project:

```text
CI = Build + Test + Push
CD = Pull + Run + Verify
```

## 13. GitHub Secrets

Create these repository secrets:

```text
DOCKERHUB_USERNAME
DOCKERHUB_TOKEN
```

They are used by the workflows:

```yaml
with:
  username: ${{ secrets.DOCKERHUB_USERNAME }}
  password: ${{ secrets.DOCKERHUB_TOKEN }}
```

A Docker Hub access token should be used instead of storing the Docker Hub password.

## 14. Docker Image Tags

The image uses a version tag:

```text
v1.0.0
```

Complete image name:

```text
sahsatyajeet/python-flask-app:v1.0.0
```

New versions can use:

```text
v1.0.1
v1.0.2
v1.1.0
```

For example:

```bash
docker build -t sahsatyajeet/python-flask-app:v1.0.1 .
docker push sahsatyajeet/python-flask-app:v1.0.1
```

Using different version tags makes it possible to distinguish image versions.

## 15. Pull the Image from Docker Hub

```bash
docker pull sahsatyajeet/python-flask-app:v1.0.0
```

Check:

```bash
docker images
```

## 16. Run the Docker Hub Image Locally

```bash
docker run -p 4000:5000 sahsatyajeet/python-flask-app:v1.0.0
```

To always check Docker Hub before running:

```bash
docker run --pull always -p 4000:5000 sahsatyajeet/python-flask-app:v1.0.0
```

Open:

```text
http://localhost:4000
```

## 17. Useful Docker Commands

### List running containers

```bash
docker ps
```

### List all containers

```bash
docker ps -a
```

### List images

```bash
docker images
```

### Stop a container

```bash
docker stop flask-container
```

### Remove a container

```bash
docker rm flask-container
```

### View container logs

```bash
docker logs flask-container
```

### Run in detached mode

```bash
docker run -d -p 4000:5000 --name flask-container flask-app:v1.0.0
```

## 18. GitHub-Hosted Runner

The workflows use:

```yaml
runs-on: ubuntu-latest
```

GitHub provides a temporary Ubuntu machine to execute the workflow.

The runner performs tasks such as:

```text
Checkout
Build
Run Docker
Test
Push
```

The runner is discarded after the workflow finishes.

Therefore:

```text
CI Runner ≠ CD Runner
```

The Docker image needs to be stored in a registry such as Docker Hub if another workflow needs it.

## 19. Deployment Note

The CD workflow demonstrates deployment by running the Docker container on the GitHub Actions runner.

This is useful for learning and deployment verification, but it is not a permanent production server because the runner is temporary.

A real production deployment could use:

```text
Azure Virtual Machine
Azure Container Apps
Azure Kubernetes Service
Azure App Service
```

A production flow could be:

```text
Developer
   |
   v
GitHub
   |
   v
GitHub Actions CI
   |
   | Build + Test
   v
Docker Hub
   |
   | Pull
   v
Azure / Production Environment
   |
   v
Running Application
```

## 20. Troubleshooting

### Docker daemon error

If an error mentions:

```text
DockerDesktopLinuxEngine
```

make sure Docker Desktop is running.

Verify:

```bash
docker version
```

### Container is unreachable

Check the port mapping:

```bash
docker run -p 4000:5000 flask-app:v1.0.0
```

Do not use:

```bash
docker run -p 5000:80 flask-app:v1.0.0
```

because Flask listens on container port `5000`.

### Check logs

```bash
docker logs flask-container
```

### Check container status

```bash
docker ps
```

### Image not found

Use the complete image name:

```text
sahsatyajeet/python-flask-app:v1.0.0
```

Note that the tag is:

```text
v1.0.0
```

not:

```text
1.0.0
```

## 21. Development Workflow

```text
Modify app.py
      ↓
Test locally
      ↓
Build Docker image
      ↓
Run container
      ↓
Test application
      ↓
Commit changes
      ↓
Push to GitHub
      ↓
GitHub Actions CI
      ↓
Docker Hub
      ↓
GitHub Actions CD
      ↓
Pull image
      ↓
Run container
      ↓
Verify application
```

## 22. Technologies Used

- Python
- Flask
- Docker
- Docker Hub
- Git
- GitHub
- GitHub Actions
- Bash
- curl

## 23. DevOps Concepts Demonstrated

### Continuous Integration

Automatically build and test the application after code changes.

### Continuous Deployment

Use the successfully built image in a deployment workflow.

### Containerization

Package the application and its dependencies into a Docker image.

### Container Registry

Store Docker images in Docker Hub.

### Automated Testing

Use HTTP smoke tests to verify the application.

### Versioned Docker Images

Use tags such as:

```text
v1.0.0
v1.0.1
```

to identify image versions.

## 24. Final CI/CD Flow

```text
                 Developer
                     |
                     | git push
                     v
              GitHub Repository
                     |
                     v
              GitHub Actions CI
                     |
          +----------+----------+
          |                     |
          v                     v
    Build Docker           Run Container
       Image                    |
          |                     v
          |                Smoke Tests
          |                     |
          +----------+----------+
                     |
                  Success
                     |
                     v
                Docker Hub
                     |
                     | Pull Image
                     v
              GitHub Actions CD
                     |
                     v
              Run Container
                     |
                     v
             Verify Application
```

## Conclusion

This project demonstrates a basic but complete Docker-based CI/CD pipeline for a Python Flask application.

The core workflow is:

```text
Code
  ↓
Build
  ↓
Test
  ↓
Docker Image
  ↓
Docker Hub
  ↓
Deploy
  ↓
Verify
```

Possible future improvements include:

- Automated version tagging
- Unit tests with `pytest`
- Docker image security scanning
- Azure deployment
- Terraform infrastructure
- GitHub Actions environments
- Approval gates
- Rollback strategies
- Kubernetes deployment
