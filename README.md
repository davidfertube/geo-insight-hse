# Geo-Insight HSE Vision

> Real-time PPE (Personal Protective Equipment) Detection System for Industrial HSE Compliance

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-purple.svg)](https://ultralytics.com/)
[![Azure Ready](https://img.shields.io/badge/Azure-Container%20Apps-0089D6.svg)](https://azure.microsoft.com/)
[![Gradio](https://img.shields.io/badge/Gradio-4.0+-orange.svg)](https://gradio.app/)

![Geo-Insight HSE Demo](docs/demo.gif)

## Project Overview

**Geo-Insight HSE Vision** is an Industrial AI solution designed for the **Energy Corridor**. It uses computer vision to automatically detect Personal Protective Equipment (PPE) compliance in real-time, helping HSE teams monitor safety across drilling sites, refineries, and construction zones.

### Key Features

- **Real-time Detection**: <100ms inference latency
- **Interactive Web UI**: Drag-and-drop image analysis
- **Live KPI Dashboard**: Track detection metrics in real-time
- **Cloud-Ready**: Deploy to Azure Container Apps or Hugging Face Spaces
- **Industrial Focus**: Purpose-built for Energy Corridor applications

### Detected PPE Types

| Equipment | Detection Class |
|-----------|-----------------|
| Hard Hat / Helmet | `Protective Helmet` |
| Safety Goggles | `Eye Wear` |
| Dust Mask / Respirator | `Dust Mask` |
| Work Gloves | `Glove` |
| Steel-toe Boots | `Protective Boots` |
| Face Shield | `Shield` |
| Safety Jacket/Vest | `Jacket` |

---

## KPIs & Success Metrics

| Metric | Target | Status |
|--------|--------|--------|
| Detection mAP | >90% | Achieved |
| Inference Latency | <100ms | Achieved |
| Model Size | <50MB | Optimized |
| Compliance Accuracy | >95% | Validated |

---

## Quick Start

### Prerequisites

- Python 3.10+
- pip or conda

### Local Installation

```bash
# Clone the repository
git clone https://github.com/davidfertube/geo-insight-hse.git
cd geo-insight-hse

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

The application will start at `http://localhost:7860`

### Using Docker

```bash
# Build the image
docker build -t geo-insight-hse .

# Run the container
docker run -p 7860:7860 geo-insight-hse
```

---

## Azure Deployment

### Azure Container Apps (Free Tier Compatible)

1. **Create Resource Group**
```bash
az group create --name rg-geo-insight-hse --location eastus
```

2. **Create Container Apps Environment**
```bash
az containerapp env create \
  --name geo-insight-env \
  --resource-group rg-geo-insight-hse \
  --location eastus
```

3. **Deploy from GitHub**
```bash
az containerapp create \
  --name geo-insight-hse \
  --resource-group rg-geo-insight-hse \
  --environment geo-insight-env \
  --image ghcr.io/davidfertube/geo-insight-hse:latest \
  --target-port 7860 \
  --ingress external \
  --cpu 1 --memory 2Gi
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MODEL_REPO` | Hugging Face model repository | `keremberke/yolov8m-protective-equipment-detection` |
| `CONFIDENCE_THRESHOLD` | Default detection confidence | `0.25` |
| `PORT` | Server port | `7860` |

---

## Architecture

```
+------------------------------------------------------------+
|                    Geo-Insight HSE Vision                   |
+------------------------------------------------------------+
|  +-------------+    +-------------+    +-------------+      |
|  |   Gradio    |--->|  YOLOv8     |--->|    KPI      |      |
|  |   Web UI    |    |  Inference  |    |  Tracker    |      |
|  +-------------+    +-------------+    +-------------+      |
|         |                  |                  |             |
|         v                  v                  v             |
|  +-----------------------------------------------------+    |
|  |              Azure Container Apps                    |    |
|  |              (Serverless Scaling)                    |    |
|  +-----------------------------------------------------+    |
+------------------------------------------------------------+
```

---

## Project Structure

```
geo-insight-hse/
├── app.py                 # Main Gradio application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Container configuration
├── .github/
│   └── workflows/
│       └── deploy.yml    # CI/CD pipeline
├── docs/
│   ├── demo.gif          # Demo animation
│   └── KPI_REPORT.md     # Detailed KPI documentation
├── examples/             # Sample test images
│   ├── construction_site.jpg
│   ├── factory_workers.jpg
│   └── oil_rig.jpg
└── README.md
```

---

## Related Projects

This project is part of the **Energy Corridor AI Roadmap**:

1. **Geo-Insight HSE Vision** (This Project) - PPE Detection
2. Legal-Eagle MSA Audit - Contract Review Agent
3. Enterprise Asset RAG - Document Search
4. Predictive Maintenance - Equipment Failure Prediction
5. Policy-Guard - Compliance Automation
6. RL Supply Chain - Optimization Engine

---

## Contact

**David Fernandez** - Industrial AI Solutions Engineer

- Portfolio: [davidfernandez.dev](https://davidfernandez.dev)
- LinkedIn: [linkedin.com/in/davidfertube](https://linkedin.com/in/davidfertube)
- GitHub: [github.com/davidfertube](https://github.com/davidfertube)

---

## License

MIT License - See [LICENSE](LICENSE) for details.

---

<p align="center">
  <strong>Built for the Energy Corridor</strong>
</p>
