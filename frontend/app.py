#  app.py  —  Streamlit Frontend for AI Food Analyzer
#  Features: Login/Register, Food Analysis, Image Analysis,
#             Meal Categories, Calorie Goal, BMI Calculator,
#             Weekly Chart, Pie Chart, PDF Export, Email Summary
import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# Backend API base URL (must match where uvicorn is running)
API_URL = "http://127.0.0.1:8000"

# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="🍔 AI Food Analyzer",
    page_icon="🍔",
    layout="wide"
)


#  SESSION STATE INIT
#  Streamlit re-runs the whole script on every interaction,
#  so we use session_state to persist login info across reruns.

if "user"  not in st.session_state: st.session_state.user  = None
if "token" not in st.session_state: st.session_state.token = None

def auth_headers():
    """Return Authorization header dict for all API calls."""
    return {"Authorization": f"Bearer {st.session_state.token}"}


#  SIDEBAR NAVIGATION
if st.session_state.user is None:
    # Logged-out users only see Login / Register
    menu   = ["Login", "Register"]
    choice = st.sidebar.selectbox("Menu", menu)
else:
    # Logged-in users navigate between dashboard sections
    st.sidebar.success(f"👤 {st.session_state.user}")
    choice = st.sidebar.radio("Navigate", [
        "🏠 Dashboard",
        "📊 Analytics",
        "📅 Weekly Chart",
        "⚖️ BMI & Profile",
        "🧠 My Data",
        "📄 Export PDF",
        "📧 Email Summary",
        "🗑 Clear History"
    ])
#  REGISTER

if choice == "Register":
    st.title("📝 Create Account")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Register"):
        res = requests.post(f"{API_URL}/register", data={"username": u, "password": p})
        if res.status_code == 200:
            st.success("✅ " + res.json()["msg"] + " — Please login.")
        else:
            st.error(res.json().get("detail", "Registration failed"))


#  LOGIN
elif choice == "Login":
    st.title("🔐 Login")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        res = requests.post(f"{API_URL}/login", data={"username": u, "password": p})
        if res.status_code == 200 and res.json().get("msg") == "success":
            st.session_state.user  = u
            st.session_state.token = res.json()["token"]
            st.success("Logged in!")
            st.rerun()      # Reload page to show dashboard
        else:
            st.error("Invalid credentials")


#  DASHBOARD  —  Food Analysis + Image Upload
elif choice == "🏠 Dashboard":
    st.title(f"🍔 Welcome, {st.session_state.user}!")

    # ---- CALORIE GOAL PROGRESS ----
    # Fetch today's history to calculate today's total calories
    res_analytics = requests.get(f"{API_URL}/analytics", headers=auth_headers())
    if res_analytics.status_code == 200:
        history = res_analytics.json().get("history", [])
        today_str = datetime.now().date().isoformat()

        # Filter to only today's entries
        today_entries = [h for h in history if h.get("date") == today_str]
        today_calories = sum(h["calories"] for h in today_entries)

        # Fetch the user's calorie goal from their profile
        profile_res = requests.get(f"{API_URL}/profile", headers=auth_headers())
        goal = 2000  # Default goal
        if profile_res.status_code == 200 and profile_res.json():
            goal = profile_res.json().get("calorie_goal", 2000)

        # Show progress bar (capped at 100%)
        progress = min(today_calories / goal, 1.0)
        st.markdown(f"### 🎯 Today's Calorie Goal: **{today_calories} / {goal} kcal**")
        st.progress(progress)

        if today_calories >= goal:
            st.warning("⚠️ You've reached your daily calorie goal!")
        else:
            st.info(f"✅ {goal - today_calories} kcal remaining today")

    st.divider()

    # ---- MEAL TYPE SELECTOR ----
    # Shown above both text and image analysis
    st.markdown("### 🍽️ Meal Type")
    meal_type = st.selectbox(
        "Select meal type for this entry:",
        ["Breakfast", "Lunch", "Dinner", "Snack", "Other"]
    )

    # ---- TEXT FOOD ANALYSIS ----
    st.markdown("### 🥗 Analyze Food by Name")
    food = st.text_input("Enter food name (e.g. Biryani, Apple, Pizza)")

    if st.button("🔍 Analyze Food"):
        if not food.strip():
            st.warning("Please enter a food name.")
        else:
            with st.spinner("Analyzing with Gemini..."):
                res = requests.post(
                    f"{API_URL}/analyze",
                    data={"food": food, "meal_type": meal_type},
                    headers=auth_headers()
                )
            if res.status_code == 200:
                st.success("Analysis complete!")
                st.markdown(res.json()["result"])
            else:
                st.error(f"Error: {res.json().get('detail', res.text)}")

    st.divider()

    # ---- IMAGE FOOD ANALYSIS ----
    st.markdown("### 📷 Analyze Food by Image")
    img = st.file_uploader("Upload a food photo", type=["jpg", "jpeg", "png", "webp"])

    if img:
        st.image(img, caption="Uploaded Image", width=300)
        if st.button("🔍 Analyze Image"):
            with st.spinner("Gemini is identifying the food..."):
                res = requests.post(
                    f"{API_URL}/image",
                    files={"file": img},
                    data={"meal_type": meal_type},
                    headers=auth_headers()
                )
            if res.status_code == 200:
                st.success("Analysis complete!")
                st.markdown(res.json()["result"])
            else:
                st.error(f"Image error: {res.json().get('detail', res.text)}")

    # ---- LOGOUT BUTTON ----
    st.divider()
    if st.button("🚪 Logout"):
        requests.post(f"{API_URL}/logout", headers=auth_headers())
        st.session_state.user  = None
        st.session_state.token = None
        st.rerun()

