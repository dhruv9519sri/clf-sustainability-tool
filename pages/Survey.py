import streamlit as st
import pandas as pd
import sqlite3
import json

st.set_page_config(layout="wide")
st.title("CLF Sustainability Assessment Survey")

#----------------------------
# ENUMERATOR DETAILS
#----------------------------
st.header("Enumerator Details")

enumerator_name = st.text_input("Enumerator Name")

enumerator_phone = st.text_input("Enumerator Phone Number")

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
st.header("SECTION A – Basic Information")

# District Dropdown
district = st.selectbox("District", sorted(clf_data.keys()))

# Block Dropdown (depends on district)
block = st.selectbox(
    "Block",
    sorted(clf_data[district].keys())
)

# CLF Dropdown (depends on block)
clf_name = st.selectbox(
    "CLF Name",
    sorted(clf_data[district][block])
)

adoption_date = st.date_input("Date of Adoption under REAP")
reap_start_date = st.date_input("Date CLF started receiving REAP support")

respondent = st.text_input("Respondent Name & Designation")
survey_date = st.date_input("Date of Survey")

# ---------------------------
# SECTION B – PRE SUPPORT STATUS
# ---------------------------
st.header("SECTION B – Pre-Support Status")

pre_business = st.radio("Did CLF have business before REAP support?", ["Yes","No"])

pre_income_source = st.text_input("Main income source before REAP")

pre_revenue = st.number_input("Approx annual revenue before REAP (₹)", min_value=0)

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
    "SECTION C – REAP Project Support Received",
    [
        "Business Plan Support",
        "Staff Support",
        "Enterprise Support",
        "Matching Grant",
        "Computer/Furniture",
        "Office Rent Support",
        "Other REAP Support"
    ]
)

# ---------------------------

# SECTION D – OTHER GOVT SUPPORT
# ---------------------------
govt_total, govt_json = fy_table(
    "SECTION D – Other Government Support",
    ["Scheme Support"]
)

# ---------------------------
# SECTION E – SHARE CAPITAL & FD
# ---------------------------
st.header("SECTION E – Share Capital & FD")

fd_amount = st.number_input("Total FD maintained (₹)", min_value=0)

interest_22 = st.number_input("Interest FY 22-23", min_value=0)
interest_23 = st.number_input("Interest FY 23-24", min_value=0)
interest_24 = st.number_input("Interest FY 24-25", min_value=0)
interest_25 = st.number_input("Interest FY 25-26", min_value=0)

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
    "SECTION F – Business Revenue",
    [
        "Aggregation/Trading",
        "Processing",
        "Service/Commission",
        "Retail Sales",
        "Other"
    ]
)

# ---------------------------
# SECTION G – OPERATING COSTS
# ---------------------------
cost_total, cost_json = fy_table(
    "SECTION G – Operating Costs",
    [
        "Staff Salary",
        "Office Rent",
        "Utilities & Admin",
        "Transport",
        "Raw Material",
        "Other"
    ]
)

# ---------------------------
# SECTION H – NET REVENUE & COST COVERAGE
# ---------------------------
st.header("SECTION H – Net Revenue & Cost Coverage")

st.info("Enter values from financial records. Net revenue will calculate automatically.")

