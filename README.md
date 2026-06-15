# InsureVoice — AI-Based Insurance Review & Transparency Platform

> **Final Year Engineering Project** | B.Tech CSE with AI Specialization
> Full-Stack Web Application · Firebase · Python NLP · Chart.js

---

## 📌 Abstract

InsureVoice is a web-based platform designed to bring transparency to India's insurance ecosystem by enabling customers to share authentic reviews about their insurance experiences. The platform uses AI-powered Natural Language Processing (NLP) to automatically classify review sentiments as Positive, Negative, or Neutral. It provides verified review badges for reviews with uploaded proof documents, real-time analytics dashboards, and smart search/filter capabilities — helping consumers make informed insurance decisions beyond promotional content.


## 🚀 Live Demo

🌐 Frontend: https://playful-cannoli-1cc235.netlify.app/

📂 GitHub Repository: https://github.com/LMR09/InsureVoice

⚙️ Backend API: https://insurevoice.onrender.com/

---

## 🔥 Problem Statement

Millions of Indian insurance customers rely on advertisements and agents when selecting policies, but lack access to genuine peer experiences about:
- Claim approval/rejection processes
- Hidden policy conditions
- Customer support quality
- Claim processing times and delays

This information asymmetry leads to poor insurance decisions, financial losses, and eroded trust in the sector.

---

## 🎯 Objectives

1. Build a platform for users to post, read, and rate insurance reviews
2. Apply NLP sentiment analysis to auto-classify each review
3. Reduce fake reviews through a document-verified badge system
4. Visualize analytics to identify poorly-performing insurance companies
5. Enable real-time search and filtering by company, policy, rating, and sentiment

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🔐 Firebase Auth | Email/password + Google OAuth login |
| 📝 Review Posting | Rate, describe, and categorize insurance experiences |
| 🤖 AI Sentiment | Python NLP classifies reviews as Positive/Negative/Neutral |
| ✅ Verified Badges | Upload claim docs to earn a Verified review badge |
| 📊 Dashboard | Chart.js analytics: ratings, sentiments, claim trends |
| 🔍 Search & Filter | Filter by company, policy, rating, sentiment, verified status |
| 📱 Responsive | Works on mobile, tablet, and desktop |
| 🌐 Free Deploy | Firebase Hosting + Render (Python backend) |

---

## 🛠️ Technology Stack

### Frontend
- HTML5, CSS3 (custom design system — no Bootstrap)
- Vanilla JavaScript (ES6+)
- Chart.js 4.x (analytics charts)
- Google Fonts: Playfair Display + DM Sans

### Backend (AI/NLP)
- Python 3.10+
- Flask 3.0 (REST API)
- TextBlob + NLTK (sentiment analysis)
- Flask-CORS (cross-origin support)

### Firebase Services
- **Firebase Authentication** — user login/signup
- **Firestore** — review storage (NoSQL real-time database)
- **Firebase Storage** — proof document uploads
- **Firebase Hosting** — static frontend deployment

---

## 📂 Project Structure

```
InsureVoice/
│
├── index.html          # Landing page
├── login.html          # User login
├── signup.html         # User registration
├── review.html         # Write a review (auth-protected)
├── reviews.html        # Browse all reviews with search/filter
├── dashboard.html      # Analytics dashboard
├── profile.html        # User profile & my reviews
│
├── css/
│   └── style.css       # Complete design system (variables, components)
│
├── js/
│   ├── auth.js         # Auth state management, guard, logout
│   └── utils.js        # Helpers: stars, badges, dates, constants
│
├── firebase/
│   ├── firebase-config.js   # Firebase SDK initialization
│   ├── firestore.rules      # Firestore security rules
│   └── storage.rules        # Storage security rules
│
├── backend/
│   ├── app.py               # Flask API server
│   ├── sentiment.py         # NLP sentiment engine
│   └── requirements.txt     # Python dependencies
│
└── README.md
```

---

## 🚀 Setup Guide

### Step 1 — Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/InsureVoice.git
cd InsureVoice
```

---

### Step 2 — Firebase Project Setup

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click **"Add project"** → name it `InsureVoice`
3. Disable Google Analytics (optional) → **Create project**

#### Enable Authentication
1. Sidebar → **Authentication** → **Get Started**
2. **Sign-in method** tab → Enable **Email/Password**
3. Enable **Google** (set project support email)

#### Enable Firestore
1. Sidebar → **Firestore Database** → **Create database**
2. Select **Production mode** → choose your region → **Done**
3. Go to **Rules** tab → paste contents of `firebase/firestore.rules` → **Publish**

#### Enable Storage
1. Sidebar → **Storage** → **Get Started** → **Next** → **Done**
2. Go to **Rules** tab → paste contents of `firebase/storage.rules` → **Publish**

#### Get Firebase Config
1. Sidebar → ⚙️ **Project Settings** → **Your apps** → click **</>** (Web)
2. Register app name → copy the `firebaseConfig` object
3. Open `firebase/firebase-config.js` → replace all placeholder values

```javascript
const firebaseConfig = {
  apiKey:            "AIzaSy...",
  authDomain:        "insure-voice.firebaseapp.com",
  projectId:         "insure-voice",
  storageBucket:     "insure-voice.appspot.com",
  messagingSenderId: "123456789",
  appId:             "1:123...:web:abc..."
};
```

---

### Step 3 — Python Backend Setup

```bash
cd backend

# Create virtual environment (recommended)
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download NLTK data (run once)
python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger'); nltk.download('brown')"

