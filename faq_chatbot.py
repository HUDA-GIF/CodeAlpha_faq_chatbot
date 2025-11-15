import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import csv
import io

# Page configuration
st.set_page_config(
    page_title="Universal FAQ Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Title and description
st.title("🌐 Universal FAQ Chatbot")
st.markdown("""
**Enter any topic and its FAQs, then chat with your personalized AI assistant!**

1. **Add your FAQs** in the sidebar
2. **Chat** with the bot about your topic
3. **Export/Import** your FAQ data
""")

# Initialize session state for FAQs
if 'faqs' not in st.session_state:
    st.session_state.faqs = {'questions': [], 'answers': []}

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Sidebar - FAQ Management
with st.sidebar:
    st.header("📝 Manage FAQs")
    
    # Add individual Q&A
    st.subheader("Add Question & Answer")
    
    with st.form("add_faq_form"):
        question = st.text_input("Question:")
        answer = st.text_area("Answer:")
        submitted = st.form_submit_button("Add FAQ")
        
        if submitted and question and answer:
            st.session_state.faqs['questions'].append(question)
            st.session_state.faqs['answers'].append(answer)
            st.success("FAQ added successfully!")
    
    # Bulk upload from CSV
    st.subheader("📤 Bulk Upload (CSV)")
    uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])
    
    if uploaded_file is not None:
        try:
            # Read CSV
            df = pd.read_csv(uploaded_file)
            if 'question' in df.columns and 'answer' in df.columns:
                new_questions = df['question'].tolist()
                new_answers = df['answer'].tolist()
                
                st.session_state.faqs['questions'].extend(new_questions)
                st.session_state.faqs['answers'].extend(new_answers)
                st.success(f"Added {len(new_questions)} FAQs from CSV!")
            else:
                st.error("CSV must contain 'question' and 'answer' columns")
        except Exception as e:
            st.error(f"Error reading CSV: {e}")
    
    # Manual text input for bulk FAQs
    st.subheader("📝 Quick Bulk Add")
    bulk_text = st.text_area("Enter FAQs (Format: Question?|Answer)", 
                           height=150,
                           placeholder="What is AI?|Artificial Intelligence is...\nHow does ML work?|Machine Learning works by...")
    
    if st.button("Parse Bulk FAQs") and bulk_text:
        lines = bulk_text.strip().split('\n')
        added_count = 0
        
        for line in lines:
            if '|' in line:
                q, a = line.split('|', 1)
                if q.strip() and a.strip():
                    st.session_state.faqs['questions'].append(q.strip())
                    st.session_state.faqs['answers'].append(a.strip())
                    added_count += 1
        
        if added_count > 0:
            st.success(f"Added {added_count} FAQs!")
        else:
            st.warning("No valid FAQs found. Use format: Question?|Answer")
    
    # FAQ Statistics
    st.subheader("📊 FAQ Statistics")
    st.write(f"Total FAQs: **{len(st.session_state.faqs['questions'])}**")
    
    if st.session_state.faqs['questions']:
        st.write("Sample questions:")
        for i, q in enumerate(st.session_state.faqs['questions'][:3]):
            st.write(f"• {q}")
    
    # Export FAQs
    if st.session_state.faqs['questions']:
        st.subheader("💾 Export FAQs")
        
        # CSV Export
        csv_data = pd.DataFrame({
            'question': st.session_state.faqs['questions'],
            'answer': st.session_state.faqs['answers']
        }).to_csv(index=False)
        
        st.download_button(
            label="Download as CSV",
            data=csv_data,
            file_name="my_faqs.csv",
            mime="text/csv"
        )
        
        # JSON Export
        json_data = json.dumps(st.session_state.faqs, indent=2)
        st.download_button(
            label="Download as JSON",
            data=json_data,
            file_name="my_faqs.json",
            mime="application/json"
        )
    
    # Clear all FAQs
    if st.button("🗑️ Clear All FAQs", type="secondary"):
        st.session_state.faqs = {'questions': [], 'answers': []}
        st.session_state.chat_history = []
        st.rerun()

# Main Chat Area
col1, col2 = st.columns([2, 1])

with col1:
    st.header("💬 Chat with Your FAQ Bot")
    
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "confidence" in message:
                st.caption(f"Confidence: {message['confidence']:.2f}")

# FAQ Processing and Matching Functions
@st.cache_resource
def initialize_similarity(questions):
    """Initialize TF-IDF vectorizer with current FAQs"""
    if not questions:
        return None, None
    
    vectorizer = TfidfVectorizer(stop_words='english', lowercase=True)
    tfidf_matrix = vectorizer.fit_transform(questions)
    return vectorizer, tfidf_matrix

