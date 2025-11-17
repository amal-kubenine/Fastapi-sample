# GitHub Repository Setup and CI/CD Configuration

## Prerequisites

1. GitHub account
2. Docker Hub account
3. SSH key for bastion access (already configured)

## Step 1: Initialize Git Repository

```bash
cd fastapi-app
git init
git add .
git commit -m "Initial commit: FastAPI application with CI/CD"
```

## Step 2: Create GitHub Repository

1. Go to GitHub and create a new repository (e.g., `fastapi-civo-app`)
2. **Do NOT** initialize with README, .gitignore, or license (we already have these)

## Step 3: Push to GitHub

```bash
# Add remote (replace YOUR_USERNAME and REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# Rename branch to main if needed
git branch -M main

# Push to GitHub
git push -u origin main
```

## Step 4: Configure GitHub Secrets

Go to your GitHub repository → Settings → Secrets and variables → Actions → New repository secret

Add the following secrets:

### Required Secrets

1. **DOCKERHUB_USERNAME**
   - Your Docker Hub username
   - Example: `myusername`

2. **DOCKERHUB_TOKEN**
   - Docker Hub access token (not password)
   - Create at: https://hub.docker.com/settings/security
   - Permissions: Read, Write, Delete

3. **BASTION_HOST**
   - Bastion host public IP address
   - Get from: `cd ../terraform && terraform output -raw bastion_public_ip`
   - Example: `212.2.255.81`

4. **BASTION_SSH_KEY**
   - SSH private key for bastion access
   - Get from: `cat ~/.ssh/id_ed25519_1`
   - **Important**: Include the entire key including `-----BEGIN OPENSSH PRIVATE KEY-----` and `-----END OPENSSH PRIVATE KEY-----`

### How to Get Bastion IP

```bash
cd terraform
terraform output -raw bastion_public_ip
```

### How to Get SSH Key

```bash
cat ~/.ssh/id_ed25519_1
```

Copy the entire output including the BEGIN and END lines.

## Step 5: Update Ingress Domain

Before deploying, update the domain in `k8s/ingress.yaml`:

```yaml
spec:
  tls:
  - hosts:
    - api.yourdomain.com  # Change this
    secretName: fastapi-app-tls
  rules:
  - host: api.yourdomain.com  # Change this
```

Or use a placeholder that you'll update later.

## Step 6: Test the Pipeline

1. Make a small change to the code (e.g., update version in `app/main.py`)
2. Commit and push:
   ```bash
   git add .
   git commit -m "Test CI/CD pipeline"
   git push
   ```
3. Go to GitHub → Actions tab to watch the workflow run

## Step 7: Verify Deployment

After the pipeline completes:

```bash
export BASTION_IP=$(cd ../terraform && terraform output -raw bastion_public_ip)
ssh -i ~/.ssh/id_ed25519_1 civo@$BASTION_IP "export KUBECONFIG=~/.kube/config && kubectl get pods -n fastapi"
```

## CI/CD Pipeline Workflow

The GitHub Actions workflow (`.github/workflows/ci-cd.yaml`) performs:

1. **Checkout code** - Gets the latest code from the repository
2. **Set up Docker Buildx** - Prepares Docker for building
3. **Login to Docker Hub** - Authenticates using secrets
4. **Build Docker image** - Builds the FastAPI app image
5. **Push to Docker Hub** - Pushes image with SHA tag and latest tag
6. **Setup SSH** - Configures SSH for bastion access
7. **Deploy to Kubernetes** - Transfers manifests and applies via bastion
8. **Verify deployment** - Checks that pods, services, and ingress are created

## Troubleshooting

### Pipeline Fails at Docker Login
- Verify `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` are correct
- Ensure Docker Hub token has Read, Write, Delete permissions

### Pipeline Fails at SSH
- Verify `BASTION_HOST` is correct
- Verify `BASTION_SSH_KEY` includes the full key with BEGIN/END lines
- Test SSH manually: `ssh -i ~/.ssh/id_ed25519_1 civo@<BASTION_IP>`

### Pipeline Fails at Deployment
- Check bastion has kubectl configured: `ssh civo@<BASTION_IP> "kubectl get nodes"`
- Verify namespace exists: `kubectl get namespace fastapi`
- Check deployment logs: `kubectl logs -n fastapi -l app=fastapi-app`

### Image Pull Errors
- Verify Docker image was pushed: Check Docker Hub repository
- Verify image name matches in deployment.yaml
- Check image pull secrets if using private registry

## Manual Deployment (Alternative)

If CI/CD is not working, deploy manually:

```bash
# Build and push image
docker build -t YOUR_DOCKERHUB_USERNAME/fastapi-app:latest .
docker push YOUR_DOCKERHUB_USERNAME/fastapi-app:latest

# Update deployment
export BASTION_IP=$(cd ../terraform && terraform output -raw bastion_public_ip)
ssh -i ~/.ssh/id_ed25519_1 civo@$BASTION_IP "export KUBECONFIG=~/.kube/config && kubectl set image deployment/fastapi-app fastapi=YOUR_DOCKERHUB_USERNAME/fastapi-app:latest -n fastapi"
```

## Next Steps

1. Configure DNS to point to the public LoadBalancer IP
2. Update ingress.yaml with your domain
3. Cert-manager will automatically provision TLS certificates
4. Access your FastAPI app at `https://api.yourdomain.com`

