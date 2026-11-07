# SENTINEL AI: Fake Review & Coordinated Reviewer Network Detection System

An enterprise-grade, privacy-first cybersecurity and artificial intelligence platform designed to detect fraudulent product reviews and unmask coordinated reviewer collusion rings using **Natural Language Processing (NLP)**, **Machine Learning (Scikit-Learn)**, and **Bipartite Graph Theory (NetworkX)**.

---

## 🌟 Key Highlights & Core Capabilities

1. **Tri-Pillar Detection Architecture**:
   - **Linguistic & Stylometric NLP**: TF-IDF cosine similarity for duplicate text and spun templates, punctuation shouting intensity, and sentiment-rating cognitive dissonance.
   - **Behavioral Profiling**: Temporal burst velocity (posting frequency spikes), rating extremity skews (1-star vs 5-star bias), and unverified buyer friction.
   - **Bipartite Graph Theory (NetworkX)**: Models Reviewer $\leftrightarrow$ Product relationships, computes co-review graph projections, and uncovers coordinated collusion rings and dense cliques.
2. **Explainable AI (XAI)**:
   - Does not output opaque black-box verdicts.
   - Breaks down every score ($0$ to $100$) into justifiable evidence factors (e.g., `+30% High Duplicate Match`, `+40% Coordinated Collusion Ring Member`).
3. **Privacy & Ethical Safeguards**:
   - Salted SHA-256 pseudonymization of reviewer emails and usernames ensures personal data is never stored in plaintext.
   - Implements a Human-in-the-Loop audit console where trust analysts review and verify cases without automatically defaming customers.
4. **Automated Forensic PDF Dossiers**:
   - Generates publication-ready PDF audit reports summarizing threat landscape KPIs, at-risk product SKUs, and actionable recommendations.

---

## 📁 Project Directory Structure

```text
fake-review-network-detector/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── v1/
│   │   │   │   ├── auth.py          # User registration, login, JWT issuance
│   │   │   │   ├── products.py      # Catalog management & trust scores
│   │   │   │   ├── reviews.py       # Review submission & batch CSV ingestion
│   │   │   │   ├── graph.py         # NetworkX topology & collusion ring mining
│   │   │   │   ├── dashboard.py     # High-level KPIs & risk tier statistics
│   │   │   │   └── reports.py       # PDF dossier generator & audit logs
│   │   │   └── deps.py              # JWT authentication & RBAC guards
│   │   ├── core/
│   │   │   ├── config.py            # App settings (Pydantic Settings)
│   │   │   ├── database.py          # SQLAlchemy engine (MySQL / SQLite)
│   │   │   └── security.py          # Bcrypt hashing & salted SHA-256 privacy
│   │   ├── models/                  # SQLAlchemy ORM database models
│   │   ├── schemas/                 # Pydantic request/response schemas
│   │   ├── services/
│   │   │   ├── nlp_service.py       # TF-IDF, Cosine Sim & Sentiment Divergence
│   │   │   ├── behavioral_service.py# Burst velocity & rating extremity
│   │   │   ├── ml_service.py        # Supervised ML inference pipeline
│   │   │   ├── graph_service.py     # NetworkX bipartite graph & clique engine
│   │   │   ├── scoring_service.py   # Explainable AI composite scoring
│   │   │   └── report_service.py    # ReportLab automated PDF generator
│   │   └── main.py                  # FastAPI application entrypoint
│   ├── ml_pipeline/
│   │   ├── dataset_loader.py        # Benchmark dataset generator
│   │   └── train_models.py          # Train & evaluate Logistic Regression, RF, GBoost
│   ├── saved_models/
│   │   └── champion_model.joblib    # Serialized champion model weights
│   ├── tests/
│   │   └── test_backend.py          # Comprehensive test suite (7/7 passing)
│   ├── requirements.txt             # Python dependencies
│   └── seed_data.py                 # Database seeder (products, reviews, rings)
├── frontend/
│   ├── src/
│   │   ├── api/client.js            # API client with JWT handling
│   │   ├── components/
│   │   │   ├── Navbar.jsx           # Navigation, user profile, PDF export
│   │   │   ├── NetworkGraph.jsx     # Interactive Vis.js 2D network visualizer
│   │   │   ├── DashboardView.jsx    # Real-time metrics & risk breakdown
│   │   │   ├── ProductsView.jsx     # Catalog reputation management
│   │   │   ├── IngestionView.jsx    # Live text scan & batch CSV upload
│   │   │   ├── CollusionRingsView.jsx# Collusion ring audit & quarantine
│   │   │   └── AuthModal.jsx        # Login/Register with 1-click demo fill
│   │   ├── App.jsx                  # Main React orchestrator
│   │   ├── index.css                # Modern dark-mode UI styling
│   │   └── main.jsx                 # React root mount
│   ├── package.json                 # Node/Vite dependencies
│   └── vite.config.js               # Vite bundler & reverse proxy config
├── run_backend.bat                  # 1-click Windows backend launcher
├── run_frontend.bat                 # 1-click Windows frontend launcher
├── seed_demo_data.bat               # 1-click database seeder launcher
└── run_tests.bat                    # 1-click test suite launcher
```

