import streamlit as st
import json
from pathlib import Path
from saved_resources_store import list_resources, save_resource

st.set_page_config(page_title="Saved Resources", page_icon="💾", layout="wide")

st.title("💾 Saved Resources")

# Load all saved resources
resources = list_resources()

if not resources:
    st.info("No resources saved yet. Go to Learning Hub and click 'Save Resource' to add items here.")
else:
    st.success(f"You have {len(resources)} saved resource(s).")
    
    # Display resources in a table-like format
    st.subheader("Your Saved Resources")
    
    for idx, resource in enumerate(resources):
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.markdown(f"### {resource.get('title', 'Untitled')}")
            st.caption(f"Saved: {resource.get('saved_at', 'N/A')} | ID: {resource.get('id')}")
            if resource.get('source'):
                st.caption(f"Source: {resource.get('source')}")
        
        with col2:
            if st.button("View", key=f"view_{idx}"):
                st.json(resource)
        
        with col3:
            if st.button("Delete", key=f"delete_{idx}"):
                # Remove from session state if present
                if "saved_resources" in st.session_state:
                    st.session_state.saved_resources = [
                        r for r in st.session_state.saved_resources 
                        if r.get('id') != resource.get('id')
                    ]
                st.success("Deleted from session. (Note: file persistence requires reload)")
        
        st.divider()

# Export / Download
st.subheader("Export Your Resources")
if resources:
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Export as JSON"):
            json_str = json.dumps(resources, ensure_ascii=False, indent=2)
            st.download_button(
                label="Download JSON",
                data=json_str,
                file_name="saved_resources.json",
                mime="application/json"
            )
    
    with col2:
        if st.button("Export as CSV"):
            import pandas as pd
            df = pd.DataFrame([
                {
                    'Title': r.get('title', 'N/A'),
                    'Source': r.get('source', 'N/A'),
                    'Saved At': r.get('saved_at', 'N/A'),
                    'ID': r.get('id', 'N/A')
                }
                for r in resources
            ])
            csv_str = df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv_str,
                file_name="saved_resources.csv",
                mime="text/csv"
            )

# Quick add resource (for testing)
st.subheader("Quick Add Resource (Testing)")
with st.form("quick_add_form"):
    title_input = st.text_input("Resource Title")
    source_input = st.selectbox("Source", ["Manual", "Learning Hub", "AI Advisor", "Other"])
    if st.form_submit_button("Add Resource"):
        if title_input.strip():
            new_res = save_resource({
                'title': title_input,
                'source': source_input
            })
            st.success(f"Added resource '{title_input}' (ID: {new_res.get('id')})")
            st.rerun()
        else:
            st.error("Please enter a resource title.")
