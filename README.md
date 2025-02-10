
 # 📊 Reddit Sentiment Analysis Data Pipeline 🚀

## **🔹 Project Overview**
This project automates **data ingestion, processing, and visualization** using **Apache Airflow, AWS S3, and Streamlit**. It extracts **Reddit posts**, performs **sentiment analysis**, and visualizes insights on a **real-time dashboard**.

👉 **Technologies Used**:
- **ETL & Orchestration**: Apache Airflow  
- **Data Processing**: Pandas, NumPy, PyArrow, TextBlob  
- **Storage**: AWS S3 (Parquet format)  
- **Dashboard**: Streamlit & Plotly  
- **Containerization**: Docker & Kubernetes  
- **CI/CD**: GitHub Actions & Docker Hub  
- **Cloud Deployment**: AWS EC2  

---

## **🔹 Architecture**
```plaintext
🏠 Apache Airflow  ➔  📦 AWS S3 (Data Storage)  ➔  📈 Streamlit Dashboard
```
- **Airflow DAGs** fetch Reddit data, analyze sentiment, and store results in **AWS S3**.
- **Streamlit Dashboard** dynamically pulls data from S3 and visualizes trends.

---

## **🚀 Setup Instructions**
### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/yourusername/Reddit-Sentiment-Analysis-Data-Pipeline.git
cd Reddit-Sentiment-Analysis-Data-Pipeline
```

### **2️⃣ Set Up Environment Variables**
Create a **`.env`** file in the project root and add:
```ini
AWS_ACCESS_KEY=your_aws_access_key
AWS_SECRET_KEY=your_aws_secret_key
S3_BUCKET_NAME=your_s3_bucket_name
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_USER_AGENT=your_reddit_user_agent
```

### **3️⃣ Run the Project Locally (Docker)**
```sh
docker-compose up --build -d
```
- **Airflow UI** → [http://localhost:8080](http://localhost:8080)  
- **Streamlit Dashboard** → [http://localhost:8501](http://localhost:8501)  

---

## **🚀 Deployment via CI/CD (GitHub Actions)**
### **🔹 GitHub Secrets**
Before pushing code, add these **GitHub Secrets** under **Settings → Secrets & Variables**:

| Secret Name           | Description |
|----------------------|-------------|
| `AWS_ACCESS_KEY`      | AWS S3 Access Key |
| `AWS_SECRET_KEY`      | AWS S3 Secret Key |
| `S3_BUCKET_NAME`      | S3 Bucket Name |
| `REDDIT_CLIENT_ID`    | Reddit API Client ID |
| `REDDIT_CLIENT_SECRET` | Reddit API Secret |
| `REDDIT_USER_AGENT`   | Reddit API User Agent |
| `DOCKER_HUB_USERNAME` | Docker Hub Username |
| `DOCKER_HUB_ACCESS_TOKEN` | Docker Hub Token |
| `SERVER_IP`           | AWS EC2 Public IP |
| `SERVER_USER`         | SSH Username (`ubuntu` for AWS) |
| `SSH_PRIVATE_KEY`     | Your `.pem` SSH Key |

### **🔹 How CI/CD Works**
1. **Push to `main` branch** → GitHub Actions **builds & pushes Docker images**.
2. **Deploys to AWS EC2** via SSH.
3. **Pulls latest images & restarts containers automatically**.

---

## **🚀 Manual Deployment (AWS EC2)**
### **1️⃣ SSH into Your EC2 Server**
```sh
ssh -i your-key.pem ubuntu@your-server-ip
```

### **2️⃣ Pull Latest Docker Images**
```sh
docker pull your-dockerhub-username/airflow:latest
docker pull your-dockerhub-username/streamlit-dashboard:latest
```

### **3️⃣ Restart Services**
```sh
docker-compose down
docker-compose up -d
```

---

## **📊 Dashboard Preview**
<p align="center">
  <img src="https://user-images.githubusercontent.com/example/dashboard-preview.png" width="700" alt="Streamlit Dashboard Preview">
</p>

---

## **🔹 Key Features**
✅ **Automated Data Pipeline** – Extract, transform, store & visualize Reddit data.  
✅ **Parallel Processing** – Uses **Airflow CeleryExecutor** with **Redis** for scalability.  
✅ **Secure Deployment** – Manages secrets via **GitHub Secrets & AWS Secrets Manager**.  
✅ **CI/CD Pipeline** – Automates Docker builds & deployment via **GitHub Actions**.  
✅ **Scalable Infrastructure** – Runs as Docker containers, deployable to **AWS, GCP, Kubernetes**.  

---

## **📞 Contact & Contributions**
👨‍💻 **Author**: [Your Name](https://github.com/MadhurDixit13)  
🤝 **Contributions**: PRs are welcome! Open an issue to discuss improvements.  
🌟 **Star this repo** if you found it useful!  

---

## **🔹 License**
This project is licensed under the **MIT License**. Feel free to modify and use it.

---

🚀 **Now, your README is professional, detailed, and CI/CD-ready!** Let me know if you want to add more details! 🚀

