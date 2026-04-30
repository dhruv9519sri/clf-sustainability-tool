import streamlit as st
import pandas as pd
import sqlite3
import json

st.set_page_config(layout="wide")
st.title("CLF Sustainability Assessment Survey")

#----------------------------
# ENUMERATOR DETAILS
#----------------------------
st.header("Enumerator Details / गणनाकर्ता विवरण")

enumerator_name = st.text_input("Enumerator Name / गणनाकर्ता का नाम")

enumerator_phone = st.text_input("Enumerator Phone Number / फ़ोन नंबर")

# Validate phone number
phone_valid = False

if enumerator_phone:
    if enumerator_phone.isdigit() and len(enumerator_phone) == 10:
        phone_valid = True
        st.success("Valid phone number")
    else:
        st.error("Phone number must be exactly 10 digits and numeric only.")

# ---------------------------
# CLF MASTER DATA
# ---------------------------
clf_data = {
    "Almora": {
        "Takula": [
            "Ujjawal Swaayat Sahkarita Takula"
        ]
    },
    "Bageshwar": {
        "Bageshwar": [
            "Garima Mahila Ajeevika Swayatt Sahkarita, Simkuna"
        ]
    },
    "Chamoli": {
        "Karanprayag": [
            "Ekata CLF-LC",
            "Ujjawal CLF-LC"
        ],
        "Dewal": [
            "Sunanda CLF-LC"
        ]
    },
    "Champawat": {
        "Champawat": [
            "Mahila Vikas CLF-LC Khrakkarki"
        ],
        "Dewal": [
            "Vikas CLF-LC Lohagat"
        ]
    },
    "Dehradun": {
        "Vikasnagar": [
            "Sangam Cluster Level Federation",
            "Abhinandan Cluster Level Federation"
        ],
        "Sahaspur": [
            "Aastha Cluster Level Federation"
        ]
    },
    "Haridwar": {
        "Bahadrabad": [
            "Shardha Mahila Cluster Federation"
        ],
        "Gordhanpur": [
            "Cluster Stariya Sahakarita, Gordhanpur"
        ]
    },
    "Nainital": {
        "Kotabag": [
            "Jagriti CLF-LC"
        ],
        "Ramgarh": [
            "Samarpan CLF-LC",
            "Swabhiman CLF-LC"
        ],
        "Betalghat": [
            "Divya Jyoti CLF-LC",
            "Saraswati CLF-LC"
        ]
    },
    "Pauri": {
        "Bironkhal": [
            "Eklakshya CLF"
        ],
        "Thalisain": [
            "Nari Shakti CLF"
        ],
        "Khirshu": [
            "Bhoomi CLF"
        ]
    },
    "Pithoragarh": {
        "Munsyari": [
            "Nai Ummid CLF-LC",
            "Nari Shakti CLF-LC"
        ]
    },
    "Rudraprayag": {
        "Ukhimath": ["Udan"],
        "Augustmuni": ["Unnati"]
    },
    "Tehri Garhwal": {
        "Chandrawadni": ["Mahila CLF Choras"],
        "Jaunpur": ["Maa Bhawani CLF Than"],
        "Jakhnidhar": ["Sangam CLF Nandgaon"]
    },
    "Udham Singh Nagar": {
        "Jaspur": [
            "Tulshi Mahila CLF Bharatpur",
            "Aradhana Mahila CLF Kasampur",
            "Sahayog Mahila CLF Puranpur"
        ]
    },
    "Uttarkashi": {
        "Dunda": ["Unnati CLF"],
        "Chinyalisaur": [
            "Jan Shakti CLF",
            "Maa Renuka CLF",
            "Sarv Shakti CLF"
        ]
    }
}

# ---------------------------
# SECTION A – BASIC INFO
# ---------------------------
st.header("SECTION A – Basic Information / बुनियादी जानकारी")

# District Dropdown
district = st.selectbox("District / जिला", sorted(clf_data.keys()))

