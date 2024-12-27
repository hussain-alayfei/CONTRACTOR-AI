import os
import time
import base64
from PIL import Image
from dotenv import load_dotenv
import streamlit as st
import random

st.set_page_config(
    page_title="عقار",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load API key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Custom CSS for dark mode and enhanced UI
st.markdown("""
    <style>
    body {
        background-color: #1e1e2f;
        color: #d1d1e0;
        direction: rtl;
        text-align: right;
    }
    h1 {
        font-size: 3rem;
        color: #f39c12;
        text-align: center;
        font-weight: bold;
        text-shadow: 2px 2px 8px #000;
    }
    .stButton button {
        background-color: #34495e;
        color: white;
        border-radius: 10px;
        padding: 0.7rem 2rem;
        font-weight: bold;
        border: none;
        transition: 0.3s ease;
        margin: 1rem auto;
        display: block;
    }
    .stButton button:hover {
        background-color: #2c3e50;
    }
    .analysis-results {
        background-color: #34495e;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        margin-top: 1rem;
        color: #ecf0f1;
    }
    </style>
""", unsafe_allow_html=True)

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def analyze_combined_images(image_folder, prompt):
    combined_images = []
    for image_name in os.listdir(image_folder):
        if image_name.lower().endswith((".jpg", ".jpeg", ".png")):
            image_path = os.path.join(image_folder, image_name)
            base64_image = encode_image(image_path)
            combined_images.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}})

    if not combined_images:
        return "No valid images found for analysis."

    from openai import OpenAI
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": USER_PROMPT},
                    *combined_images
                ],
            }
        ],
        max_tokens=1000,
    )
    return response.choices[0].message.content

USER_PROMPT = """
هذي محتويات الصورة افهمها وقم بالتالي
*المهام المطلوبة:*  
1. *تحليل المطابقة للكود السعودي للبناء (SBC):*  
- قارن تصميم الأعمدة والقواعد مع متطلبات الكود السعودي للأحمال والخرسانة والتسليح.  
- تأكد من توافق أقطار الحديد (التسليح) ومسافات الأعمدة مع معايير الكود.  
- تحقق من ميول تصريف الأمطار والتمديدات الصحية مع متطلبات SBC 701 وSBC 501.  

2. *تحليل الإنشائي والكهربائي والصحي:*  
- اكتشف أي تصادم بين الأنظمة الإنشائية والكهربائية والصحية باستخدام Clash Detection.  
- تحقق من وجود تداخلات بين تمديدات السباكة والكهرباء أو أي اختلافات في المساحات والارتفاعات.  

3. *إعداد تقرير شامل:*  
- إذا لم توجد مشاكل أو أخطاء في التصميم، قم بإعداد تقرير تفصيلي لحساب الكميات المطلوبة للمشروع، بما في ذلك:  
  - كميات الحديد (التسليح)  
  - كميات الخرسانة للقواعد والأعمدة  
  - أطوال الأنابيب الصحية  
  - الميول المطلوبة لتصريف الأمطار  
  - أي مواد إنشائية أخرى مطلوبة للمشروع  
- قدم التقرير بصيغة واضحة وجاهزة للتنفيذ.

"""


st.markdown("""
    <div>
        <h1>🔍CONTRACTOR.AI</h1>
        <p style='text-align: center; font-size: 1.2rem;'>موادك بحساب، وتكلفتك بمتياز!</p>
    </div>
""", unsafe_allow_html=True)

if not api_key:
    st.error("⚠️ لم يتم العثور على مفتاح API! الرجاء إضافته في ملف .env")
    st.stop()
image_folder = "images"
if not os.path.exists(image_folder):
    st.error("📁 لم يتم العثور على مجلد الصور. الرجاء إنشاء مجلد 'images' وإضافة الصور إليه.")
else:
    image_files = [f for f in os.listdir(image_folder) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    if not image_files:
        st.warning("🖼️ لم يتم العثور على صور في المجلد!")
    else:
        st.subheader("📁 المخططات الحالية:")

        # Organize images in rows and columns
        columns = st.columns(2)
        for i, image_name in enumerate(image_files):
            image_path = os.path.join(image_folder, image_name)
            image = Image.open(image_path)
            with columns[i % len(columns)]:
                st.image(image, caption=image_name, use_container_width=True)

        if st.button("🔍 تحليل المخططات ! "):
            progress_text = "🔄 جاري تحليل المخططات..."
            my_bar = st.progress(0, text=progress_text)

            # Simulate progress bar until the analysis is complete
            for percent_complete in range(100):
                time.sleep(0.4)  # Adjust speed of the progress bar
                my_bar.progress(percent_complete + 1, text=progress_text)

            analysis_result = analyze_combined_images(image_folder, USER_PROMPT)
            my_bar.empty()

            st.success("✅ تم تحليل المخططات بنجاح!")
            st.markdown("### 📝 نتيجة التحليل:")
            st.markdown(f"""
                <div class='analysis-results'>
                    <p>{analysis_result}</p>
                </div>
            """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
    <div style='text-align: center; padding: 1rem; color: #7f8c8d;'>
        <p style='font-size: 0.8rem;'>جميع الحقوق محفوظة لدى contractor.ai</p>
    </div>
""", unsafe_allow_html=True)