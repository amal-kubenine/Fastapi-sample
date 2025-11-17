# FastAPI Hello World Application

A simple FastAPI application for the Civo Kubernetes infrastructure project with automated CI/CD pipeline.

## Features

- Hello World endpoint
- Health check endpoint
- Information endpoint
- Dockerized with multi-stage build
- Kubernetes deployment manifests
- CI/CD pipeline with GitHub Actions
- Automatic deployment to Kubernetes via bastion host

## Project Structure

```
fastapi-app/
├── app/
│   └── main.py              # FastAPI application
├── k8s/
│   ├── deployment.yaml      # Kubernetes deployment
│   ├── service.yaml         # Kubernetes service
│   └── ingress.yaml         # Kubernetes ingress with TLS
├── .github/
│   └── workflows/
│       └── ci-cd.yaml       # GitHub Actions CI/CD pipeline
├── Dockerfile               # Multi-stage Docker build
├── requirements.txt         # Python dependencies
├── .gitignore              # Git ignore rules
├── README.md               # This file
└── GITHUB_SETUP.md         # GitHub setup instructions
```

## Local Development

### Prerequisites

- Python 3.11+
- pip

### Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The application will be available at `http://localhost:8000`

### Endpoints

- `GET /` - Hello World message
- `GET /health` - Health check endpoint
- `GET /api/v1/info` - Application information

## Docker

### Build

```bash
docker build -t fastapi-app:latest .
```

### Run

```bash
docker run -p 8000:8000 fastapi-app:latest
```

## Kubernetes Deployment

The application includes Kubernetes manifests in the `k8s/` directory:

- `deployment.yaml` - Deployment with 2 replicas
- `service.yaml` - ClusterIP service
- `ingress.yaml` - Ingress with TLS via cert-manager

### Manual Deploy

```bash
# Create namespace
kubectl create namespace fastapi

# Deploy
kubectl apply -f k8s/
```

## CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/ci-cd.yaml`) automatically:

1. Builds the Docker image on every push to `main` branch
2. Pushes to Docker Hub with SHA tag and `latest` tag
3. Deploys to Kubernetes via bastion host
4. Verifies deployment status

### Required GitHub Secrets

Configure these in GitHub repository settings:

- `DOCKERHUB_USERNAME` - Docker Hub username
- `DOCKERHUB_TOKEN` - Docker Hub access token
- `BASTION_HOST` - Bastion host public IP
- `BASTION_SSH_KEY` - SSH private key for bastion access

See [GITHUB_SETUP.md](GITHUB_SETUP.md) for detailed setup instructions.

## Deployment Process

1. **Push to GitHub** - Push code to `main` branch
2. **GitHub Actions** - Workflow triggers automatically
3. **Build Image** - Docker image is built and pushed to Docker Hub
4. **Deploy** - Manifests are transferred to bastion and applied
5. **Verify** - Deployment status is verified

## Access

After deployment:

- **Via Ingress**: `https://api.yourdomain.com` (after DNS configuration)
- **Via LoadBalancer**: `http://<PUBLIC_LB_IP>` (temporary, before DNS)

Get LoadBalancer IP:
```bash
kubectl get svc -n ingress-public nginx-public-ingress-nginx-controller
```

## Environment Variables

- `ENVIRONMENT` - Set to "production" in Kubernetes deployment

## Health Checks

The application includes:
- Liveness probe: `/health` endpoint
- Readiness probe: `/health` endpoint
- Docker healthcheck: Built into Dockerfile

## Troubleshooting

### Check Pods
```bash
kubectl get pods -n fastapi
kubectl logs -n fastapi -l app=fastapi-app
```

### Check Services
```bash
kubectl get svc -n fastapi
```

### Check Ingress
```bash
kubectl get ingress -n fastapi
kubectl describe ingress fastapi-app -n fastapi
```

### Check Certificates
```bash
kubectl get certificates -n fastapi
kubectl describe certificate fastapi-app-tls -n fastapi
```

## License

This project is part of the Civo Kubernetes infrastructure deployment.
