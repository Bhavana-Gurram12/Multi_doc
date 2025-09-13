import streamlit as st
import json
import os
from datetime import datetime
from src.main_processor import MainProcessor

st.set_page_config(page_title="Document Parser", page_icon="📄", layout="wide")

# Clean, modern CSS
st.markdown("""
<style>
    .stApp { background: #ffffff; }
    .main { padding: 1rem; }
    
    /* Hide Streamlit branding */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
    
    /* Remove top padding */
    .block-container { padding-top: 1rem; }
    
    .header {
        background: linear-gradient(90deg, #4f46e5, #7c3aed);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    
    .card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    .metrics {
        display: flex;
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .metric {
        flex: 1;
        background: #f8fafc;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        border: 1px solid #e2e8f0;
    }
    
    .metric-value {
        font-size: 1.5rem;
        font-weight: bold;
        color: #1e293b;
    }
    
    .metric-label {
        font-size: 0.8rem;
        color: #64748b;
        margin-top: 0.25rem;
    }
    
    .result-item {
        background: #f9fafb;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .result-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
    }
    
    .badge {
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    .badge-green { background: #dcfce7; color: #166534; }
    .badge-yellow { background: #fef3c7; color: #92400e; }
    
    .stButton > button {
        background: linear-gradient(90deg, #4f46e5, #7c3aed);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        width: 100%;
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #3730a3, #6b21a8);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'processed_docs' not in st.session_state:
    st.session_state.processed_docs = []
if 'processing_logs' not in st.session_state:
    st.session_state.processing_logs = []

# Header
st.markdown("""
<div class="header">
    <h1 style="margin: 0; font-size: 2rem;">📄 Document Parser</h1>
    <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Upload documents and extract structured data with AI</p>
</div>
""", unsafe_allow_html=True)

# Main layout
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### Upload Files")
    
    uploaded_files = st.file_uploader(
        "Choose files",
        accept_multiple_files=True,
        type=['pdf', 'docx', 'html', 'txt']
    )
    
    sender_name = st.text_input("Sender (optional)")
    gemini_api_key = st.text_input("Gemini API Key (optional)", type="password")
    
    if st.button("Process Documents", disabled=not uploaded_files):
        processor = MainProcessor(gemini_api_key if gemini_api_key else None)
        
        progress = st.progress(0)
        
        for i, file in enumerate(uploaded_files):
            with st.spinner(f"Processing {file.name}..."):
                temp_path = f"data/{file.name}"
                os.makedirs("data", exist_ok=True)
                
                with open(temp_path, "wb") as f:
                    f.write(file.getbuffer())
                
                try:
                    document, log = processor.process_document(temp_path, sender_name or None)
                    st.session_state.processed_docs.append(document)
                    st.session_state.processing_logs.append(log)
                    os.remove(temp_path)
                except Exception as e:
                    st.error(f"Error: {e}")
                
                progress.progress((i + 1) / len(uploaded_files))
        
        processor.save_signatures()
        st.success("Processing complete!")
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Statistics
    if st.session_state.processed_docs:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Statistics")
        
        total = len(st.session_state.processed_docs)
        cost = sum(log.cost_estimate for log in st.session_state.processing_logs)
        ai_used = sum(1 for log in st.session_state.processing_logs if log.ai_usage)
        
        st.markdown(f"""
        <div class="metrics">
            <div class="metric">
                <div class="metric-value">{total}</div>
                <div class="metric-label">Documents</div>
            </div>
            <div class="metric">
                <div class="metric-value">${cost:.3f}</div>
                <div class="metric-label">Cost</div>
            </div>
            <div class="metric">
                <div class="metric-value">{ai_used}</div>
                <div class="metric-label">AI Used</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Clear All"):
            st.session_state.processed_docs = []
            st.session_state.processing_logs = []
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### Results")
    
    if st.session_state.processed_docs:
        for i, (doc, log) in enumerate(zip(st.session_state.processed_docs, st.session_state.processing_logs)):
            badge_class = "badge-green" if doc.processing_method == "rule_based" else "badge-yellow"
            
            st.markdown(f"""
            <div class="result-item">
                <div class="result-header">
                    <strong>{doc.title or f'Document {i+1}'}</strong>
                    <span class="badge {badge_class}">{doc.processing_method.replace('_', ' ').title()}</span>
                </div>
                <div style="font-size: 0.9rem; color: #64748b;">
                    Confidence: {doc.confidence_score:.2f} | Time: {log.processing_time:.1f}s | Cost: ${log.cost_estimate:.4f}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander("View Details"):
                # JSON output
                json_data = doc.model_dump(mode='json')
                if hasattr(json_data['processed_at'], 'isoformat'):
                    json_data['processed_at'] = json_data['processed_at'].isoformat()
                
                st.json(json_data)
                
                # Download
                json_str = json.dumps(json_data, indent=2)
                st.download_button(
                    "Download JSON",
                    json_str,
                    f"{doc.document_id}.json",
                    "application/json",
                    key=f"download_{i}"
                )
    else:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; color: #64748b;">
            <h4>No documents processed yet</h4>
            <p>Upload files to get started</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)