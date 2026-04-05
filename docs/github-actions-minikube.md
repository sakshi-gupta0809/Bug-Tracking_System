# GitHub Actions Pipeline for Minikube

This repository includes a GitHub Actions pipeline that builds and deploys the Bug Tracking application to Minikube for testing and validation.

## Pipeline Overview

The pipeline consists of two main jobs:

### 1. Test Job
- **Trigger**: On push to main/develop branches or pull requests
- **Actions**:
  - Sets up Python 3.9 environment
  - Installs dependencies from `requirements.txt`
  - Runs tests using pytest
- **Purpose**: Ensures code quality before deployment

### 2. Build and Deploy Job
- **Trigger**: Runs after successful test completion
- **Actions**:
  - Builds Docker image locally
  - Sets up Minikube cluster
  - Loads Docker image into Minikube
  - Deploys application using Kubernetes manifests
  - Verifies deployment and tests endpoint
  - Cleans up resources

## Key Features

- **Minikube Integration**: Uses `medyagh/setup-minikube` action for cluster setup
- **Local Docker Images**: Builds and uses local Docker images instead of registry
- **Namespace Isolation**: Deploys to `devsecops` namespace
- **Health Checks**: Waits for deployment readiness and tests service endpoint
- **Automatic Cleanup**: Removes namespace and stops Minikube after completion

## Usage

1. **Push to main/develop**: Triggers the full pipeline
2. **Create Pull Request**: Triggers test job only
3. **Manual Trigger**: Not configured by default but can be added

## Prerequisites

- GitHub repository with this workflow
- Dockerfile in repository root
- Kubernetes manifests in `manifests/` directory
- Test files in `tests/` directory

## Configuration Notes

- Uses Python 3.9 to match the Dockerfile
- Minikube driver: Docker
- Kubernetes version: v1.28.3
- Service type: NodePort (for Minikube access)
- Image: Built locally as `bug-tracker:latest`

## Troubleshooting

- Check logs in GitHub Actions tab
- Verify Minikube status in workflow logs
- Ensure all required files are present
- Check namespace and deployment names match manifests