#  ANALYTICS  —  Bar Chart + Pie Chart + Meal Breakdown

elif choice == "📊 Analytics":
    st.title("📊 Analytics")

    res = requests.get(f"{API_URL}/analytics", headers=auth_headers())
    if res.status_code != 200:
        st.error("Failed to load analytics.")
        st.stop()

    data    = res.json()
    history = data.get("history", [])

    st.metric("Total Food Entries", data["total_queries"])

    if not history:
        st.info("No history yet. Go to Dashboard and analyze some food!")
        st.stop()

    df = pd.DataFrame(history)

    # ---- RAW HISTORY TABLE ----
    st.markdown("### 📋 Full History")
    st.dataframe(
        df[["date", "meal_type", "query", "calories"]].rename(columns={
            "date": "Date", "meal_type": "Meal", "query": "Food", "calories": "Calories (kcal)"
        }),
        use_container_width=True
    )

    col1, col2 = st.columns(2)

    # ---- BAR CHART — calories per food item ----
    with col1:
        st.markdown("### 📊 Calories per Food")
        bar_df = df[df["calories"] > 0].set_index("query")["calories"]
        if not bar_df.empty:
            st.bar_chart(bar_df)
        else:
            st.info("No calorie data yet.")

    # ---- PIE CHART — calories distribution (includes image entries) ----
    with col2:
        st.markdown("### 🍩 Calorie Distribution")
        # Group all entries (text + image) by food name, sum their calories
        pie_data = df[df["calories"] > 0].groupby("query")["calories"].sum()

        if not pie_data.empty:
            fig, ax = plt.subplots(figsize=(6, 6))
            ax.pie(
                pie_data,
                labels=pie_data.index,
                autopct="%1.1f%%",
                startangle=140
            )
            ax.axis("equal")    # Make the pie circular
            st.pyplot(fig)
        else:
            st.info("No calorie data to display.")

    # ---- MEAL TYPE BREAKDOWN ----
    st.markdown("### 🍽️ Calories by Meal Type")
    meal_df = df[df["calories"] > 0].groupby("meal_type")["calories"].sum().reset_index()
    if not meal_df.empty:
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        ax2.bar(meal_df["meal_type"], meal_df["calories"], color="steelblue")
        ax2.set_xlabel("Meal Type")
        ax2.set_ylabel("Total Calories (kcal)")
        ax2.set_title("Calories by Meal Type")
        st.pyplot(fig2)

#  WEEKLY CHART  —  Line chart of calories over last 7 days

elif choice == "📅 Weekly Chart":
    st.title("📅 Weekly Calorie Trend")

    res = requests.get(f"{API_URL}/weekly", headers=auth_headers())
    if res.status_code != 200:
        st.error("Failed to load weekly data.")
        st.stop()

    weekly = res.json().get("weekly", [])
    df = pd.DataFrame(weekly)

    # Fetch goal for reference line
    profile_res = requests.get(f"{API_URL}/profile", headers=auth_headers())
    goal = 2000
    if profile_res.status_code == 200 and profile_res.json():
        goal = profile_res.json().get("calorie_goal", 2000)

    # ---- LINE CHART ----
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df["date"], df["calories"], marker="o", linewidth=2,
            color="steelblue", label="Calories Consumed")

    # Dashed goal line for reference
    ax.axhline(y=goal, color="red", linestyle="--", linewidth=1.5, label=f"Goal: {goal} kcal")

    ax.set_title("Calories Over Last 7 Days", fontsize=14)
    ax.set_xlabel("Date")
    ax.set_ylabel("Calories (kcal)")
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

    # Summary table below chart
    st.markdown("### 📋 Daily Breakdown")
    df["status"] = df["calories"].apply(
        lambda c: "✅ Under Goal" if c <= goal else "⚠️ Over Goal"
    )
    st.dataframe(df.rename(columns={"date": "Date", "calories": "Calories (kcal)", "status": "Status"}),
                 use_container_width=True)
#  BMI & PROFILE