---

## 🚀 Quickstart Guide (How to Run)

### Method 1: Using the 1-Click Launchers (Recommended for Beginners)

1. **Seed the Database**:
   - Double-click `seed_demo_data.bat`.
   - This creates the database, loads sample products, generates duplicate spam, and constructs a 4-account collusion ring.
2. **Start the Backend API**:
   - Double-click `run_backend.bat`.
   - The FastAPI backend will start at: `http://127.0.0.1:8000`.
   - Interactive Swagger API docs: `http://127.0.0.1:8000/docs`.
3. **Start the Frontend UI**:
   - Double-click `run_frontend.bat`.
   - Open your browser to: `http://localhost:3000`.

---

### Method 2: Manual Terminal Commands

#### 1. Backend Setup:
```powershell
cd backend
# Activate virtual environment
.\venv\Scripts\activate.bat

# Run automated tests to verify system health
python -m pytest tests/test_backend.py -v -o norecursedirs=venv

# Seed demo data
python seed_data.py

# Launch FastAPI server
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

#### 2. Frontend Setup:
```powershell
cd frontend
# Launch React Vite dev server
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## 🔑 Default Credentials

Click **"Sign In / Demo"** in the top navigation bar to access 1-click demo login buttons:

Demo accounts are created by running `python seed_data.py` before starting the backend. Public registrations receive analyst access; on an empty database, the first registered account is the bootstrap administrator.

| Account Role | Email Address | Password | Permissions |
|:---|:---|:---|:---|
| **System Administrator** | `admin@antigravity.io` | `Admin@12345` | Full administrative control, catalog SKU registration, audit overrides |
| **Trust & Safety Analyst** | `analyst@antigravity.io` | `Analyst@12345` | Audit investigation, quarantine rings, submit reviews, download PDF reports |

---

## 🗄️ Database: MySQL vs. SQLite

- **Instant Zero-Config Mode (SQLite)**: By default, the application runs on SQLite (`fake_review_db.sqlite3`). You do not need to install or configure anything; it works right out of the box!
- **MySQL Mode (XAMPP / Production)**:
  1. Open XAMPP Control Panel and click **Start** next to MySQL.
  2. In MySQL, create a database named `fake_review_db`:
     ```sql
     CREATE DATABASE fake_review_db;
     ```
  3. Create a `.env` file inside `backend/` with:
     ```ini
     USE_MYSQL=True
     MYSQL_URL=mysql+pymysql://root:@localhost:3306/fake_review_db
     ```
  4. Run `python seed_data.py`. The SQLAlchemy ORM will automatically migrate all tables to MySQL!

---

## 🧠 Machine Learning & Graph Theory Deep Dive

### 1. Linguistic Duplicate Matching (TF-IDF & Cosine Similarity)
$$\text{Cosine Similarity}(\vec{u}, \vec{v}) = \frac{\vec{u} \cdot \vec{v}}{\|\vec{u}\|_2 \|\vec{v}\|_2}$$
Every newly ingested review is transformed into unigram and bigram TF-IDF vectors and compared against the product's historical review corpus. A similarity score $\ge 0.70$ triggers a **"High Duplicate Text Match"** flag.

### 2. Cognitive Dissonance (Sentiment vs. Star Rating)
Measures disagreement between emotional polarity ($[-1.0, +1.0]$) and normalized rating:
$$\text{Divergence} = \frac{|\text{Normalized Rating} - \text{Sentiment Polarity}|}{2.0}$$
Catches deceptive promotional reviews (e.g. 5 stars with negative text, or 1 star with positive text).

### 3. Bipartite Graph Projection & Collusion Mining (NetworkX)
The system constructs a bipartite graph $B = (Reviewers \cup Products, E)$. It then computes the one-mode projection $G_{co\_review}$ where:
- Nodes = Reviewer accounts.
- Edge weight = Number of co-reviewed products.
NetworkX mines connected subgraphs and maximal cliques with density $> 0.35$ to automatically reveal coordinated review rings.

### 4. Explainable AI (XAI) Scoring Engine
$$S_{composite} = \sum_{i} w_i \cdot f_i \times 100$$
Each component contributes transparently to the score:
- Duplicate Plagiarism: $25\%$
- AI Deception Classifier: $15\%$
- Sentiment Divergence: $15\%$
- Burst Posting Velocity: $15\%$
- Collusion Ring Membership: $15\%$
- Rating Polarity Extremity: $10\%$
- Unverified Purchase: $5\%$
Scores are categorized into **LOW** ($< 35$), **MEDIUM** ($35-65$), and **HIGH** ($> 65$) risk tiers.
#   f i r s t p r o j e c t  
 