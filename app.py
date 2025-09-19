import streamlit as st
import qrcode
from PIL import Image
from io import BytesIO
import random
import string
import json
import time

try:
    import google.generativeai as genai
except ImportError:
    st.error("The 'google-generativeai' library is not installed. Please add 'google-generativeai' to your requirements.txt file.")
    st.stop()

# IMPORTANT: API key must be empty string as Canvas will provide it at runtime.
# When running locally, you must provide your own API key.
# Replace "YOUR_API_KEY" with your actual key.
genai.configure(api_key="AIzaSyBWwrbH9ZuyB2icupMibDbv0JAHeDQyklI")

# --- Helper Functions (Same as before) ---
def generate_random_password(length=8):
    """Generate a random password for the Wi-Fi."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

def create_bill_and_qr(order, price, wifi_time):
    """Generates the bill and QR code image."""
    st.subheader(f"✅ Your Order: {order}")
    st.write("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Item:** {order}")
        st.markdown(f"**Price:** ₹{price}")
    with col2:
        st.markdown(f"**Wi-Fi Time:** {wifi_time}")
    
    st.markdown("---")
    
    wifi_ssid = "SmartBill-WiFi"
    wifi_password = generate_random_password()
    qr_data = f"WIFI:S:{wifi_ssid};T:WPA;P:{wifi_password};;"
    
    qr_img = qrcode.make(qr_data)
    buf = BytesIO()
    qr_img.save(buf, format="PNG")
    
    st.image(buf, caption="Scan this QR for Wi-Fi access", width=250)
    st.markdown(f"**Or enter manually:**")
    st.code(f"SSID: {wifi_ssid}\nPassword: {wifi_password}")
    st.markdown("<p style='text-align: center; color: grey;'>Thank you for your purchase!</p>", unsafe_allow_html=True)
    
# --- New AI Dashboard and Logic ---
def get_sample_data():
    """Simulate a small dataset for AI analysis."""
    return {
        "daily_users": {
            "Monday": 25, "Tuesday": 32, "Wednesday": 38, "Thursday": 29, 
            "Friday": 55, "Saturday": 65, "Sunday": 40
        },
        "top_orders": {
            "Espresso": 120, "Latte": 85, "Iced Tea": 60
        }
    }

def generate_ai_insight(data):
    """Call the AI model to generate a business insight."""
    model = genai.GenerativeModel('gemini-2.5-flash-preview-05-20')
    
    prompt = f"""
    You are a professional business consultant for a café. Analyze the following data and provide one actionable business recommendation.
    
    Wi-Fi Usage Data:
    - Daily users: {json.dumps(data['daily_users'])}
    
    Order Data:
    - Top orders: {json.dumps(data['top_orders'])}
    
    Based on this data, what single, clear recommendation do you have to increase revenue and customer engagement? Be witty and creative.
    """
    
    with st.spinner("🧠 Analyzing data and generating insights..."):
        try:
            response = model.generate_content(
                prompt
            )
            return response.text
        except Exception as e:
            return f"Error generating insight: {e}"

# --- Streamlit App Layout ---
st.set_page_config(page_title="SmartBill Wi-Fi Prototype", layout="centered")

st.markdown("""
<style>
    /* Global styles for a dark, elegant theme */
    body {
        font-family: 'Inter', sans-serif;
        font-weight: 400;
    }
    
    /* Overall app container with a gradient background */
    [data-testid="stAppViewContainer"] {
        background-color: #0D0D0D; 
        color: #FFFFFF;
        background-image: radial-gradient(at 0% 0%, #1a1a1a 0%, #0D0D0D 80%);
    }

    /* Sidebar styling to match the dark theme */
    [data-testid="stSidebar"] {
        background-color: #1a1a1a;
        color: #FFFFFF;
    }

    /* Main headings and titles */
    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF;
        font-weight: 600;
    }

    /* General text and paragraphs */
    p, .stMarkdown {
        color: #B0B0B0;
        line-height: 1.6;
    }
    
    /* Button styling with a vibrant gradient */
    .stButton>button {
        background-color: #2D3748;
        color: white;
        border-radius: 12px;
        padding: 10px 24px;
        font-size: 16px;
        font-weight: bold;
        transition: all 0.2s ease-in-out;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
        border: none;
        cursor: pointer;
        font-family: 'Inter', sans-serif;
    }
    .stButton>button:hover {
        background-color: #4A5568;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.5);
        transform: translateY(-2px);
    }
    .stButton>button:active {
        background-color: #1A202C;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
        transform: translateY(0);
    }
    
    /* Order button specific styles to make them visible and interactive */
    .order-button-container .stButton>button {
        background-color: #2D3748;
        color: #E2E8F0;
        border: 2px solid #4A5568;
        transition: transform 0.2s ease-in-out, background-color 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
    }
    
    .order-button-container .stButton>button:hover {
        background-color: #4A5568;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
        transform: translateY(-4px);
    }
    
    .order-button-container .stButton>button:active {
        background-color: #1A202C;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.15);
        transform: translateY(0);
    }

    /* Metric styling */
    .st-emotion-cache-1629p8f {
        color: #B0B0B0;
        font-weight: 500;
        font-size: 1rem;
    }
    .st-emotion-cache-z5065z {
        color: #FFFFFF;
        font-weight: bold;
        font-size: 2.5rem;
    }
    
    /* Chart styling to make bars visible on dark background */
    .st-emotion-cache-16k02a6 {
        color: #B0B0B0;
    }