def find_best_match(user_question, questions, answers):
    """Find the best matching FAQ using cosine similarity"""
    if not questions:
        return "I don't have any FAQs yet. Please add some questions and answers in the sidebar!", 0.0
    
    vectorizer, tfidf_matrix = initialize_similarity(questions)
    
    # Transform user question
    user_vector = vectorizer.transform([user_question.lower()])
    
    # Calculate similarities
    similarities = cosine_similarity(user_vector, tfidf_matrix).flatten()
    
    # Find best match
    best_match_idx = np.argmax(similarities)
    best_score = similarities[best_match_idx]
    
    if best_score > 0.3:  # Confidence threshold
        return answers[best_match_idx], best_score
    else:
        return "I'm not sure about that. Could you rephrase your question or add this FAQ to my knowledge base?", best_score

with col1:
    # Chat input
    if prompt := st.chat_input("Ask a question about your FAQs..."):
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get bot response
        with st.chat_message("assistant"):
            with st.spinner("Searching FAQs..."):
                answer, confidence = find_best_match(
                    prompt, 
                    st.session_state.faqs['questions'], 
                    st.session_state.faqs['answers']
                )
                
                if confidence > 0.3:
                    response = f"{answer}\n\n*Match confidence: {confidence:.2f}*"
                else:
                    response = answer
                
                st.markdown(response)
                st.session_state.chat_history.append({
                    "role": "assistant", 
                    "content": response,
                    "confidence": confidence
                })

with col2:
    st.header("🔍 FAQ Knowledge Base")
    
    if not st.session_state.faqs['questions']:
        st.info("""
        **No FAQs yet!** 
        
        Get started by:
        1. Adding Q&A pairs in the sidebar
        2. Uploading a CSV file
        3. Using bulk text input
        """)
    else:
        # Display FAQs in an expandable format
        for i, (question, answer) in enumerate(zip(st.session_state.faqs['questions'], st.session_state.faqs['answers'])):
            with st.expander(f"Q: {question}"):
                st.write(f"**A:** {answer}")
                
                # Quick action buttons for each FAQ
                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button("🗑️", key=f"delete_{i}"):
                        st.session_state.faqs['questions'].pop(i)
                        st.session_state.faqs['answers'].pop(i)
                        st.rerun()
                
                with col_b:
                    if st.button("💬", key=f"chat_{i}"):
                        st.session_state.chat_history.append({"role": "user", "content": question})
                        st.rerun()

# Quick Setup Templates
with st.sidebar:
    st.header("🚀 Quick Templates")
    
    template_option = st.selectbox(
        "Load example template:",
        ["None", "Tech Support", "Product FAQs", "Company Policies", "Educational Content"]
    )
    
    if st.button("Load Template") and template_option != "None":
        templates = {
            "Tech Support": [
                ("How do I reset my password?", "Go to Settings > Account > Reset Password and follow the instructions."),
                ("The app is crashing, what should I do?", "Try clearing cache or reinstalling the application."),
                ("How to contact support?", "Email support@company.com or call 1-800-HELP."),
            ],
            "Product FAQs": [
                ("What are the main features?", "Our product offers feature A, B, and C with advanced customization."),
                ("Is there a free trial?", "Yes, we offer a 30-day free trial with full features."),
                ("What platforms are supported?", "Available on Windows, Mac, iOS, and Android."),
            ],
            "Company Policies": [
                ("What is the refund policy?", "We offer 30-day money-back guarantee for all purchases."),
                ("What are your working hours?", "Our team is available Monday-Friday, 9 AM - 6 PM EST."),
                ("Do you offer discounts for students?", "Yes, we provide 50% discount for verified students."),
            ],
            "Educational Content": [
                ("What is photosynthesis?", "Photosynthesis is the process plants use to convert light energy into chemical energy."),
                ("How does gravity work?", "Gravity is a force that attracts objects with mass toward each other."),
                ("What is the capital of France?", "The capital of France is Paris."),
            ]
        }
        
        for question, answer in templates[template_option]:
            st.session_state.faqs['questions'].append(question)
            st.session_state.faqs['answers'].append(answer)
        
        st.success(f"Loaded {len(templates[template_option])} FAQs from {template_option} template!")

# Footer
st.markdown("---")
st.caption("💡 **Tip**: Add at least 5-10 diverse Q&A pairs for better matching accuracy!")