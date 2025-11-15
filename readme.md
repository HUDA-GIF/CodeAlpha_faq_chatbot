🤖 FAQ Chatbot
A smart, flexible chatbot that can handle FAQs for any topic! Simply add your questions and answers, and the chatbot will intelligently match user queries with the most relevant responses using advanced NLP techniques.

✨ Features
🌐 Any Topic Support - Perfect for tech support, product FAQs, educational content, company policies, or any other subject

📝 Multiple Input Methods - Add FAQs via form, CSV upload, bulk text, or templates

🔍 Smart Matching - Uses TF-IDF and cosine similarity for accurate question matching

💬 Real-time Chat - Clean, intuitive chat interface with confidence scoring

📊 Export/Import - Save your FAQ data as CSV or JSON for backup and sharing

🚀 Quick Templates - Get started instantly with pre-built templates

📱 Responsive Design - Works perfectly on desktop and mobile devices

🚀 Quick Start
Prerequisites
Python 3.8 or higher

pip (Python package manager)

Installation
Clone or download the project

bash
# If using git
git clone <your-repository-url>
cd CodeAlpha_FAQChatbot

# Or simply download faq_chatbot.py and requirements.txt
Install dependencies

bash
pip install -r requirements.txt
Run the application

bash
streamlit run faq_chatbot.py
Open your browser to http://localhost:8501

🎯 How to Use
Getting Started
Add Your FAQs using any method in the sidebar:

Single Q&A: Use the form to add questions one by one

Bulk Upload: Paste questions and answers in "Question|Answer" format

CSV Upload: Upload a CSV file with 'question' and 'answer' columns

Templates: Load pre-built templates for quick testing

Start Chatting in the main chat interface

Manage Your Data using export features to save your work

Sample Questions to Try
"How do I reset my password?"

"What features do you offer?"

"How much does it cost?"

"Is there a free trial?"

📁 Project Structure
text
CodeAlpha_FAQChatbot/
│
├── faq_chatbot.py          # Main application file
├── requirements.txt         # Dependencies list
├── README.md               # This file
└── my_faqs.csv            # Your exported FAQ data (optional)
🛠️ Technical Details
Built With
Streamlit - Web application framework

scikit-learn - Machine learning and NLP processing

pandas - Data manipulation and CSV handling

numpy - Mathematical operations

NLTK - Natural language processing utilities

AI/ML Features
TF-IDF Vectorization - Converts text to numerical representations

Cosine Similarity - Measures similarity between questions

Confidence Scoring - Shows match accuracy for each response

Smart Preprocessing - Text cleaning and normalization

📊 Supported File Formats
CSV Format
JSON Format

🔧 Customization
Adding New Templates
Edit the templates dictionary in the code to add your own quick-start templates:

python
templates = {
    "Your Template": [
        ("Question 1?", "Answer 1"),
        ("Question 2?", "Answer 2"),
    ]
}
Modifying Confidence Threshold
Change the similarity threshold in the find_best_match function:

python
if best_score > 0.3:  # Adjust this value
    return answers[best_match_idx], best_score
🤝 Contributing
We welcome contributions! Feel free to:

Report bugs and issues

Suggest new features

Submit pull requests

Improve documentation

📝 License
This project is part of the CodeAlpha AI Internship Program. Feel free to use and modify for educational purposes.


# CodeAlpha_faq_chatbot
