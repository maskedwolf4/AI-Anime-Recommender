# AniMatch — AI Anime Recommender 🎌

AniMatch is an Artificial Intelligence-powered anime recommendation system. It leverages Large Language Models (LLMs) and Vector Databases to provide highly personalized, context-aware anime suggestions based on natural language queries. 

Currently built with **Streamlit**, **LangChain**, **ChromaDB**, and **Groq**, the project is containerized using **Docker** and deployed on a local Kubernetes cluster using **Minikube**. The system's health and metrics are monitored via **Grafana Cloud**.

## 🏗️ Architecture

The system consists of three main components:

1. **Data Ingestion & Vectorization (`src/`, `build_pipeline.py`)**
   - Anime metadata (plots, genres, etc.) is loaded and processed.
   - Text descriptions are converted into deep semantic embeddings using **HuggingFace** models.
   - The embeddings and metadata are stored in a local **ChromaDB** vector database (`chroma_db/`) for fast semantic retrieval.

2. **Inference Pipeline (`pipeline/pipeline.py`, `src/recommender.py`)**
   - Retrieves the most relevant anime from ChromaDB based on user queries (e.g., "lighthearted school anime with comedy").
   - A **LangChain** prompt orchestrates the context formulation.
   - A powerful LLM hosted on **Groq** processes the context and natural language query to generate structured, personalized recommendations (including plot summaries and matching reasons).

3. **Frontend Application (`app/app.py`)**
   - Built with **Streamlit** to provide a sleek, dark-mode, neon-styled interactive User Interface.
   - Accepts user queries, triggers the pipeline, parses the structured output, and displays "Anime Cards" formatted seamlessly.

---

## 🚀 End-to-End Deployment

The project is designed to be easily deployed to a Kubernetes cluster. Below is the workflow for deploying to **Minikube** running on an Ubuntu VM instance (e.g., Google Cloud Platform).

### 1. GCP VM & Minikube Setup
1. Provision a VM on Google Cloud Platform (e.g., Ubuntu 24.04 LTS, 16GB RAM, 256GB Disk).
2. Connect to the VM instance.
3. Install **Docker** and configure it to run without `sudo` (`sudo usermod -aG docker $USER`).
4. Install **Minikube** and **kubectl**.
5. Start the cluster:
   ```bash
   minikube start
   ```

### 2. Build & Deploy
1. Clone the repository on the VM.
2. Point your terminal's Docker daemon to Minikube:
   ```bash
   eval $(minikube -p minikube docker-env)
   ```
3. Build the Docker image directly inside the Minikube environment:
   ```bash
   docker build -t llmops-app:latest .
   ```
4. Create the required Kubernetes secrets for the APIs:
   ```bash
   kubectl create secret generic llmops-secrets \
     --from-literal=GROQ_API_KEY="your-groq-key" \
     --from-literal=HUGGINGFACEHUB_API_TOKEN="your-hf-token"
   ```
5. Apply the deployment and service manifests:
   ```bash
   kubectl apply -f llmops-k8s.yaml
   ```

### 3. Exposing the Application
1. In one terminal, create a Minikube tunnel:
   ```bash
   minikube tunnel
   ```
2. In another terminal, port-forward the service to expose it publicly:
   ```bash
   kubectl port-forward svc/llmops-service 8501:80 --address 0.0.0.0
   ```
3. Access the application in your browser via `http://<VM-EXTERNAL-IP>:8501`.

---

## 📊 Monitoring with Grafana Cloud

To keep track of the Kubernetes cluster (Minikube) performance, logs, and resource usage, the project is integrated with **Grafana Cloud Monitoring**.

### Setup Instructions
1. Create a `monitoring` namespace:
   ```bash
   kubectl create ns monitoring
   ```
2. Install **Helm** on your VM.
3. In your Grafana Cloud dashboard, navigate to **Connections > Kubernetes**.
4. Generate a new Access Token (e.g., `minikube-token`).
5. Grafana will provide a Helm configuration file snippet. Save the configuration block into a local `values.yaml` file.
6. Install the monitoring charts using the values:
   ```bash
   helm repo add grafana https://grafana.github.io/helm-charts && \
   helm repo update && \
   helm upgrade --install --atomic --timeout 300s grafana-k8s-monitoring grafana/k8s-monitoring \
     --namespace "monitoring" --create-namespace --values values.yaml
   ```
7. Verify the pods are running:
   ```bash
   kubectl get pods -n monitoring
   ```
8. Return to Grafana Cloud to visualize your cluster metrics in real-time.

---

## 🔮 Future Additions

While the current architecture leverages Streamlit for rapid prototyping and deployment, the roadmap includes completely decoupling the system into a modern, robust, two-tier architecture:

### 1. Robust FastAPI Backend
- Replace the Streamlit monolith with a dedicated **FastAPI** RESTful backend.
- This will expose dedicated API endpoints (e.g., `/api/v1/recommend`, `/api/v1/ingest`).
- **Benefits**: Better performance, asynchronous handling of LLM streams, scalability, and swagger/openapi documentation caching.

### 2. Dedicated React Frontend
- Rebuild the user interface using **React** (or Next.js).
- Implement a more responsive, dynamic single-page application (SPA).
- Provide richer animations, skeleton loaders while waiting for Groq, and user authentication to store watch-lists or history.
- **Benefits**: Separation of concerns, significantly improved UX/UI capabilities, and decoupled horizontal scaling.
