# Thesis Brainstorming

## 📌 Overview
Thesis Brainstorming is a web-based tool that generates unique and diverse thesis ideas for Computer Science students and researchers. It uses the powerful **Groq API** for lightning-fast AI-powered thesis generation with intelligent fallback systems.

## 🚀 Features
- **🤖 Live AI Integration**: Uses Groq API (free tier available) for high-quality thesis generation
- **⚡ Lightning Fast**: Groq's LPU inference engine provides incredibly fast response times
- **🎯 Multiple Thesis Types**: Supports argumentative, analytical, expository, and comparative thesis types
- **📚 Detailed Research Guidance**: Includes research overviews, methodologies, and expected contributions
- **🎨 Tone Adaptation**: Adjusts content based on academic, persuasive, critical, or neutral tones
- **🌍 Covers Diverse Fields**: Works with any field of study from Computer Science to Environmental Science
- **💎 Professional Quality**: Generates research-ready thesis ideas with comprehensive structure
- **🔄 Smart Fallback**: Enhanced mock system when API is unavailable
- **✨ Beautiful UI**: Modern, responsive design with real-time API status monitoring
- **🚀 FastAPI Backend**: High-performance backend with async processing

## 🛠️ Tech Stack
- **Backend:** FastAPI (Python)
- **Frontend:** Jinja2 Templates, HTML/CSS, JavaScript
- **AI API:** Groq API (Lightning-fast LLM inference)
- **Models:** Llama 3.1 70B Versatile (via Groq)
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

### 2️⃣ Create Virtual Environment (Recommended)
```sh
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 4️⃣ Get Your FREE Groq API Key
🔑 **Option A: Use the setup script (Recommended)**
```sh
python3 setup_api.py
```

🔑 **Option B: Manual setup**
1. Visit [https://console.groq.com/keys](https://console.groq.com/keys)
2. Sign up (it's free!)
3. Create an API key
4. Set the environment variable:
```sh
export GROQ_API_KEY=your_api_key_here
```

### 5️⃣ Run the Application
Choose one of the following methods:

**Method 1: Direct Python execution**
```sh
python3 main.py
```

**Method 2: Using uvicorn directly**
```sh
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

### 6️⃣ Access the App
Open your browser and go to:
🔗 [http://localhost:8001/](http://localhost:8001/)

> **✅ Works without API key too!** The app includes an intelligent fallback system, so it works perfectly even without the API key. But with Groq API, you get lightning-fast, high-quality AI-generated thesis ideas!

## 🔑 API Endpoints
| Method | Endpoint             | Description                   |
|--------|---------------------|-------------------------------|
| GET    | /                   | Home Page                     |
| POST   | /generate           | Generate detailed thesis ideas |
| GET    | /models             | Fetch available AI models     |
| GET    | /check-api-status   | Check API service status      |

### Example API Response:
```json
{
  "generated_thesis": "Thesis Idea 1: The integration of Machine Learning across interdisciplinary boundaries is essential for solving complex global problems.\n\nResearch Overview: This thesis advocates for breaking down silos between Machine Learning and other disciplines...\n\nPotential Research Methods: Literature review, case study analysis, empirical research, and stakeholder interviews.\n\nExpected Contributions: This research would contribute to Machine Learning by providing new insights..."
}
```

## 🐛 Troubleshooting

### Common Issues:

1. **"python: command not found"**
   - Use `python3` instead of `python`
   - Make sure Python 3.8+ is installed

2. **Missing requirements.txt**
   - The file should contain: fastapi, uvicorn, jinja2, httpx, python-multipart, pydantic

3. **API Services Unavailable**
   - The app works perfectly with an intelligent fallback system that generates detailed thesis ideas
   - External APIs (HuggingFace, WebUI, Ollama) are optional - the app is fully functional without them
   - Check console logs for detailed error messages

4. **Port 8001 already in use**
   - Change the port in main.py: `uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=True)`

## 🧠 Intelligent Thesis Generation

The application features an advanced thesis generation system that creates detailed, research-ready ideas:

### What You Get:
- **Comprehensive Thesis Statements**: Well-structured, field-specific thesis ideas
- **Detailed Research Overviews**: In-depth explanations of research approaches and significance
- **Research Methodology Guidance**: Suggested methods including literature review, case studies, and empirical research
- **Expected Contributions**: Clear articulation of how the research would advance the field
- **Tone Adaptation**: Content adjusted based on your selected tone (academic, persuasive, critical, neutral)

### Thesis Types Supported:
- **Argumentative**: Takes a position and argues for it with evidence
- **Analytical**: Breaks down complex topics and examines relationships
- **Expository**: Explains and illuminates concepts for understanding
- **Comparative**: Compares different approaches, methods, or frameworks

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