# Block Dropdown (depends on district)
block = st.selectbox(
    "Block / ब्लॉक",
    sorted(clf_data[district].keys())
)

# CLF Dropdown (depends on block)
clf_name = st.selectbox(
    "CLF Name / सीएलएफ का नाम",
    sorted(clf_data[district][block])
)

adoption_date = st.date_input("Date of Adoption under REAP / REAP के तहत अंगीकरण की तिथि")
reap_start_date = st.date_input("Date CLF started receiving REAP support / CLF को REAP सहायता प्राप्त होने की तिथि")

respondent = st.text_input("Respondent Name & Designation / उत्तरदाता का नाम एवं पदनाम")
survey_date = st.date_input("Date of Survey / सर्वेक्षण की तिथि")

# ---------------------------
# SECTION B – PRE SUPPORT STATUS
# ---------------------------
st.header("SECTION B – Pre-Support Status / सहायता-पूर्व स्थिति")

pre_business = st.radio("Did CLF have business before REAP support? / क्या REAP सहायता से पहले CLF का कोई व्यवसाय था?", ["Yes","No"])

pre_income_source = st.text_input("Main income source before REAP / REAP से पहले आय का मुख्य स्रोत")

pre_revenue = st.number_input("Approx annual revenue before REAP (₹) / REAP से पहले अनुमानित वार्षिक राजस्व (₹)", min_value=0)

# ---------------------------
# FUNCTION FOR FY TABLES
# ---------------------------
def fy_table(section_title, items):
    st.subheader(section_title)

    df = pd.DataFrame({
        "Component": items,
        "FY 22-23": [0]*len(items),
        "FY 23-24": [0]*len(items),
        "FY 24-25": [0]*len(items),
        "FY 25-26": [0]*len(items),
    })

    edited = st.data_editor(
        df,
        use_container_width=True,
        column_config={
            "FY 22-23": st.column_config.NumberColumn(),
            "FY 23-24": st.column_config.NumberColumn(),
            "FY 24-25": st.column_config.NumberColumn(),
            "FY 25-26": st.column_config.NumberColumn(),
        }
    )

    # Row totals
    edited["Total"] = edited.iloc[:,1:].sum(axis=1)

    # FY totals
    fy_totals = edited.iloc[:,1:5].sum()

    # Add FY totals row
    total_row = pd.DataFrame(
        [["FY TOTAL"] + list(fy_totals) + [fy_totals.sum()]],
        columns=edited.columns
    )

    final_table = pd.concat([edited, total_row], ignore_index=True)

    st.dataframe(final_table, use_container_width=True)

    grand_total = fy_totals.sum()

    st.success(f"Grand Total: ₹ {grand_total:,.0f}")

    # Convert table to json
    table_json = edited.to_json()

    return grand_total, table_json
# ---------------------------
# SECTION C – REAP SUPPORT
# ---------------------------
reap_total, reap_json = fy_table(
    "SECTION C – REAP Project Support Received / REAP परियोजना से प्राप्त सहायता",
    [
        "Business Plan Support / व्यवसाय योजना सहायता",
        "Staff Support / कर्मचारी सहायता",
        "Enterprise Support / उद्यम सहायता",
        "Matching Grant / मिलान अनुदान (मैचिंग ग्रांट)",
        "Computer/Furniture / कंप्यूटर/फर्नीचर",
        "Office Rent Support / कार्यालय किराया सहायता",
        "Other REAP Support / अन्य REAP सहायता"
    ]
)

# ---------------------------

# SECTION D – OTHER GOVT SUPPORT
# ---------------------------
govt_total, govt_json = fy_table(
    "SECTION D – Other Government Support / अन्य सरकारी सहायता",
    ["Scheme Support / योजना सहायता"]
)

# ---------------------------
# SECTION E – SHARE CAPITAL & FD
# ---------------------------
st.header("SECTION E – Share Capital & FD / शेयर पूंजी और सावधि जमा")

