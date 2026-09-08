import os
import pandas as pd
import streamlit as st

# إعداد الصفحة لتكون عريضة ودعم اللغة العربية من اليمين لليسار (RTL)
st.set_page_config(
    page_title="الاستعلام عن تجديد الشهادة - فرع الجيزة",
    layout="wide",
    page_icon="🏛️",
)

# تطبيق التنسيق عبر CSS
st.markdown(
    """
    <style>
    /* تغيير خلفية التطبيق بالكامل لتصبح داكنة */
    .stApp {
        background-color: #0e1117;
        color: #e0e0e0;
    }
    html, body, [class*="css"] {
        direction: rtl;
        text-align: right;
        font-family: 'Cairo', sans-serif, Arial;
        color: #e0e0e0;
    }
    /* تصميم رأس الصفحة بلون كحلي داكن فاخر ومتمركز */
    .header-box {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 25px;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.5);
    }
    .header-box h2 {
        color: #ffffff;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .header-box h4 {
        color: #58a6ff;
        margin-bottom: 8px;
    }
    .header-box p {
        color: #8b949e;
        font-size: 14px;
        margin: 0;
    }
    /* تنسيق اللون الأصفر للبرامج التدريبية */
    .programs-text {
        color: #ffcc00 !important;
        font-weight: bold;
    }
    /* تنسيق مميز بخط أكبر ولون لافت لتعليمات الاستلام */
    .pickup-instructions {
        font-size: 17px !important;
        color: #ffe566 !important;
        font-weight: bold;
        margin-top: 8px;
        display: block;
    }
    .stAlert {
        direction: rtl;
        text-align: right;
    }
    /* زر البحث */
    .stFormSubmitButton > button {
        background-color: #21262d;
        color: white;
        width: 100%;
        border-radius: 6px;
        border: 1px solid #30363d;
        font-weight: bold;
    }
    .stFormSubmitButton > button:hover {
        background-color: #30363d;
        border-color: #8b949e;
    }
    /* جعل تسمية خانة الإدخال باللون الأبيض */
    .stTextInput label {
        color: #ffffff !important;
        font-weight: bold !important;
    }
    /* تصميم خانة الإدخال لتتناغم مع التصميم الداكن */
    .stTextInput input {
        background-color: #161b22 !important;
        color: white !important;
        border: 1px solid #30363d !important;
        border-radius: 6px !important;
    }
    /* تصميم بطاقة بيانات المعلم الداكنة */
    .teacher-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 22px;
        border-radius: 12px;
        margin-bottom: 20px;
        box-shadow: 0 6px 15px rgba(0,0,0,0.4);
        text-align: right;
        direction: rtl;
    }
    .card-title {
        color: #58a6ff;
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 15px;
        border-bottom: 1px solid #30363d;
        padding-bottom: 8px;
        text-align: right;
        direction: rtl;
    }
    .card-row {
        font-size: 16px;
        margin-bottom: 10px;
        color: #c9d1d9;
        text-align: right;
        direction: rtl;
    }
    /* تنسيق صناديق الحالات المخصصة */
    .status-red {
        background-color: rgba(248, 81, 73, 0.15);
        color: #ff7b72;
        padding: 14px;
        border-radius: 8px;
        border-right: 5px solid #f85149;
        margin-top: 15px;
        font-size: 16px;
        font-weight: bold;
        text-align: center;
        direction: rtl;
        border-top: 1px solid rgba(248, 81, 73, 0.2);
        border-bottom: 1px solid rgba(248, 81, 73, 0.2);
        border-left: 1px solid rgba(248, 81, 73, 0.2);
    }
    .status-green {
        background-color: rgba(46, 160, 67, 0.15);
        color: #3fb950;
        padding: 14px;
        border-radius: 8px;
        border-right: 5px solid #2ea043;
        margin-top: 15px;
        font-size: 16px;
        font-weight: bold;
        text-align: center;
        direction: rtl;
        border-top: 1px solid rgba(46, 160, 67, 0.2);
        border-bottom: 1px solid rgba(46, 160, 67, 0.2);
        border-left: 1px solid rgba(46, 160, 67, 0.2);
    }
    .status-blue {
        background-color: rgba(56, 139, 253, 0.15);
        color: #58a6ff;
        padding: 14px;
        border-radius: 8px;
        border-right: 5px solid #388bfd;
        margin-top: 15px;
        font-size: 16px;
        font-weight: bold;
        text-align: center;
        direction: rtl;
        border-top: 1px solid rgba(56, 139, 253, 0.2);
        border-bottom: 1px solid rgba(56, 139, 253, 0.2);
        border-left: 1px solid rgba(56, 139, 253, 0.2);
    }
    /* تنسيق تذييل الصفحة (Footer) */
    .footer {
        margin-top: 50px;
        padding: 20px;
        text-align: center;
        border-top: 1px solid #30363d;
        color: #8b949e;
        font-size: 14px;
        direction: rtl;
        line-height: 1.8;
    }
    .location-link {
        color: #58a6ff !important;
        text-decoration: none;
        font-weight: bold;
    }
    .location-link:hover {
        text-decoration: underline;
        color: #79c0ff !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# وضع الشعار في منتصف الصفحة تماماً من الأعلى
col_spacer1, col_logo, col_spacer2 = st.columns([2, 1, 2])
with col_logo:
    logo_path = "logo.png"
    if os.path.exists(logo_path):
        st.image(logo_path, width=130)
    else:
        found = False
        for file in os.listdir("."):
            if file.lower().startswith("logo") and file.lower().endswith(
                (".png", ".jpg", ".jpeg")
            ):
                st.image(file, width=130)
                found = True
                break
        if not found:
            st.image(
                "https://cdn-icons-png.flaticon.com/512/3135/3135755.png",
                width=110,
            )

# صندوق العنوان والبرامج التدريبية
st.markdown(
    """
    <div class="header-box">
        <h2>🏛️ الأكاديمية المهنية للمعلمين - فرع الجيزة</h2>
        <h4>الاستعلام عن تجديد شهادة القيادة والإشراف</h4>
        <p><b>البرامج التدريبية :</b> <span class="programs-text">مدير ووكيل إدارة تعليمية &nbsp;|&nbsp; مدير ووكيل إدارة مدرسية &nbsp;|&nbsp; أساسيات التوجيه الفني</span></p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")


# دالة قراءة البيانات وتسريعها عبر الذاكرة المخبأة (Caching)
@st.cache_data(ttl=600)  # يتم تحديث الكاش كل 10 دقائق تلقائياً
def load_data(file_path):
    if not os.path.exists(file_path):
        return None
    df = pd.read_excel(file_path, dtype=str)
    df.columns = df.columns.astype(str).str.strip()
    return df


excel_file = "certificates.xlsx"
df = load_data(excel_file)

if df is not None:
    # 1. تحديد عمود الرقم القومي
    id_column = None
    for col in df.columns:
        if any(keyword in col for keyword in ["قومي", "الرقم", "ID"]):
            id_column = col
            break
    if id_column is None:
        id_column = df.columns[0]

    # 2. تحديد عمود حالة الشهادة
    status_column = None
    for col in df.columns:
        if any(keyword in col for keyword in ["حالة", "الشهادة"]):
            status_column = col
            break

    # النص الإرشادي
    st.markdown(
        '<div style="text-align: right; direction: rtl; font-size: 18px; font-weight: bold; margin-bottom: 10px; color: #c9d1d9;">💡 أدخل الرقم القومي الخاص بك (14 رقماً) ثم اضغط على زر بحث:</div>',
        unsafe_allow_html=True,
    )

    # نموذج البحث
    with st.form(key="search_form"):
        search_query = st.text_input("الرقم القومي:", max_chars=14).strip()
        submit_button = st.form_submit_button(label="🔍 بحث")

    if submit_button:
        if search_query:
            # تنظيف عمود الرقم القومي والبحث فيه
            df[id_column] = (
                df[id_column]
                .astype(str)
                .str.replace(r"\.0$", "", regex=True)
                .str.strip()
            )
            result = df[df[id_column] == search_query]

            if result.empty:
                result = df[df[id_column].str.contains(search_query, na=False)]

            if not result.empty:
                st.success("🎉 تم العثور على بيانات الشهادة بنجاح:")

                for idx, row in result.iterrows():
                    # البحث الذكي عن اسم المعلم
                    name_val = "غير متوفر"
                    for c in df.columns:
                        if any(
                            k in c for k in ["اسم", "الاسم", "المعلم", "السيد"]
                        ) and not any(
                            k in c for k in ["قومي", "إدارة", "الادارة"]
                        ):
                            name_val = str(row[c]) if pd.notna(row[c]) else "غير متوفر"
                            break

                    # البحث الذكي عن الإدارة
                    admin_val = "غير متوفر"
                    for c in df.columns:
                        if "الادارة" in c or "الإدارة" in c:
                            admin_val = str(row[c]) if pd.notna(row[c]) else "غير متوفر"
                            break

                    # البحث الذكي عن البرنامج التدريبي
                    prog_val = "غير متوفر"
                    for c in df.columns:
                        if any(k in c for k in ["البرنامج", "الترقي", "التدريب"]):
                            prog_val = str(row[c]) if pd.notna(row[c]) else "غير متوفر"
                            break

                    # البحث الذكي عن رقم المسلسل
                    serial_val = "غير متوفر"
                    for c in df.columns:
                        if "مسلسل" in c or c.strip() == "m":
                            serial_val = str(row[c]) if pd.notna(row[c]) else "غير متوفر"
                            break

                    # عرض بطاقة البيانات
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

                    # عرض حالة الشهادة
                    if status_column and pd.notna(row[status_column]):
                        status_val = str(row[status_column]).strip()
                        if "لم تصل" in status_val:
                            st.markdown(
                                """
                                <div class="status-red">
                                    🔴 لم تصل إلى الفرع حتى الآن<br>
                                    <span style="font-weight: normal; font-size: 14px; color: #8b949e;">يرجى الاستعلام في وقت لاحق.</span>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )
                        elif "موجودة" in status_val:
                            st.markdown(
                                """
                                <div class="status-green">
                                    🟢 موجودة بالفرع<br>
                                    <span class="pickup-instructions">📌 يرجى التوجه لمقر الفرع لاستلامها مع احضار صحيفة أحوال إلكترونية حديثة معتمدة + صورة البطاقة.</span>
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
else:
    st.warning(
        "⚠️ جاري تجهيز قاعدة البيانات أو أن ملف الكشف غير متوفر حالياً. برجاء التأكد من رفع ملف (certificates.xlsx) في مجلد المشروع على GitHub."
    )

# تذييل الصفحة (Footer) مع عنوان ورابط موقع الفرع
st.markdown(
    """
    <div class="footer">
        📍 <b>مقر الفرع:</b> الأكاديمية المهنية للمعلمين - فرع الجيزة<br>
        🗺️ <a href="https://share.google/RUJSeiO0XnMXz7hwY" target="_blank" class="location-link">اضغط هنا للوصول لموقع الفرع على الخريطة (Google Maps)</a><br><br>
        تصميم وتنفيذ <b>أحمد الجنزوري</b> - مدير الفرع
    </div>
    """,
    unsafe_allow_html=True,
)
