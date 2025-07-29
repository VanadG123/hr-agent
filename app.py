import streamlit as st
import pandas as pd
from agent_setup import setup_agent_executor

st.title("📝 Agentic Offer Letter Generator")

# File Upload Section
st.header("📁 Upload Required Documents")

# PDF Uploaders
col1, col2 = st.columns(2)

with col1:
    hr_leave_policy = st.file_uploader(
        "1. HR Leave & Work from Home Policy (PDF)",
        type=['pdf'],
        help="Upload the company's leave and work from home policy document"
    )
    
    hr_travel_policy = st.file_uploader(
        "2. HR Travel Policy (PDF)", 
        type=['pdf'],
        help="Upload the company's travel policy document"
    )

with col2:
    sample_offer_letter = st.file_uploader(
        "3. Sample Offer Letter (PDF)",
        type=['pdf'],
        help="Upload a sample offer letter template"
    )
    
    employee_metadata = st.file_uploader(
        "4. Employee Metadata (CSV)",
        type=['csv'],
        help="Upload CSV file containing employee data (salary, team, joining date, etc.)"
    )

# Display uploaded files info
if any([hr_leave_policy, hr_travel_policy, sample_offer_letter, employee_metadata]):
    st.subheader("📋 Uploaded Files Status")
    
    files_status = {
        "HR Leave & Work from Home Policy": "✅ Uploaded" if hr_leave_policy else "❌ Not uploaded",
        "HR Travel Policy": "✅ Uploaded" if hr_travel_policy else "❌ Not uploaded", 
        "Sample Offer Letter": "✅ Uploaded" if sample_offer_letter else "❌ Not uploaded",
        "Employee Metadata": "✅ Uploaded" if employee_metadata else "❌ Not uploaded"
    }
    
    for file_name, status in files_status.items():
        st.write(f"**{file_name}:** {status}")

# Preview employee metadata if uploaded
if employee_metadata is not None:
    st.subheader("👥 Employee Metadata Preview")
    try:
        df = pd.read_csv(employee_metadata)
        st.dataframe(df.head(), use_container_width=True)
        st.write(f"**Total records:** {len(df)}")
    except Exception as e:
        st.error(f"Error reading CSV file: {e}")

# Candidate Information Section
st.header("👤 Candidate Information")
employee_name = st.text_input("Enter the full name of the candidate:")

# Generate Offer Letter Button
if st.button("🚀 Generate Offer Letter", type="primary"):
    if employee_name:
        # Check if all required files are uploaded
        required_files = [hr_leave_policy, hr_travel_policy, sample_offer_letter, employee_metadata]
        missing_files = [i+1 for i, file in enumerate(required_files) if file is None]
        
        if missing_files:
            st.error(f"❌ Please upload all required files. Missing: {', '.join(map(str, missing_files))}")
        else:
            with st.spinner("Generating... The agent is at work! 🧠"):
                try:
                    # Set up the agent executor with uploaded files
                    agent_executor = setup_agent_executor(
                        hr_leave_policy, 
                        hr_travel_policy, 
                        sample_offer_letter, 
                        employee_metadata
                    )
                    
                    # Generate the offer letter
                    response = agent_executor.invoke({
                        "input": f"Generate a complete offer letter for {employee_name} using the uploaded policies and metadata."
                    })
                    
                    st.markdown("### Generated Offer Letter")
                    st.markdown(response["output"])
                    
                except Exception as e:
                    st.error(f"Error generating offer letter: {str(e)}")
                    st.info("Please make sure you have set your COGCACHE_API_KEY in the .env file.")
    else:
        st.warning("Please enter a candidate's name.")