fd_amount = st.number_input("Total FD maintained (₹) / कुल सावधि जमा राशि (₹)", min_value=0)

interest_22 = st.number_input("Interest FY 22-23 / ब्याज वित्तीय वर्ष 22-23", min_value=0)
interest_23 = st.number_input("Interest FY 23-24 / ब्याज वित्तीय वर्ष 23-24", min_value=0)
interest_24 = st.number_input("Interest FY 24-25 / ब्याज वित्तीय वर्ष 24-25", min_value=0)
interest_25 = st.number_input("Interest FY 25-26 / ब्याज वित्तीय वर्ष 25-26", min_value=0)

fd_json = json.dumps({
    "fd_amount": fd_amount,
    "interest_22": interest_22,
    "interest_23": interest_23,
    "interest_24": interest_24,
    "interest_25": interest_25
})

# ---------------------------
# SECTION F – BUSINESS REVENUE
# ---------------------------
revenue_total, revenue_json = fy_table(
    "SECTION F – Business Revenue / व्यावसायिक राजस्व",
    [
        "Aggregation/Trading / एकत्रीकरण/व्यापार",
        "Processing / प्रसंस्करण",
        "Service/Commission / सेवा/कमीशन",
        "Retail Sales / खुदरा बिक्री",
        "Other / अन्य"
    ]
)

# ---------------------------
# SECTION G – OPERATING COSTS
# ---------------------------
cost_total, cost_json = fy_table(
    "SECTION G – Operating Costs / परिचालन लागत",
    [
        "Staff Salary / कर्मचारी वेतन",
        "Office Rent / कार्यालय किराया",
        "Utilities & Admin / उपयोग और प्रशासनिक खर्च",
        "Transport / परिवहन",
        "Raw Material / कच्चा माल",
        "Other / अन्य"
    ]
)

# ---------------------------
# SECTION H – NET REVENUE & COST COVERAGE
# ---------------------------
st.header("SECTION H – Net Revenue & Cost Coverage / शुद्ध राजस्व और लागत कवरेज")

st.info("Enter values from financial records. Net revenue will calculate automatically.")

section_h = pd.DataFrame({
    "Description": [
        "Total Revenue / कुल राजस्व",
        "Operating Cost (With REAP Support) / परिचालन लागत (REAP सहायता सहित)",
        "Operating Cost (Without REAP Support) / परिचालन लागत (REAP सहायता के बिना)",
        "Net Revenue (With REAP Support) / शुद्ध राजस्व (REAP सहायता सहित)",
        "Net Revenue (Without REAP Support) / शुद्ध राजस्व (REAP सहायता के बिना)"
    ],
        "FY 22-23": [0]*5,
        "FY 23-24": [0]*5,
        "FY 24-25": [0]*5,
        "FY 25-26": [0]*5,
})

# Editable table
section_h_edit = st.data_editor(section_h, use_container_width=True)

# Auto calculate net revenue rows
for i in range(4):
    section_h_edit.iloc[3, i+1] = (
        section_h_edit.iloc[0, i+1] - section_h_edit.iloc[1, i+1]
    )
    section_h_edit.iloc[4, i+1] = (
        section_h_edit.iloc[0, i+1] - section_h_edit.iloc[2, i+1]
    )

st.dataframe(section_h_edit, use_container_width=True)
section_h_json = section_h_edit.to_json()

# ---------------------------
# SECTION I – STAFF SUSTAINABILITY
# ---------------------------
st.header("SECTION I – Staff & Sustainability / कर्मचारी एवं स्थिरता")

staff_salary_latest = st.number_input("Total annual staff salary (latest FY) / कर्मचारियों का कुल वार्षिक वेतन (नवीनतम वित्तीय वर्ष)", min_value=0)
latest_revenue = st.number_input("Total business revenue (latest FY) / कुल व्यावसायिक राजस्व (नवीनतम वित्तीय वर्ष)", min_value=0)

