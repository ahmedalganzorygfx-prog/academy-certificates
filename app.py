import pandas as pd
import streamlit as st

# إعداد الصفحة لتكون عريضة ودعم اللغة العربية من اليمين لليسار (RTL)
st.set_page_config(
    page_title="الاستعلام عن تجديد الشهادة - فرع الجيزة", layout="wide"
)

st.markdown(
    """
    <style>
    html, body, [class*="css"] {
        direction: rtl;
        text-align: right;
        font-family: 'Cairo', sans-serif, Arial;
    }
    .header-box {
        background-color: #1b5e20;
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
    }
    table {
        direction: rtl;
        text-align: right !important;
    }
    th, td {
        text-align: right !important;
    }
    .stAlert {
        direction: rtl;
        text-align: right;
    }
    .stFormSubmitButton > button {
        background-color: #1b5e20;
        color: white;
        width: 100%;
        border-radius: 5px;
        font-weight: bold;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# رأس الصفحة مع الشعار والعنوان
col1, col2 = st.columns([1, 4])

with col1:
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

# قراءة ملف الإكسيل الثابت تلقائياً من المجلد
excel_file = "certificates.xlsx"

try:
    df = pd.read_excel(excel_file)

    # تنظيف أسماء الأعمدة لإزالة المسافات الزائدة
    df.columns = df.columns.astype(str).str.strip()

    # البحث عن عمود الرقم القومي تلقائياً
    id_column = None
    for col in df.columns:
        if "قومي" in col or "الرقم" in col or "ID" in col:
            id_column = col
            break

    if id_column is None:
        id_column = df.columns[0]

    # النص الإرشادي موجه ناحية اليمين
    st.markdown(
        '<div style="text-align: right; direction: rtl; font-size: 18px; font-weight: bold; margin-bottom: 10px;">💡 أدخل الرقم القومي الخاص بك (14 رقماً) ثم اضغط على زر بحث:</div>',
        unsafe_allow_html=True,
    )

    # تصميم نموذج البحث (Form)
    with st.form(key="search_form"):
        search_query = st.text_input("الرقم القومي:", max_chars=14)
        submit_button = st.form_submit_button(label="🔍 بحث")

    # تنفيذ البحث عند الضغط على زر بحث
    if submit_button:
        if search_query.strip():
            df[id_column] = df[id_column].astype(str).str.strip()
            result = df[df[id_column].str.contains(search_query, na=False)]

            if not result.empty:
                st.success("🎉 تم العثور على بيانات الشهادة بنجاح:")

                # ترتيب الأعمدة الأساسية لتكون في المقدمة من اليمين لليسار إذا كانت موجودة في الملف
                cols = list(result.columns)
                priority_cols = []

                # البحث عن الأعمدة بالأسماء الشبيهة
                for p in ["مسلسل", "الاسم", "الادارة", "القومي"]:
                    for c in cols:
                        if p in c and c not in priority_cols:
                            priority_cols.append(c)

                # إضافة باقي الأعمدة إن وجدت
                remaining_cols = [c for c in cols if c not in priority_cols]
                final_order = priority_cols + remaining_cols

                # عرض الجدول بالترتيب الجديد
                st.dataframe(
                    result[final_order],
                    use_container_width=True,
                    hide_index=True,
                )
            else:
                st.error(
                    "❌ عذراً، لم يتم العثور على بيانات بهذا الرقم القومي. تأكد من صحة الرقم المُدخل."
                )
        else:
            st.warning("⚠️ برجاء كتابة الرقم القومي أولاً قبل الضغط على بحث.")

except Exception as e:
    st.warning(
        "⚠️ جاري تجهيز قاعدة البيانات أو أن ملف الكشف غير متوفر حالياً. برجاء التأكد من رفع ملف (certificates.xlsx) في مجلد المشروع على GitHub."
    )
