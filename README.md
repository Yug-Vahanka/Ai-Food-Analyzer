🍔 AI Food Analyzer

An intelligent web application that analyzes food using AI, tracks daily calorie intake, and provides health insights like BMI,
nutrition breakdown, and weekly analytics.

Built using FastAPI (backend) and Streamlit (frontend) with Google Gemini AI.

🚀 Features
🔐 User Authentication (Register / Login / Logout)
🥗 Food Analysis (by name)
📷 Image-based Food Detection (AI-powered)
🔥 Calorie Tracking System
📊 Analytics Dashboard (Charts + Insights)
📅 Weekly Calorie Trends
⚖️ BMI Calculator & Profile Management
📄 Export Reports as PDF
📧 Daily Email Summary
🗑️ Clear History Option

🏗️ Project Structure

ai-food-analyzer/
│
├── app/                    # Backend (FastAPI)
│   ├── main.py             # Entry point :contentReference[oaicite:0]{index=0}
│   ├── api/                # Routes (auth, food, analytics, etc.)
│   ├── core/               # Config & security
│   ├── db/                 # Database setup & queries :contentReference[oaicite:1]{index=1}
│   ├── services/           # Business logic (AI, BMI, PDF, Email)
│   └── utils/              # Helper functions :contentReference[oaicite:2]{index=2}
│
├── frontend/
│   └── app.py              # Streamlit UI :contentReference[oaicite:3]{index=3}
│
├── data/
│   └── food_ai.db          # SQLite Database
│
├── .env                    # API keys & email config :contentReference[oaicite:4]{index=4}
├── requirements.txt
├── run.py                  # Run both backend & frontend :contentReference[oaicite:5]{index=5}
└── README.md

⚙️ Tech Stack

Frontend: Streamlit
Backend: FastAPI
Database: SQLite
AI Model: Google Gemini API
Authentication: Token-based (Bearer + bcrypt)
Visualization: Matplotlib, Pandas
PDF Generation: ReportLab
Email Service: SMTP (Gmail)

🧠 How It Works

User logs in or registers
Sends food input (text or image)
Backend uses Gemini AI to analyze nutrition
Data is stored in SQLite database
Calories are extracted automatically
Dashboard shows analytics, charts, and insights
🔧 Installation & Setup
1. Clone the repository
git clone https://github.com/your-username/ai-food-analyzer.git
cd ai-food-analyzer
2. Create virtual environment
python -m venv venv
venv\Scripts\activate   # Windows
3. Install dependencies
pip install -r requirements.txt
4. Setup .env file

Create a .env file in root:

GEMINI_API_KEY=your_api_key_here
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_app_password

▶️ Run the Application

Option 1 (Recommended)
python run.py

👉 This runs:

FastAPI backend (uvicorn)
Streamlit frontend
Option 2 (Manual)

Start Backend:

uvicorn app.main:app --reload

Start Frontend:

streamlit run frontend/app.py

🌐 API Endpoints

Method	Endpoint	Description
POST	/register	Create account
POST	/login	Login user
POST	/analyze	Analyze food (text)
POST	/image	Analyze food image
GET	/analytics	Get analytics data
GET	/weekly	Weekly calorie trend
GET	/profile	Get user profile
POST	/profile	Update profile
GET	/export_pdf	Download report
POST	/send_email	Send summary email
DELETE	/delete_history	Clear all data
📊 Screenshots

<img width="1907" height="873" alt="Screenshot 2026-05-25 161954" src="https://github.com/user-attachments/assets/6ebdb12f-b0be-4501-b825-30693189f1d8" />
<img width="1558" height="752" alt="Screenshot 2026-05-25 162012" src="https://github.com/user-attachments/assets/234dce9a-b9c3-4ba5-9192-be6e029f6ea3" />
<img width="1544" height="536" alt="Screenshot 2026-05-25 162024" src="https://github.com/user-attachments/assets/058fa0e4-6f07-4894-9eb1-6712e55bee6c" />
<img width="1155" height="809" alt="Screenshot 2026-05-25 162042" src="https://github.com/user-attachments/assets/936a6efc-d951-4c4e-ab12-6406a608eb61" />
<img width="1581" height="842" alt="Screenshot 2026-05-25 162145" src="https://github.com/user-attachments/assets/7fe474a0-e863-480e-933a-8e7082de2d76" />
<img width="1553" height="378" alt="Screenshot 2026-05-25 162215" src="https://github.com/user-attachments/assets/b5eac1af-d59a-4972-aad8-07cad9a86fb5" />
<img width="1856" height="497" alt="Screenshot 2026-05-25 162225" src="https://github.com/user-attachments/assets/df96736a-bac0-4bd9-ac4c-8d91cd5fa170" />
<img width="1507" height="297" alt="Screenshot 2026-05-25 162245" src="https://github.com/user-attachments/assets/d8b747ce-6a9c-4543-bd20-eb5d11a3f066" />
<img width="1537" height="430" alt="Screenshot 2026-05-25 162510" src="https://github.com/user-attachments/assets/fcefd9b7-e26b-45e7-8614-f868f304fa6f" />
<img width="1531" height="436" alt="Screenshot 2026-05-25 162500" src="https://github.com/user-attachments/assets/fa41977e-bfa1-4639-a8c2-1bcd390a4147" />
<img width="1847" height="443" alt="Screenshot 2026-05-25 162440" src="https://github.com/user-attachments/assets/9584d5fd-24d4-4d4f-aea7-4506681a6e47" />
<img width="1511" height="507" alt="Screenshot 2026-05-25 162408" src="https://github.com/user-attachments/assets/35addc3d-6b65-443e-9dd8-b3d09a53beef" />
<img width="970" height="774" alt="Screenshot 2026-05-25 162301" src="https://github.com/user-attachments/assets/12c2e95c-bd6f-475e-a32d-9064f6b33e40" />
<img width="1512" height="725" alt="Screenshot 2026-05-25 162204" src="https://github.com/user-attachments/assets/15cd462c-7902-4904-8602-19ce77fa53f2" />

🔒 Security
Passwords hashed using bcrypt
Token-based authentication
Environment variables for sensitive data
🚧 Future Improvements
🔄 Add JWT authentication
🌍 Deploy on cloud (AWS / Render / Railway)
📱 Mobile-friendly UI
🍽️ Meal recommendations
🧬 Advanced nutrition insights
👨‍💻 Author

Yug Vahanka

⭐ Support

If you like this project, give it a ⭐ on GitHub!