elif choice == "⚖️ BMI & Profile":
    st.title("⚖️ BMI Calculator & Profile")

    # Load existing profile if available
    profile_res = requests.get(f"{API_URL}/profile", headers=auth_headers())
    existing = {}
    if profile_res.status_code == 200:
        existing = profile_res.json()

    with st.form("profile_form"):
        st.markdown("### 📝 Your Details")

        col1, col2 = st.columns(2)
        with col1:
            height = st.number_input("Height (cm)", min_value=50.0, max_value=250.0,
                                     value=float(existing.get("height_cm") or 170))
            weight = st.number_input("Weight (kg)", min_value=10.0, max_value=300.0,
                                     value=float(existing.get("weight_kg") or 70))
            age    = st.number_input("Age", min_value=1, max_value=120,
                                     value=int(existing.get("age") or 25))

        with col2:
            gender   = st.selectbox("Gender", ["Male", "Female", "Other"],
                                    index=["Male", "Female", "Other"].index(
                                        existing.get("gender", "Male")))
            activity = st.selectbox("Activity Level",
                                    ["Sedentary", "Light", "Moderate", "Active", "Very Active"],
                                    index=["Sedentary", "Light", "Moderate", "Active", "Very Active"].index(
                                        existing.get("activity", "Sedentary")))
            goal     = st.number_input("Daily Calorie Goal (kcal)", min_value=500, max_value=5000,
                                       value=int(existing.get("calorie_goal", 2000)))

        submitted = st.form_submit_button("💾 Save Profile & Calculate BMI")

    if submitted:
        res = requests.post(
            f"{API_URL}/profile",
            data={
                "height_cm": height, "weight_kg": weight, "age": age,
                "gender": gender, "activity": activity, "calorie_goal": goal
            },
            headers=auth_headers()
        )
        if res.status_code == 200:
            result = res.json()
            bmi      = result["bmi"]
            category = result["category"]
            rec_cal  = result["recommended_calories"]

            st.success("✅ Profile saved!")

            # Display BMI result cards
            col1, col2, col3 = st.columns(3)
            col1.metric("BMI", bmi)
            col2.metric("Category", category)
            col3.metric("Recommended Calories", f"{rec_cal} kcal")

            # Color-coded BMI interpretation
            if category == "Underweight":
                st.warning("⚠️ You are underweight. Consider a higher calorie diet.")
            elif category == "Normal":
                st.success("✅ You have a healthy BMI. Keep it up!")
            elif category == "Overweight":
                st.warning("⚠️ You are slightly overweight. A moderate calorie deficit may help.")
            else:
                st.error("❌ BMI indicates obesity. Please consult a health professional.")
        else:
            st.error("Failed to save profile.")
#  MY DATA  —  Raw table of all history entries

elif choice == "🧠 My Data":
    st.title("🧠 My Food History")

    res = requests.get(f"{API_URL}/my_data", headers=auth_headers())
    if res.status_code == 200:
        data = res.json().get("data", [])
        if data:
            df = pd.DataFrame(data)
            st.dataframe(
                df[["date", "meal_type", "query", "response"]].rename(columns={
                    "date": "Date", "meal_type": "Meal",
                    "query": "Food", "response": "Analysis"
                }),
                use_container_width=True
            )
        else:
            st.warning("No data found.")
    else:
        st.error("Failed to load data.")


#  EXPORT PDF
elif choice == "📄 Export PDF":
    st.title("📄 Export Food Report as PDF")
    st.info("Click the button below to download your full food history as a PDF report.")

    if st.button("⬇️ Download PDF Report"):
        with st.spinner("Generating PDF..."):
            res = requests.get(f"{API_URL}/export_pdf", headers=auth_headers())

        if res.status_code == 200:
            # Offer the PDF as a Streamlit download
            st.download_button(
                label="📥 Click to Save PDF",
                data=res.content,
                file_name=f"{st.session_state.user}_food_report.pdf",
                mime="application/pdf"
            )
        else:
            st.error("Failed to generate PDF.")


#  EMAIL SUMMARY
elif choice == "📧 Email Summary":
    st.title("📧 Daily Email Summary")
    st.info(
        "Enter your email below to receive today's food log and calorie total. "
        "Make sure EMAIL_USER and EMAIL_PASS are set in your .env file."
    )

    email = st.text_input("Your email address")
    if st.button("📨 Send Summary"):
        if not email.strip():
            st.warning("Please enter an email address.")
        else:
            with st.spinner("Sending email..."):
                res = requests.post(
                    f"{API_URL}/send_email",
                    data={"email": email},
                    headers=auth_headers()
                )
            if res.status_code == 200:
                st.success(res.json()["msg"])
            else:
                st.error(res.json().get("detail", "Failed to send email."))

#  CLEAR HISTORY

elif choice == "🗑 Clear History":
    st.title("🗑 Clear My History")
    st.warning("⚠️ This will permanently delete ALL your food history. This cannot be undone.")

    if st.button("🗑 Yes, Delete Everything"):
        res = requests.delete(f"{API_URL}/delete_history", headers=auth_headers())
        if res.status_code == 200:
            st.success("History deleted.")
        else:
            st.error("Failed to delete history.")
