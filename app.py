import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="الأكاديمية المهنية للمعلمين - الاستعلام عن تجديد الشهادة",
    page_icon="🎓",
    layout="centered"
)

# Custom Styling for Arabic RTL layout and professional government style
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
        text-align: right;
    }
    .main-header {
        background: linear-gradient(135deg, #1b4d3e 0%, #2c7a51 100%);
        color: white;
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .result-card {
        background-color: #f8f9fa;
        border: 2px solid #2c7a51;
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    .result-row {
        font-size: 18px;
        margin-bottom: 12px;
        padding-bottom: 8px;
        border-bottom: 1px dashed #dee2e6;
    }
    .status-msg-1 {
        background-color: #fff3cd;
        color: #856404;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #ffeeba;
        font-weight: bold;
        text-align: center;
        font-size: 18px;
        margin-top: 15px;
    }
    .status-msg-2 {
        background-color: #d4edda;
        color: #155724;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #c3e6cb;
        font-weight: bold;
        text-align: center;
        font-size: 18px;
        margin-top: 15px;
    }
    .status-msg-3 {
        background-color: #cce5ff;
        color: #004085;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #b8daff;
        font-weight: bold;
        text-align: center;
        font-size: 18px;
        margin-top: 15px;
    }
    .error-card {
        background-color: #f8d7da;
        color: #721c24;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #f5c6cb;
        text-align: center;
        font-weight: bold;
        font-size: 18px;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="main-header">
        <h2 style="margin: 0; font-size: 26px;">الأكاديمية المهنية للمعلمين</h2>
        <p style="margin: 5px 0 0 0; font-size: 20px;">الاستعلام عن تجديد الشهادة</p>
    </div>
""", unsafe_allow_html=True)

# File uploader for the Excel sheet
uploaded_file = st.file_uploader("📂 برجاء رفع ملف كشف الشهادات (Excel)", type=["xlsx", "xls"])

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
        
        # Clean column names
        df.columns = [str(c).strip() for c in df.columns]
        
        # Ensure الرقم القومي is string
        if 'الرقم القومي' in df.columns:
            df['الرقم القومي'] = df['الرقم القومي'].astype(str).str.replace('.0', '', regex=False).str.strip()
        
        st.markdown("### 🔍 أدخل الرقم القومي للاستعلام:")
        national_id = st.text_input("الرقم القومي", max_chars=14, placeholder="أدخل الرقم القومي (14 رقماً)...")
        
        if st.button("استعلام", type="primary", use_container_width=True):
            if not national_id or len(national_id.strip()) != 14:
                st.warning("⚠️ برجاء إدخال رقم قومي صحيح مكون من 14 رقماً.")
            else:
                result = df[df['الرقم القومي'] == national_id.strip()]
                
                if result.empty:
                    st.markdown("""
                        <div class="error-card">
                            ❌ عذراً، الرقم القومي غير مسجل في الكشف.
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    for idx, row in result.iterrows():
                        serial_no = row.get('مسلسل', 'غير متوفر')
                        teacher_name = row.get('اسم المعلم', 'غير متوفر')
                        admin_office = row.get('الإدارة', 'غير متوفر')
                        nat_id = row.get('الرقم القومي', 'غير متوفر')
                        program_name = row.get('اسم البرنامج', 'غير متوفر')
                        reg_date = row.get('تاريخ التسجيل', 'غير متوفر')
                        
                        raw_status = str(row.get('حالة الشهادة', '')).strip()
                        
                        # Display requested details including serial number
                        st.markdown(f"""
                            <div class="result-card">
                                <div class="result-row"><strong>🔢 رقم المسلسل:</strong> {serial_no}</div>
                                <div class="result-row"><strong>👤 اسم المعلم:</strong> {teacher_name}</div>
                                <div class="result-row"><strong>🏢 الإدارة:</strong> {admin_office}</div>
                                <div class="result-row"><strong>🆔 الرقم القومي:</strong> {nat_id}</div>
                                <div class="result-row"><strong>📚 اسم البرنامج:</strong> {program_name}</div>
                                <div class="result-row" style="border-bottom: none;"><strong>📅 تاريخ التسجيل:</strong> {reg_date}</div>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        # Determine message based on status rules
                        if raw_status in ['لم تصل', 'لم تصل إلى الفرع حتى الآن', ''] or pd.isna(row.get('حالة الشهادة')):
                            st.markdown("""
                                <div class="status-msg-1">
                                    ⏳ الحالة: لم تصل إلى الفرع حتى الآن<br>
                                    <span style="font-size: 16px; font-weight: normal;">يرجى الاستعلام في وقت لاحق</span>
                                </div>
                            """, unsafe_allow_html=True)
                        elif raw_status in ['موجودة', 'موجودة بالفرع']:
                            st.markdown("""
                                <div class="status-msg-2">
                                    ✅ الحالة: موجودة بالفرع<br>
                                    <span style="font-size: 16px; font-weight: normal; display: block; margin-top: 8px;">
                                    يرجى التوجه لمقر الفرع لاستلامها وبحوزتكم صحيفة أحوال إلكترونية حديثة معتمدة + صورة البطاقة
                                    </span>
                                </div>
                            """, unsafe_allow_html=True)
                        elif raw_status in ['تم التسليم', 'تم تسليم الشهادة للمعلم']:
                            st.markdown("""
                                <div class="status-msg-3">
                                    🎉 الحالة: تم تسليم الشهادة للمعلم<br>
                                    <span style="font-size: 16px; font-weight: normal; display: block; margin-top: 8px;">تم التسليم للمعلم</span>
                                </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                                <div class="status-msg-2">
                                    📌 الحالة: {raw_status}
                                </div>
                            """, unsafe_allow_html=True)
                            
    except Exception as e:
        st.error(f"حدث خطأ أثناء قراءة الملف: {e}")
else:
    st.info("💡 برجاء رفع ملف الـ Excel لبدء العمل.")
