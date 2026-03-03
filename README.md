#  Bangtan FAQ AI: Beyond the Story
------------------------------------------
******************************************

An AI-powered contextual search engine designed to navigate the **BTS 10th Anniversary Memoir**. This tool transforms a static 400+ page PDF into an interactive, searchable knowledge base.

---

## --The "ENGENE" Logic
-----------------------------
This application moves beyond simple keyword matching by using a structured **NLP Pipeline**:

1.  **Preprocessing:** Cleans PDF "noise" and tokenizes text using **NLTK**.
2.  **Semantic Mapping:** Uses a custom synonym layer (in `config.py`) to ensure the AI knows "Bangtan" = "BTS".
3.  **Vectorization:** Transforms text into mathematical signatures using **TF-IDF**.
4.  **Similarity:** Calculates the **Cosine Similarity** to find the most relevant passage.
5.  **Context Window:** Returns the target answer along with surrounding lines to maintain narrative flow.



---

## --Project Structure
----------------------------
The project follows a modular architecture for professional-grade code management:

* **`app.py`**: The Streamlit web interface and session state manager.
* **`engene.py`**: The mathematical core (Vectorization & Similarity).
* **`processor.py`**: The data pipeline (PDF parsing & text cleaning).
* **`config.py`**: Global settings, synonym maps, and thresholds.
* **`requirements.txt`**: List of necessary Python libraries.

---

## --Installation & Setup
----------------------------

### 1. Install Dependencies
Ensure you have Python installed, then run:
```bash
pip install -r requirements.txt
2. Setup AI Resources
Download the necessary NLP models for tokenization and text cleaning:

Bash
python -c "import nltk; nltk.download('punkt_tab'); nltk.download('stopwords')"
3. Launch the UI
Start the web server to open the interface in your browser:

Bash
streamlit run app.py


--Tech Stack
---------------------
Language: Python 3.13

NLP: NLTK (Natural Language Toolkit)

Machine Learning: Scikit-learn (TF-IDF, Cosine Similarity)

UI Framework: Streamlit

PDF Engine: PyPDF2

--License & Credits
-----------------------
Developed as an AI Internship Project for CodeAlpha.

Author: NotSoArmyGemini/Twin

Topic: Beyond the Story: 10-Year Record of BTS Framework: Open-source AI Development for ARMY and BTS enthusiasts.
