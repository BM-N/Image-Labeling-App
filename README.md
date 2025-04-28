# 🖼️ Image Labeling App – Django + PyTorch + HuggingFace

A backend-driven image classification app where users upload images, receive model predictions, and track their submissions — all through a Django REST API and simple web UI.

---

## ✨ Project Highlights

- **🔒 JWT Authentication**: Secure user registration and login.
- **🖼️ Image Upload and Labeling**: Upload images, classify them, and store predictions per user.
- **🧠 ML Model Integration**:
  - `main` branch: Local inference using PyTorch’s `resnet50`
  - `hfapi` branch: Cloud inference using HuggingFace Inference API
- **🚀 Deployment**: Live app hosted on Render (hfapi branch)

---

## 🌐 Live Demo

> [🔗 Access the Deployed App Here](https://image-labeling-app.onrender.com/)

⚡ **Important**:  
Render uses a free-tier server.  
If the app has been inactive, **the first request might take up to 1 minute** to load due to cold start!

---

## 🧰 Tech Stack

- **Backend**: Django, Django REST Framework
- **ML Framework**: PyTorch (`resnet50` pretrained model)
- **Inference (cloud)**: HuggingFace Inference API
- **Auth**: JWT (SimpleJWT)
- **Deployment**: Docker + Render
- **Database**: SQLite3 (local)

---

## 🖥️ How to Use (Through the Web UI)

1. **Register**
   - Go to `/api/user/register/`
   - Fill username and password
   - Click **Register**

2. **Login**
   - Go to `/api/user/login/`
   - Enter your credentials
   - Obtain your JWT access token

3. **Upload an Image**
   - Navigate to `/api/classify/`
   - Upload your image file
   - Submit → Get back the **top-k(default=1) predictions** and **confidence scores**

4. **View Previously Uploaded Images & Results**
   - *(optional feature to be developed further)* View user-specific uploads.

---

## 📂 Project Structure Overview

```bash
api/          # Django app for user auth, API endpoints
label_app/    # Django project settings
ml/           # PyTorch model loading and inference logic
templates/    # Minimal HTML forms for UI interaction
media/        # Uploaded user images
Dockerfile    # Containerization setup
render.yaml   # Render deployment config
requirements.txt
```

---

## 🧩 Branches

| Branch | Purpose |
|--------|---------|
| `main` | Full local PyTorch inference using `resnet50` |
| `hfapi` | Deployed version: lightweight inference via HuggingFace API |

---

## 🛠 Local Setup Instructions

### 1. Clone the repo and setup environment
```bash
git clone https://github.com/BM-N/Image-Labeling-App.git
cd Image-Labeling-App
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run Django server
```bash
python manage.py migrate
python manage.py runserver
```

- Visit `http://127.0.0.1:8000/`
- Follow the web UI to Register → Login → Upload Image.

---

## ✅ Roadmap

- [x] Deploy demo version using HuggingFace inference
- [x] Build local inference version with ResNet50
- [x] Build simple UI to display classification results elegantly
- [ ] Add user history page (previous uploads and results)

---

## 👨‍💻 Author

**Bruno Nunes**  

Machine Learning Engineer and Backend Developer specializing in building ML-driven systems.

Currently completing a Master's degree focused on AI applications in medicine, combining deep learning with backend architecture to deliver real-world healthcare solutions.

🔗 [Portfolio](https://bmn-portfolio.framer.website/)  
🔗 [LinkedIn](https://www.linkedin.com/in/bmn27296256/)  
🔗 [GitHub](https://github.com/BM-N)

---

## 📜 License

MIT License — Free to use, learn, and adapt.