salary_sufficient = st.selectbox(
    "Is business revenue sufficient to pay staff salary? / क्या व्यवसाय का राजस्व कर्मचारियों के वेतन का भुगतान करने के लिए पर्याप्त है?",
    ["Yes","Partial","No"]
)

reap_stop = st.selectbox(
    "If REAP staff support stops today, can CLF sustain salaries? / यदि आज REAP स्टाफ का समर्थन बंद हो जाता है, तो क्या CLF वेतन का भुगतान जारी रख पाएगा?",
    ["Yes","Partial","No"]
)

business_plan_exists = st.selectbox(
    "Is business plan support still existing? / क्या व्यापार योजना संबंधी सहायता अभी भी जारी है?",
    ["Yes","Partial","No"]
)

# ---------------------------
# SECTION J – TAX COMPLIANCE
# ---------------------------
st.header("SECTION J – Tax Compliance & Registrations / कर अनुपालन एवं पंजीकरण")
# GST
gst_status = st.selectbox("GST Registration Status / GST पंजीकरण स्थिति", ["Yes", "No", "Applied but Pending"])
gst_number = st.text_input("GSTIN Number / GSTIN नंबर")
gst_filing = st.selectbox("GST Filing Status / GST फाइलिंग स्थिति", ["Regular", "Irregular", "No"])
gst_reason = st.text_input("Reason if not registered / यदि पंजीकृत नहीं है तो कारण")
# ITR
itr_status = st.selectbox("ITR Filing Status / ITR दाखिल करने की स्थिति", ["Regular", "Irregular", "No", "Not Applicable"])
itr_year = st.text_input("Last ITR FY / अंतिम ITR वित्तीय वर्ष")
itr_freq = st.selectbox("ITR Frequency / ITR आवृत्ति", ["Annual", "2-3 years", "Never"])
pan = st.selectbox("PAN Available? / क्या आपके पास पैन कार्ड है?", ["Yes", "No"])
pan_number = st.text_input("PAN Number / पैन नंबर")
# Licences Table

lic_df = pd.DataFrame({
    "Licence": ["FSSAI", "Udyam / उद्यम", "Trade Licence / व्यापार लाइसेंस", "Shops Act / दुकान अधिनियम", "Other / अन्य"],
    "Available": ["No"]*5,
    "Reg No": [""]*5,
    "Valid Till": [""]*5
})
lic_edit = st.data_editor(lic_df, use_container_width=True)
lic_json = lic_edit.to_json()
# GI Tag
gi = st.selectbox("GI Product? / जीआई उत्पाद?", ["Yes", "No", "Unsure"])
gi_name = st.text_input("GI Product Name / जीआई उत्पाद का नाम")
gi_reg = st.selectbox("GI Registered? / जीआई पंजीकृत?", ["Yes", "No", "Applied"])
gi_use = st.selectbox("GI Used? / जीआई का उपयोग?", ["Yes", "No", "Partially"])
gi_premium = st.selectbox("Premium due to GI? / जीआई के कारण प्रीमियम?", ["Yes", "No", "Not tracked"])
# Tax Table
tax_df = pd.DataFrame({
    "Tax": ["GST / जीएसटी", "Income Tax / आयकर", "Professional Tax / पेशेवर कर", "Licence Fees / लाइसेंस शुल्क"],
    "FY 22-23": [0]*4,
    "FY 23-24": [0]*4,
    "FY 24-25": [0]*4
})
tax_edit = st.data_editor(tax_df, use_container_width=True)
tax_json = tax_edit.to_json()
section_j_json = json.dumps({
    "gst_status": gst_status,
    "gst_number": gst_number,
    "gst_filing": gst_filing,
    "gst_reason": gst_reason,
    "itr_status": itr_status,
    "itr_year": itr_year,
    "itr_freq": itr_freq,
    "pan": pan,
    "pan_number": pan_number,
    "licences": lic_json,
    "gi": gi,
    "gi_name": gi_name,
    "gi_reg": gi_reg,
    "gi_use": gi_use,
    "gi_premium": gi_premium,
    "tax": tax_json
})

