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
    /* تصميم بطاقة بيانات المعلم ومحاذاتها لليمين */
    .teacher-card {
        background-color: #f9f9f9;
        border: 2px solid #1b5e20;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: right;
        direction: rtl;
    }
    .card-title {
        color: #1b5e20;
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 15px;
        border-bottom: 2px solid #ddd;
        padding-bottom: 8px;
        text-align: right;
        direction: rtl;
    }
    .card-row {
        font-size: 16px;
        margin-bottom: 10px;
        color: #333;
        text-align: right;
        direction: rtl;
    }
    /* تنسيق صناديق الحالات المخصصة */
    .status-red {
        background-color: #ffebee;
        color: #c62828;
        padding: 12px;
        border-radius: 6px;
        border-right: 5px solid #c62828;
        margin-top: 15px;
        font-size: 16px;
        font-weight: bold;
        text-align: right;
        direction: rtl;
    }
    .status-green {
        background-color: #e8f5e9;
        color: #2e7d32;
        padding: 12px;
        border-radius: 6px;
        border-right: 5px solid #2e7d32;
        margin-top: 15px;
        font-size: 16px;
        font-weight: bold;
        text-align: right;
        direction: rtl;
    }
    .status-blue {
        background-color: #e3f2fd;
        color: #1565c0;
        padding: 12px;
        border-radius: 6px;
        border-right: 5px solid #1565c0;
        margin-top: 15px;
        font-size: 16px;
        font-weight: bold;
        text-align: right;
        direction: rtl;
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

    # البحث عن عمود حالة الشهادة تلقائياً
    status_column = None
    for col in df.columns:
        if "حالة" in col or "الشهادة" in col:
            status_column = col
            break

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

                # عرض النتائج في شكل بطاقات أنيقة
                for idx, row in result.iterrows():
                    # البحث الذكي والشامل عن اسم المعلم
                    name_val = "غير متوفر"
                    for c in df.columns:
                        if (
                            "اسم" in c
                            or "الاسم" in c
                            or "المعلم" in c
                            or "السيد" in c
                        ):
                            if (
                                "قومي" not in c
                                and "إدارة" not in c
                                and "الادارة" not in c
                            ):
                                name_val = str(row[c])
                                break

                    # البحث الذكي عن الإدارة
                    admin_val = "غير متوفر"
                    for c in df.columns:
                        if "الادارة" in c or "الإدارة" in c:
                            admin_val = str(row[c])
                            break

                    # البحث الذكي عن البرنامج التدريبي
                    prog_val = "غير متوفر"
                    for c in df.columns:
                        if "البرنامج" in c or "الترقي" in c or "التدريب" in c:
                            prog_val = str(row[c])
                            break

                    # البحث الذكي عن رقم المسلسل
                    serial_val = "غير متوفر"
                    for c in df.columns:
                        if "مسلسل" in c or "م" == c.strip():
                            serial_val = str(row[c])
                            break

                    # رسم البطاقة الأساسية مع محاذاة لليمين
                    card_code = f"""
                    <div class="teacher-card">
                        <div class="card-title">👤 بيانات المعلم</div>
                        <div class="card-row"><b>رقم المسلسل:</b> {serial_val}</div>
                        <div class="card-row"><b>اسم المعلم:</b> {name_val}</div>
                        <div class="card-row"><b>الرقم القومي:</b> {row[id_column]}</div>
                        <div class="card-row"><b>الإدارة التعليمية:</b> {admin_val}</div>
                        <div class="card-row"><b>البرنامج التدريبي:</b> {prog_val}</div>
                    </div>
                    """
                    st.markdown(card_code, unsafe_allow_html=True)

                    # عرض صندوق الحالة بشكل منفصل ومستقل ومحاذاة لليمين
                    if status_column:
                        status_val = str(row[status_column]).strip()
                        if "لم تصل" in status_val:
                            st.markdown(
                                """
                                <div class="status-red">
                                    🔴 لم تصل إلى الفرع حتى الآن<br>
                                    <span style="font-weight: normal; font-size: 18px; color: #333;">يرجى الاستعلام في وقت لاحق.</span>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )
                        elif "موجودة" in status_val:
                            st.markdown(
                                """
                                <div class="status-green">
                                    🟢 موجودة بالفرع<br>
                                    <span style="font-weight: normal; font-size: 18px; color: #333;">يرجى التوجه لمقر الفرع لاستلامها وبحوزتكم صحيفة أحوال الكترونية حديثة معتمدة + صورة البطاقة.</span>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )
                        elif "تسليم" in status_val:
                            st.markdown(
                                """
                                <div class="status-blue">
                                    🔵 تم تسليم الشهادة للمعلم
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )
                        else:
                            st.markdown(
                                f'<div class="status-blue">حالة الشهادة: {status_val}</div>',
                                unsafe_allow_html=True,
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
