# Thesis Brainstorming

## 📌 Overview
Thesis Brainstorming is a web-based tool that generates unique and diverse thesis ideas for Computer Science students and researchers. It integrates AI-based models from Open-WebUI and Ollama to provide insightful research topics across multiple subfields.

## 🚀 Features
- Covers diverse subfields in Computer Science (Cybersecurity, Networking, Blockchain, etc.).
- Uses Open-WebUI API (primary) and Ollama API (fallback).
- Supports multiple AI models like gemma2:2b, qwen2.5:0.5b, deepseek-r1:1.5b, etc.
- FastAPI backend with Jinja2 templating.
- CORS-enabled for smooth frontend integration.

## 🛠️ Tech Stack
- **Backend:** FastAPI (Python)
- **Frontend:** Jinja2 Templates, HTML/CSS
- **AI Models:** Open-WebUI, Ollama
- **Database:** None (stateless API)
- **Hosting:** Localhost (default), deployable to cloud

## 📂 Folder Structure
```
thesis_brainstorming/
│── static/               # Static assets (CSS, JS, images)
│── templates/            # HTML templates
│── main.py               # FastAPI backend
│── README.md             # Documentation
│── requirements.txt      # Dependencies
```

## ⚡ Installation & Setup

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/your-username/thesis_brainstorming.git
cd thesis_brainstorming
```

### 2️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 3️⃣ Run the Application
```sh
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

### 4️⃣ Access the App
Open your browser and go to:
🔗 [http://localhost:8001/](http://localhost:8001/)

## 📽️ Video Demo
[Watch the demo here](https://drive.google.com/drive/folders/15QZQBIpYqZW7dUDS-qeVQpf7vjm0g2mD?usp=sharing)

## 🔑 API Endpoints
| Method | Endpoint   | Description                   |
|--------|-----------|-------------------------------|
| GET    | /         | Home Page                     |
| POST   | /generate | Generate thesis statements    |
| GET    | /models   | Fetch available AI models     |

## 🛠 Configuration
- Set your API Key in `main.py` (`API_KEY = "your-api-key"`).
- Modify model preferences (`DEFAULT_MODEL = "gemma2:2b"`).
- Adjust CORS settings as needed.

## 🏗️ Future Enhancements
- 🌍 Frontend UI using React.js.
- 🏛️ Database Integration for saving thesis topics.
- 🎙️ Voice Input for thesis generation.

## 🤝 Contributing
Pull requests are welcome! Open an issue for suggestions.

## 📜 License
This project is MIT Licensed. See `LICENSE` for details.

## 👨‍💻 Developed by Udit 🚀