# ---------------------------
# SECTION K – GOVERNANCE
# ---------------------------
st.header("SECTION K – Governance Assessment / शासन मूल्यांकन")
# Board
board = st.number_input("Total Board Members / कुल बोर्ड सदस्य", min_value=0)
meetings = st.number_input("Meetings in FY / वित्तीय वर्ष में बैठकें", min_value=0)
quorum = st.selectbox("Quorum / कोरम", ["Always", "Mostly", "Rarely", "Never"])
mom = st.selectbox("Minutes recorded / रिकॉर्ड किए गए कार्यवृत्त", ["All", "Most", "No"])
tracking = st.selectbox("Decision tracking / निर्णय ट्रैकिंग", ["Formal", "Informal", "None"])

# AGM
agm = st.selectbox("AGM conducted? / वार्षिक आम बैठक आयोजित हुई?", ["Yes", "No"])
agm_date = st.text_input("AGM Date / वार्षिक आम बैठक की तिथि")
audit_present = st.selectbox("Audit presented? / लेखापरीक्षा प्रस्तुत की गई?", ["Yes", "No", "Not audited"])
audit = st.selectbox("Audit done? / लेखापरीक्षा पूरी हुई?", ["Yes", "No"])
audit_year = st.text_input("Audit FY / लेखापरीक्षा वित्तीय वर्ष")
# Members
members = st.number_input("Total members / कुल सदस्य", min_value=0)
active = st.number_input("Active members / सक्रिय सदस्य", min_value=0)
# Partnership
partnership = st.selectbox("Partnership? / साझेदारी?", ["Yes", "No"])
partner_name = st.text_input("Partner Name / साझेदार का नाम")
offtake = st.selectbox("Offtake agreement? / ऑफटेक समझौता?", ["Yes", "No", "Under Negotiation"])
section_k_json = json.dumps({
    "board": board,
    "meetings": meetings,
    "quorum": quorum,
    "mom": mom,
    "tracking": tracking,
    "agm": agm,
    "agm_date": agm_date,
    "audit_present": audit_present,
    "audit": audit,
    "audit_year": audit_year,
    "members": members,
    "active": active,
    "partnership": partnership,
    "partner_name": partner_name,
    "offtake": offtake
})

# ---------------------------
# SUSTAINABILITY CLASSIFICATION
# ---------------------------
st.header("Sustainability Classification")

if revenue_total > cost_total:
    status = "Sustainable"
elif revenue_total >= 0.75 * cost_total:
    status = "Near Sustainability"
elif revenue_total >= 0.25 * cost_total:
    status = "Dependent"
else:
    status = "Non-Viable"

st.success(f"Final Classification: {status}")

# ---------------------------
# SAVE DATA
# ---------------------------

if st.button("Submit Survey"):
    conn = sqlite3.connect("data_v2.db")
    c = conn.cursor()

    c.execute("""
INSERT INTO responses (
    enumerator_name,
    enumerator_phone,
    district,
    block,
    clf_name,
    survey_date,
    pre_support_business,
    pre_revenue,
    reap_support,
    govt_support,
    revenue_table,
    cost_table,
    staff_salary,
    latest_revenue,
    section_j,
    section_k,
    total_revenue,
    total_cost,
    sustainability
)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    enumerator_name,
    enumerator_phone,
    district,
    block,
    clf_name,
    str(survey_date),
    pre_business,
    pre_revenue,
    reap_json,
    govt_json,
    revenue_json,
    cost_json,
    staff_salary_latest,
    latest_revenue,
    section_j_json,
    section_k_json,
    revenue_total,
    cost_total, 
    status
))

    conn.commit()

    conn.close()

    st.success("Survey Submitted Successfully!")