section_h = pd.DataFrame({
    "Description": [
        "Total Revenue",
        "Operating Cost (With REAP Support)",
        "Operating Cost (Without REAP Support)",
        "Net Revenue (With REAP Support)",
        "Net Revenue (Without REAP Support)"
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
st.header("SECTION I – Staff & Sustainability")

staff_salary_latest = st.number_input("Total annual staff salary (latest FY)", min_value=0)
latest_revenue = st.number_input("Total business revenue (latest FY)", min_value=0)

salary_sufficient = st.selectbox(
    "Is business revenue sufficient to pay staff salary?",
    ["Yes","Partial","No"]
)

reap_stop = st.selectbox(
    "If REAP staff support stops today, can CLF sustain salaries?",
    ["Yes","Partial","No"]
)

business_plan_exists = st.selectbox(
    "Is business plan support still existing?",
    ["Yes","Partial","No"]
)

# ---------------------------
# SECTION J – TAX COMPLIANCE
# ---------------------------
st.header("SECTION J – Tax Compliance & Registrations")
# GST
gst_status = st.selectbox("GST Registration Status", ["Yes", "No", "Applied but Pending"])
gst_number = st.text_input("GSTIN Number")
gst_filing = st.selectbox("GST Filing Status", ["Regular", "Irregular", "No"])
gst_reason = st.text_input("Reason if not registered")
# ITR
itr_status = st.selectbox("ITR Filing Status", ["Regular", "Irregular", "No", "Not Applicable"])
itr_year = st.text_input("Last ITR FY")
itr_freq = st.selectbox("ITR Frequency", ["Annual", "2-3 years", "Never"])
pan = st.selectbox("PAN Available?", ["Yes", "No"])
pan_number = st.text_input("PAN Number")
# Licences Table

lic_df = pd.DataFrame({
    "Licence": ["FSSAI", "Udyam", "Trade Licence", "Shops Act", "Other"],
    "Available": ["No"]*5,
    "Reg No": [""]*5,
    "Valid Till": [""]*5
})
lic_edit = st.data_editor(lic_df, use_container_width=True)
lic_json = lic_edit.to_json()
# GI Tag
gi = st.selectbox("GI Product?", ["Yes", "No", "Unsure"])
gi_name = st.text_input("GI Product Name")
gi_reg = st.selectbox("GI Registered?", ["Yes", "No", "Applied"])
gi_use = st.selectbox("GI Used?", ["Yes", "No", "Partially"])
gi_premium = st.selectbox("Premium due to GI?", ["Yes", "No", "Not tracked"])
# Tax Table
tax_df = pd.DataFrame({
    "Tax": ["GST", "Income Tax", "Professional Tax", "Licence Fees"],
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
st.header("SECTION K – Governance Assessment")
# Board
board = st.number_input("Total Board Members", min_value=0)
meetings = st.number_input("Meetings in FY", min_value=0)
quorum = st.selectbox("Quorum", ["Always", "Mostly", "Rarely", "Never"])
mom = st.selectbox("Minutes recorded", ["All", "Most", "No"])
tracking = st.selectbox("Decision tracking", ["Formal", "Informal", "None"])

# AGM
agm = st.selectbox("AGM conducted?", ["Yes", "No"])
agm_date = st.text_input("AGM Date")
audit_present = st.selectbox("Audit presented?", ["Yes", "No", "Not audited"])
audit = st.selectbox("Audit done?", ["Yes", "No"])
audit_year = st.text_input("Audit FY")
# Members
members = st.number_input("Total members", min_value=0)
active = st.number_input("Active members", min_value=0)
# Partnership
partnership = st.selectbox("Partnership?", ["Yes", "No"])
partner_name = st.text_input("Partner Name")
offtake = st.selectbox("Offtake agreement?", ["Yes", "No", "Under Negotiation"])
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
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    c.execute("""
    INSERT INTO responses (
        enumerator_name, enumerator_phone,
        district, block, clf_name, survey_date,
        pre_support_business, pre_income_source, pre_revenue,
        reap_support, govt_support, fd_details,
        revenue_table, cost_table, section_h,
        staff_salary, latest_revenue, salary_sufficient, reap_stop, business_plan_exists,
        total_revenue, total_cost, sustainability
    )
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        enumerator_name, enumerator_phone,
        district, block, clf_name, str(survey_date),
        pre_business, pre_income_source, pre_revenue,
        reap_json, govt_json, fd_json,
        revenue_json, cost_json, section_h_json,
        staff_salary_latest, latest_revenue,
        salary_sufficient, reap_stop, business_plan_exists,
        revenue_total, cost_total, status
    ))

    conn.commit()

    conn.close()

    st.success("Survey Submitted Successfully!")
