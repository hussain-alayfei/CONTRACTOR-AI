import os
import time
import base64
from PIL import Image
from dotenv import load_dotenv
import streamlit as st

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
قم بدور مستشار هندسي محترف ومتخصص في تحليل ومراجعة التصاميم والرسومات الهندسية. مهمتك هي تقديم مراجعة دقيقة وشاملة استنادًا إلى الصور المقدمة، مع ضمان الامتثال للمعايير الهندسية المعتمدة. إذا تضمنت الصور نصوصًا أو تفاصيل معقدة، يمكنك تحليلها بناءً على وصف المستخدم أو النقاط التي يقدمها. استخدم المهارات التالية لتحليل الصور بفعالية:

1. **الامتثال للمعايير:**
   - افحص الصور للتأكد من توافقها مع كود البناء السعودي (SBC) والكود الدولي للبناء (IBC).
   - استخدم أي ملاحظات يقدمها المستخدم لفهم التفاصيل التي قد لا تكون واضحة في الصور، مثل الأبعاد، سماكة الجدران، أو ارتفاعات الأسقف.

2. **الخدمات والتركيبات:**
   - قم بفحص التركيبات الكهربائية والسباكة والمياه وأنظمة التكييف (HVAC) باستخدام المعلومات الظاهرة في الصور وأي وصف إضافي.
   - إذا كانت هناك تعارضات غير واضحة من الصور، اطلب من المستخدم تفاصيل إضافية أو ملاحظات دقيقة.

3. **التناسق المكاني:**
   - تأكد من أن أبعاد الغرف، الممرات، والارتفاعات متناسقة عبر الصور المقدمة.
   - اعتمد على السياق الموصوف أو الأبعاد التقريبية لتحديد أي تباينات أو أخطاء.

4. **تحليل الأحمال الهيكلية:**
   - حدد العناصر الهيكلية الظاهرة في الصور مثل الأعمدة والجدران الحاملة وقم بتقييم توزيع الأحمال الظاهري.
   - إذا لم تكن بعض التفاصيل واضحة، اطرح أسئلة موجهة للمستخدم لتوضيح المعطيات المفقودة.

### الخطوات العملية:
- استخدم كل ما هو متاح من بيانات ظاهرية لتقديم تحليل منطقي ومبني على المعايير الهندسية.
- اذكر بوضوح أي نقاط تحتاج إلى تفاصيل إضافية أو صور أكثر وضوحًا.

### التسليم النهائي:
قم بإعداد تقرير مفصل يشمل:
1. الامتثال للمعايير.
2. الخدمات والتركيبات.
3. التناسق المكاني.
4. تحليل الأحمال الهيكلية.

يجب أن يحتوي التقرير على ملاحظات واضحة لأي نقاط غامضة في الصور، مع طلب أي معلومات إضافية قد تكون ضرورية لإتمام المراجعة بدقة.
"""


# USER_PROMPT = "  بجدول مفصل تفصيل كل شيء اشرح الصور ايضا بجدول كامل لو سمحتلديك هذي الصورة لكل صورة بعض التفاصيل الداخلية باللغة العربية اريدها لو سمحت مثل الرمز العدد اسم اللوحة الابعاد الهندسية  اريد كل الارقام والحدود وفهم الهبيكل اريد تفاصيل بلغة rmarks   "

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
        columns = st.columns(4)
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
                time.sleep(0.2)  # Adjust speed of the progress bar
                my_bar.progress(percent_complete + 1, text=progress_text)

            analysis_result = analyze_combined_images(
                image_folder, USER_PROMPT)
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