</style>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)


st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Demo", "AI Dashboard"])

if page == "Demo":
    st.title("SmartBill Wi-Fi Prototype")
    st.markdown("Choose an order to get your purchase-linked Wi-Fi access pass.")
    st.divider()
    
    col_coffee, col_breakfast, col_lunch = st.columns(3)
    
    with col_coffee:
        st.markdown('<div class="order-button-container">', unsafe_allow_html=True)
        if st.button("☕ Coffee (₹50)"):
            create_bill_and_qr("Coffee", 50, "30 minutes")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_breakfast:
        st.markdown('<div class="order-button-container">', unsafe_allow_html=True)
        if st.button("🍳 Breakfast (₹150)"):
            create_bill_and_qr("Breakfast", 150, "1 hour")
        st.markdown('</div>', unsafe_allow_html=True)
            
    with col_lunch:
        st.markdown('<div class="order-button-container">', unsafe_allow_html=True)
        if st.button("🍲 Lunch (₹300)"):
            create_bill_and_qr("Lunch", 300, "2 hours")
        st.markdown('</div>', unsafe_allow_html=True)
            
elif page == "AI Dashboard":
    st.title("📈 Business Insights Dashboard")
    st.markdown("Analyze customer behavior and get AI-powered recommendations.")
    st.divider()
    
    data = get_sample_data()
    
    # --- Metrics Section ---
    st.subheader("📊 Key Metrics at a Glance")
    col_metrics1, col_metrics2 = st.columns(2)
    
    total_users = sum(data["daily_users"].values())
    top_selling_item = max(data["top_orders"], key=data["top_orders"].get)
    
    with col_metrics1:
        st.metric(label="Total Weekly Wi-Fi Users", value=f"{total_users}")
    with col_metrics2:
        st.metric(label="Top Selling Item", value=top_selling_item, delta=f"{data['top_orders'][top_selling_item]} sold")
    
    st.divider()
    
    # --- Chart Visualization ---
    st.subheader("📈 Weekly Wi-Fi User Trends")
    st.bar_chart(data["daily_users"])
    
    st.subheader("☕ Top Selling Items")
    st.bar_chart(data["top_orders"])
    
    st.divider()
    
    # --- AI Insight Section ---
    st.subheader("✨ AI-Powered Recommendations")
    
    if st.button("Generate an Insight", key="ai_button", help="Click to get an AI-driven business recommendation."):
        with st.container():
            st.info("Generating a personalized recommendation...")
            
            ai_insight = generate_ai_insight(data)
            
            st.markdown(f"**Actionable Recommendation:**")
            st.success(ai_insight)
    else:
        st.info("Click the button above to get a strategic recommendation based on your data.")
