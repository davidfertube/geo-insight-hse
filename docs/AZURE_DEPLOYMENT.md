# Azure Deployment Guide for Geo-Insight HSE

> Step-by-step guide to deploy your PPE detection system on Azure Container Apps (Free Tier)

## Prerequisites

Before starting, ensure you have:
- Azure Account (Free tier is fine)
- Azure CLI installed on your Mac
- Docker Desktop installed

---

## Step 1: Install Azure CLI (if not installed)

```bash
# Install via Homebrew
brew update && brew install azure-cli

# Verify installation
az --version
```

---

## Step 2: Login to Azure

```bash
# Login to your Azure account (opens browser)
az login

# Verify you're logged in
az account show
```

---

## Step 3: Create Azure Resources

### 3.1 Create Resource Group

```bash
# Create a resource group in your preferred region
az group create \
  --name rg-geo-insight-hse \
  --location eastus
```

### 3.2 Create Container Registry (ACR)

> **For Free Tier**: We'll use GitHub Container Registry (ghcr.io) instead of ACR to save costs. Skip this step.

### 3.3 Create Container Apps Environment

```bash
# Create the Container Apps environment
az containerapp env create \
  --name geo-insight-env \
  --resource-group rg-geo-insight-hse \
  --location eastus
```

---

## Step 4: Build and Push Docker Image

### Option A: Use GitHub Container Registry (FREE) - Recommended

```bash
# Login to GitHub Container Registry
echo $GITHUB_TOKEN | docker login ghcr.io -u davidfertube --password-stdin

# Build the image
cd /Users/david/.gemini/antigravity/playground/solar-belt
docker build -t ghcr.io/davidfertube/geo-insight-hse:latest .

# Push to registry
docker push ghcr.io/davidfertube/geo-insight-hse:latest
```

### Option B: Use Azure Container Registry (if you have ACR)

```bash
# Create ACR (costs money)
az acr create \
  --resource-group rg-geo-insight-hse \
  --name geoinsighthse \
  --sku Basic

# Login to ACR
az acr login --name geoinsighthse

# Build and push
az acr build --registry geoinsighthse --image geo-insight-hse:latest .
```

---

## Step 5: Deploy to Container Apps

```bash
# Deploy the container (using GitHub Container Registry)
az containerapp create \
  --name geo-insight-hse \
  --resource-group rg-geo-insight-hse \
  --environment geo-insight-env \
  --image ghcr.io/davidfertube/geo-insight-hse:latest \
  --target-port 7860 \
  --ingress external \
  --cpu 1 \
  --memory 2Gi \
  --min-replicas 0 \
  --max-replicas 1 \
  --registry-server ghcr.io \
  --registry-username davidfertube \
  --registry-password $GITHUB_TOKEN
```

> **Note**: `--min-replicas 0` enables scale-to-zero for cost savings!

---

## Step 6: Get Your App URL

```bash
# Get the application URL
az containerapp show \
  --name geo-insight-hse \
  --resource-group rg-geo-insight-hse \
  --query properties.configuration.ingress.fqdn \
  --output tsv
```

Your app will be available at: `https://geo-insight-hse.<random>.eastus.azurecontainerapps.io`

---

## Step 7: Set Up CI/CD (Optional)

### Create Azure Service Principal for GitHub Actions

```bash
# Create service principal
az ad sp create-for-rbac \
  --name "geo-insight-hse-deploy" \
  --role contributor \
  --scopes /subscriptions/$(az account show --query id -o tsv)/resourceGroups/rg-geo-insight-hse \
  --sdk-auth
```

### Add Secret to GitHub

1. Go to: https://github.com/davidfertube/geo-insight-hse/settings/secrets/actions
2. Click "New repository secret"
3. Name: `AZURE_CREDENTIALS`
4. Value: Paste the JSON output from the previous command
5. Click "Add secret"

Now every push to `main` will automatically deploy!

---

## Cost Estimation (Free Tier)

| Resource | Free Tier Allowance | Your Usage |
|----------|---------------------|------------|
| Container Apps | 2M requests/month | Well within |
| vCPU | 180,000 vCPU-seconds/month | Scale-to-zero |
| Memory | 360,000 GiB-seconds/month | Minimal usage |
| Ingress | First 2M requests free | Portfolio demos |

**Estimated Monthly Cost: $0** (with scale-to-zero enabled)

---

## Troubleshooting

### Container won't start
```bash
# Check logs
az containerapp logs show \
  --name geo-insight-hse \
  --resource-group rg-geo-insight-hse \
  --follow
```

### Memory issues
```bash
# Increase memory allocation
az containerapp update \
  --name geo-insight-hse \
  --resource-group rg-geo-insight-hse \
  --cpu 2 \
  --memory 4Gi
```

### Delete everything (if needed)
```bash
# Delete the entire resource group
az group delete --name rg-geo-insight-hse --yes --no-wait
```

---

## Success!

After deployment, you'll have:
- Live demo URL for your portfolio
- Automatic HTTPS certificate
- Scale-to-zero for cost savings
- CI/CD pipeline for updates

Add this URL to your portfolio at [davidfernandez.dev](https://davidfernandez.dev)!

---

## Alternative: Hugging Face Spaces (Also Free)

If Azure setup is too complex, you can deploy to Hugging Face Spaces:

1. Go to [huggingface.co/spaces](https://huggingface.co/spaces)
2. Click "Create new Space"
3. Select "Gradio" as SDK
4. Push your code to the Space repo

```bash
# Clone your HF Space
git clone https://huggingface.co/spaces/davidfertube/geo-insight-hse

# Copy files
cp -r /Users/david/.gemini/antigravity/playground/solar-belt/* .

# Push
git add . && git commit -m "Initial deploy" && git push
```

---

*Guide created for Energy Corridor AI Roadmap | January 2026*
