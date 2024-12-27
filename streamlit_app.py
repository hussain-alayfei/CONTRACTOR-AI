import os
import time
import base64
from PIL import Image
from dotenv import load_dotenv
import streamlit as st
import random
import time

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
            combined_images.append({"type": "image_url", "image_url": {
                                   "url": f"data:image/jpeg;base64,{base64_image}"}})

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
قم بدور مستشار هندسي محترف ومتخصص في تحليل ومراجعة التصاميم الهندسية وفقًا للكود السعودي للبناء (SBC). مهمتك تشمل الآتي:

### المهام المطلوبة:

#### 1. الامتثال للمعايير الهندسية:
- مراجعة تصميم الأعمدة والقواعد للتأكد من توافقها مع معايير الأحمال، الخرسانة، والتسليح وفقًا للكود السعودي.  
- التحقق من أقطار حديد التسليح ومسافات الأعمدة بما يتماشى مع متطلبات الكود.  
- تحليل ميول تصريف الأمطار للتأكد من توافقها مع SBC 701.  
- مراجعة تمديدات السباكة والصرف الصحي لضمان الامتثال لمتطلبات SBC 501.

#### 2. كشف التداخلات والتعارضات:
- إجراء تحليل كشف تصادم (Clash Detection) لتحديد التعارضات بين الأنظمة المختلفة (إنشائي، كهربائي، صحي).  
- الإبلاغ عن أي اختلافات في الأبعاد، المساحات، أو الارتفاعات بين المخططات.

#### 3. إعداد  جدول شامل: 
انشئ جدول مثل هذا 
البند,الكمية المقدرة
حديد التسليح للأعمدة,15 طن تقريباً
خرسانة الأعمدة,50 متر مكعب
حديد التسليح للقواعد,10 طن تقريباً
خرسانة القواعد,30 متر مكعب
أنابيب الصرف الصحي,120 متر
مواد تصريف مياه الأمطار,50 متر (مواسير + منافذ تصريف)

- في حال عدم وجود مشاكل، قم بتقديم تقرير يتضمن الكميات المطلوبة للمشروع:
  - كميات الحديد (التسليح).  
  - كميات الخرسانة للقواعد والأعمدة.  
  - أطوال الأنابيب الصحية.  
  - المواد المطلوبة لتصريف مياه الأمطار.  
  - أي مواد أخرى ضرورية.

#### خطوات العمل:
1. راجع التفاصيل الهندسية المعروضة في المخططات باستخدام البيانات المقدمة.  
2. إذا وجدت نقاط غامضة أو غير واضحة، قدم ملاحظات أو استفسارات محددة.  
3. تأكد من أن التقرير واضح وشامل وجاهز للتنفيذ.

### مخرجات العمل:
تقرير هندسي شامل يحتوي على:
- تحليل الامتثال للمعايير.  
- كشف التداخلات أو التعارضات.  
- الكميات التفصيلية المطلوبة للمشروع.  
ملاحظات :
- لا اريد منه ان يقترح لي تطبيقات اخرى اريد فقط تحليل هذي البيانات وتقديم اجابة ممتازة
- اريد اضافة تنسيقات للنص في صيغة rmarks 
- لا اريد ان يقول لا استطيع 


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
    st.error(
        "📁 لم يتم العثور على مجلد الصور. الرجاء إنشاء مجلد 'images' وإضافة الصور إليه.")
else:
    image_files = [f for f in os.listdir(
        image_folder) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
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
            # List of analysis status messages
            status_messages = [
                "🔄 جاري التحليل...",
                time.sleep(10)
                "🔍 جاري مطابقة المعايير...",
                time.sleep(10)
                "📊 جاري حساب الكميات...",
                time.sleep(10)
                "📝 جاري كتابة التقرير..."
            ]

            status_placeholder = st.empty()

            # Cycle through status messages
            for _ in range(3):  # Cycle through messages 3 times
                for message in status_messages:
                    status_placeholder.markdown(
                        f"<h3 style='text-align: center;'>{message}</h3>",
                        unsafe_allow_html=True
                    )
                    time.sleep(0.8)

            analysis_result = analyze_combined_images(
                image_folder, USER_PROMPT)
            status_placeholder.empty()

            st.success("✅ تم تحليل المخططات بنجاح!")

            # Centered analysis title and result
            st.markdown("""
                <h2 style='text-align: center; color: #f39c12; margin-bottom: 1.5rem;'>
                    📝 نتيجة التحليل
                </h2>
            """, unsafe_allow_html=True)

            st.markdown(f"""
                <div style='
                    background-color: #34495e;
                    padding: 2rem;
                    border-radius: 15px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                    margin: 0 auto;
                    max-width: 800px;
                    text-align: right;
                    direction: rtl;
                    color: #ecf0f1;
                '>
                    <p style='font-size: 1.1rem; line-height: 1.6;'>{analysis_result}</p>
                </div>
            """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
    <div style='text-align: center; padding: 1rem; color: #7f8c8d;'>
        <p style='font-size: 0.8rem;'>جميع الحقوق محفوظة لدى contractor.ai</p>
    </div>
""", unsafe_allow_html=True)