# Start the API server
python app.py
```

The API will be live at: `https://insurevoice.onrender.com/analyze`

Test it:
```bash
curl -X POST https://insurevoice.onrender.com/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "Claim was rejected without any valid reason. Very frustrating."}'
```

Expected response:
```json
{
  "sentiment": "negative",
  "polarity": -0.62,
  "subjectivity": 0.74,
  "label": "Negative 😞",
  "confidence": "high",
  "keywords": {
    "positive": [],
    "negative": ["rejected", "frustrating"]
  }
}
```

---

### Step 4 — Run Locally

Open `index.html` in your browser directly, or use Live Server (VS Code extension) for hot reload.

> **Note:** The site works fully without the Python backend — sentiment analysis falls back to a client-side keyword engine. The backend enhances accuracy.

---

## 🌐 Live Deployment

### Frontend (Netlify)

The InsureVoice frontend is deployed and accessible at:

**Live Demo:**
https://playful-cannoli-1cc235.netlify.app/

### Backend API (Render)

The Python Flask Sentiment Analysis API is deployed on Render:

**API Endpoint:**
https://insurevoice.onrender.com/

### Available API Routes

#### Health Check

GET

```bash
https://insurevoice.onrender.com/
```

Response:

```json
{
  "status": "success",
  "message": "InsureVoice Sentiment API Running"
}
```

#### Sentiment Analysis

POST

```bash
https://insurevoice.onrender.com/analyze
```

Request Body:

```json
{
  "text": "Excellent customer service and quick claim settlement."
}
```

Response:

```json
{
  "sentiment": "Positive",
  "score": 0.8
}
```

---

## 🚀 Deployment Architecture

Frontend (HTML, CSS, JavaScript)
↓
Netlify Hosting
↓
Firebase Authentication
↓
Cloud Firestore Database
↓
Render Hosted Python API
↓
AI-Based Sentiment Analysis

---

## 🔗 Project Links

### Live Application

https://playful-cannoli-1cc235.netlify.app/

### GitHub Repository

https://github.com/LMR09/InsureVoice

### Backend API

https://insurevoice.onrender.com/

```

---

## 🗄️ Database Design (Firestore)

### `users` collection
```
users/{uid}/
  ├── uid           : string
  ├── name          : string
  ├── email         : string
  ├── createdAt     : timestamp
  └── reviewCount   : number
```

### `reviews` collection
```
reviews/{reviewId}/
  ├── userId            : string
  ├── username          : string
  ├── email             : string
  ├── insuranceCompany  : string
  ├── policyType        : string
  ├── rating            : number (1-5)
  ├── reviewTitle       : string
  ├── reviewText        : string
  ├── claimStatus       : "Approved" | "Rejected" | "Delayed" | "N/A"
  ├── sentiment         : "positive" | "negative" | "neutral"
  ├── polarity          : number
  ├── subjectivity      : number
  ├── verifiedStatus    : boolean
  ├── uploadedProofURL  : string | null
  ├── helpfulCount      : number
  └── timestamp         : timestamp
```

---

## 🧪 Testing

### Test Authentication
- Sign up with email → check Firestore `users` collection
- Login with wrong password → should show error
- Google OAuth → should create user doc

### Test Review Submission
- Submit a review with all required fields
- Check Firestore `reviews` collection for new document
- Upload a PDF proof → check Firebase Storage

### Test Sentiment API
```bash
cd backend
python sentiment.py
```
This runs 6 pre-defined test cases and prints results.

### Test Dashboard
- Open `dashboard.html` — should show charts with live Firestore data
- If Firebase not configured, shows realistic demo data

---

## 📈 Advantages

- ✅ **Free to deploy** — Firebase free tier + Render free tier
- ✅ **AI-powered** — NLP sentiment beyond simple star ratings
- ✅ **Trust mechanism** — Verified review badges reduce fake reviews
- ✅ **Real-time** — Firestore gives instant data updates
- ✅ **Beginner-friendly** — No complex frameworks; pure HTML/CSS/JS
- ✅ **Scalable** — Firebase scales automatically with usage

---

## 🔮 Future Scope

1. **Admin Panel** — Moderate reviews, ban users, manage companies
2. **Email Notifications** — Alert companies about new negative reviews
3. **Company Response** — Allow insurers to reply to reviews
4. **Advanced NLP** — Fine-tune BERT/RoBERTa on insurance domain data
5. **IRDA Integration** — Link with IRDAI public complaint data
6. **Mobile App** — React Native version
7. **Multilingual** — Hindi/Telugu review support
8. **API for Insurers** — Paid B2B sentiment monitoring dashboard

---

## 📘 IEEE-Style Documentation Sections

### Proposed System
InsureVoice proposes a three-tier web architecture: a static HTML/JS frontend hosted on Firebase Hosting, a Firestore NoSQL database for real-time review storage, and a Python/Flask REST API for NLP sentiment classification. The system integrates Firebase Authentication for secure access control and Firebase Storage for verified proof document uploads.

### Conclusion
InsureVoice successfully demonstrates the application of AI/NLP techniques in a domain-specific consumer platform. The integration of TextBlob sentiment analysis with insurance-domain keyword enhancement achieves meaningful review classification with no ML training overhead. The platform addresses a genuine information asymmetry problem in India's insurance sector and is production-deployable using entirely free cloud services.

---

## 👨‍💻 Team

Built as a Final Year B.Tech CSE (AI) Major Project.

---

## 📄 License

MIT License — free to use and modify for educational purposes.
