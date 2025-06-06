import streamlit as st
import pandas as pd
from PIL import Image

# -------------------------
# 1) APP CONFIGURATION
# -------------------------
st.set_page_config(
    page_title="Herbal Product Recommender",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------
# 2) DATA
# -------------------------
data = {
    'Name': ['Ashwagandha', 'Tulsi Drops', 'Aloe Vera Gel', 'Triphala Powder', 'Brahmi', 'Neem Capsules', 'Giloy'],
    'Category': ['Energy', 'Immunity', 'Skincare', 'Digestive', 'Brain Health', 'Skincare', 'Immunity'],
    'Benefits': [
        'Reduces stress and increases vitality',
        'Boosts immunity and fights colds',
        'Heals skin and reduces acne',
        'Improves digestion and detoxifies body',
        'Enhances memory and cognitive function',
        'Purifies blood and prevents acne',
        'Fights infections and purifies blood'
    ],
    'Recommended_For': ['Stress', 'Immunity', 'Acne', 'Digestion', 'Memory', 'Acne', 'Immunity'],
    'Price': [250, 180, 150, 200, 220, 160, 190],
    'Images_File': [
        'Images_File/Ashwagandha.jpg',
        'Images_File/Tulsi.jpg',
        'Images_File/AloeVera.jpg',
        'Images_File/Powder.jpg',
        'Images_File/Brahmi.jpg',
        'Images_File/Neems Capsule.jpg',
        'Images_File/Giloy.jpg'
    ]
}
df = pd.DataFrame(data)

# -------------------------
# 3) SIDEBAR NAVIGATION
# -------------------------
st.sidebar.title("🌿 Navigation")
page = st.sidebar.radio("Go to", ["Home", "Recommendations", "Gallery"])

# -------------------------
# 4) CUSTOM STYLING
# -------------------------
st.markdown("""
    <style>
    .stApp {
        background-color: #f0f9f0;
        font-family: 'Segoe UI', sans-serif;
        color: #1b3a1b;
    }
    h1, h2, h3, h4 {
        color: #2e7d32;
    }
    header[data-testid="stHeader"] {
        background-color: #d4f5d0;
        box-shadow: 0 1px 4px rgba(0,0,0,0.1);
    }
    section[data-testid="stSidebar"] {
        background-color: #d4f5d0;
        border-right: 1px solid #c3eac2;
    }
    .stSelectbox > div {
        background-color: #e0f2e9;
        border-radius: 5px;
        color: #1b3a1b;
    }
    .product-card {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .footer-placeholder {
        text-align: center;
        margin-top: 2rem;
        color: gray;
        font-size: 0.8rem;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------
# 5) HOME PAGE
# -------------------------
if page == "Home":
    st.title("🌿 Welcome to AyurHerb Recommender")
    st.markdown("""
        Discover natural herbal remedies tailored to your health needs.  
        Whether you're looking to reduce stress, boost immunity, or care for your skin – we've got suggestions for you.
    """)
    st.markdown("### 🨭 How to use:")
    st.markdown("""
    1. Go to the Recommendations tab and select a health concern.  
    2. View personalized herbal product suggestions.  
    3. Explore all herbal items visually in the Gallery tab.  
    """)

# -------------------------
# 6) RECOMMENDATIONS PAGE
# -------------------------
elif page == "Recommendations":
    st.title("🌿 Herbal Product Recommendations")
    st.markdown("Select your health concern below to receive personalized herbal product suggestions tailored for you.")

    selected_issue = st.selectbox(
        "Choose a health concern:",
        [""] + sorted(df['Recommended_For'].unique()),
        index=0,
        help="Pick a health issue to get matching herbal product recommendations."
    )

    st.markdown("""
        <style>
        .herb-card {
            background: #ffffff;
            border-left: 8px solid #4caf50;
            padding: 20px 25px;
            margin-bottom: 25px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(76, 175, 80, 0.2);
            transition: transform 0.2s ease-in-out;
        }
        .herb-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(76, 175, 80, 0.35);
        }
        .herb-card h4 {
            margin-bottom: 10px;
            color: #2e7d32;
            font-weight: 700;
            font-size: 1.4rem;
        }
        .herb-card p {
            margin: 5px 0;
            font-size: 1rem;
            line-height: 1.4;
            color: #3a4f18;
        }
        .stImage > img {
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            object-fit: contain;
        }
        </style>
    """, unsafe_allow_html=True)

    if selected_issue:
        results = df[df['Recommended_For'] == selected_issue]
        st.markdown(f"### 🌱 Found {len(results)} recommendation(s) for {selected_issue}:")

        for _, row in results.iterrows():
            img_col, text_col = st.columns([1, 3])
            with img_col:
                try:
                    image = Image.open(row["Images_File"])
                    st.image(image, width=140, caption=row['Name'])
                except Exception:
                    st.markdown("🖼 Image not found")

            with text_col:
                st.markdown(f"""
                <div class='herb-card'>
                    <h4>{row['Name']}</h4>
                    <p><strong>Category:</strong> {row['Category']}</p>
                    <p><strong>Benefits:</strong> {row['Benefits']}</p>
                    <p><strong>Price:</strong> ₹{row['Price']}</p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("✨ Please select a health concern from the dropdown above to view herbal product recommendations.")

# -------------------------
# 7) GALLERY PAGE
# -------------------------
elif page == "Gallery":
    st.title("🖼 Herbal Products Gallery")

    num_cols = 3
    rows = [df[i:i + num_cols] for i in range(0, len(df), num_cols)]

    for row_items in rows:
        cols = st.columns(num_cols)
        for col, (_, row) in zip(cols, row_items.iterrows()):
            with col:
                try:
                    image = Image.open(row["Images_File"]).resize((200, 200))
                    st.image(image)
                except:
                    st.warning(f"Image not found for {row['Name']}")
                st.markdown(f"<h4 style='color:green'>{row['Name']}</h4>", unsafe_allow_html=True)
                st.markdown(f"*Benefits:* {row['Benefits']}")
                st.markdown(f"*Price:* ₹{row['Price']}")

# -------------------------
# 8) FOOTER
# -------------------------
st.markdown('<div class="footer-placeholder">© 2025 Herbal Recommender Demo</div>', unsafe_allow_html=True)
