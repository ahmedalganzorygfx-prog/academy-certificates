import pandas as pd
import streamlit as st

# إعداد الصفحة لتكون عريضة
st.set_page_config(
    page_title="الاستعلام عن تجديد الشهادة - فرع الجيزة", layout="wide"
)

# تخصيص التصميم ودعم اللغة العربية من اليمين لليسار (RTL)
st.markdown(
    """
    <style>
    /* توجيه كافة العناصر من اليمين لليسار */
    html, body, [class*="css"] {
        direction: rtl;
        text-align: right;
        font-family: 'Cairo', sans-serif, Arial;
    }
    
    /* تنسيق صندوق العنوان الرئيسي */
    .header-box {
        background-color: #1b5e20;
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
    }
    
    /* تنسيق الجداول والبيانات لتكون من اليمين لليسار */
    table {
        direction: rtl;
        text-align: right !important;
    }
    th, td {
        text-align: right !important;
    }
    
    /* تنسيق صناديق النجاح والتحذير */
    .stAlert {
        direction: rtl;
        text-align: right;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# رأس الصفحة (يمكنك وضع رابط اللوجو الخاص بك مكان رابط الصورة أدناه)
col1, col2 = st.columns([1, 4])

with col1:
    # ضع رابط الشعار (Logo) الخاص بالفرع هنا، أو اترك مسار الصورة المحلية
    # مثال لرابط شعار افتراضي أو يمكنك رفع الشعار بجانب الكود وتسميته logo.png
    try:
        st.image("logo.png", width=120)
    except:
        st.image(
            "https://cdn-icons-png.flaticon.com/512/3135/3135755.png", width=100
        )

with col2:
    st.markdown(
        """
        <div class="header-box">
            <h2>الأكاديمية المهنية للمعلمين - فرع الجيزة</h2>
            <h4>الاستعلام عن تجديد الشهادة</h4>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# رفع ملف إكسيل الشهادات
uploaded_file = st.file_uploader(
    "📁 برجاء رفع ملف كشف الشهادات (Excel)", type=["xlsx", "xls"]
)

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)

        # تنظيف أسماء الأعمدة لإزالة المسافات الزائدة
        df.columns = df.columns.astype(str).str.strip()

        # البحث عن عمود الرقم القومي تلقائياً
        id_column = None
        for col in df.columns:
            if "قومي" in col or "الرقم" in col or "ID" in col:
                id_column = col
                break

        if id_column is None:
            id_column = df.columns[
                0
            ]  # افتراض أن العمود الأول هو الرقم القومي إذا لم يتم العثور عليه

        st.success("تم رفع الملف بنجاح! يمكنك الآن الاستعلام.")

        # صندوق إدخال الرقم القومي
        search_query = st.text_input(
            "أدخل الرقم القومي (14 رقماً):", max_chars=14
        )

        if search_query:
            # تحويل القيم إلى نص للبحث السليم
            df[id_column] = df[id_column].astype(str).str.strip()
            result = df[df[id_column].str.contains(search_query, na=False)]

            if not result.empty:
                st.success("🎉 تم العثور على البيانات بنجاح:")
                # عرض النتائج في جدول منسق ومن اليمين لليسار
                st.dataframe(result, use_container_width=True)
            else:
                st.error(
                    "❌ عذراً، لم يتم العثور على بيانات بهذا الرقم القومي. تأكد من صحة الرقم المُدخل."
                )

    except Exception as e:
        st.error(f"حدث خطأ أثناء قراءة الملف: {e}")
else:
    st.info(
        "💡 برجاء رفع ملف الإكسيل الخاص بالشهادات لتبدأ عملية الاستعلام للأعضاء."
    )
