 Bangtan FAQ AI: Beyond the Story
----------------------------------------
----------------------------------------

 *An Intelligent Contextual Search Engine for the BTS 10th Anniversary Memoir*
--------------------------------------------------------------------------------------------

![BTS Logo](https://img.shields.io/badge/BTS-Borahae-purple) ![Python](https://img.shields.io/badge/Python-3.13-blue) ![Groq](https://img.shields.io/badge/Inference-Groq_LPU-orange)

**Bangtan FAQ AI** iAn AI-powered contextual search engine designed to navigate the BTS 10th Anniversary Memoir. This tool transforms a static 400+ page PDF into an interactive, searchable knowledge base.

---

---The "ENGENE" Pipeline
---------------------------
This application uses a custom-built **NLP & Inference Pipeline** to ensure accuracy and speed:

* **Semantic Preprocessing:** Cleans OCR noise and tokenizes text via **NLTK**, handling multi-column layouts from the original PDF.
* **Vectorized Retrieval:** Maps user queries into a high-dimensional space using **TF-IDF Vectorization** to find the exact page and paragraph.
* **Contextual Smoothing:** Employs **Cosine Similarity** to retrieve not just a keyword, but the surrounding "Context Window" for a narrative-rich response.
* **LPU-Powered Inference:** Passes the retrieved context to **Llama 3.3 (via Groq)**. Using Groq’s LPU (Language Processing Unit) allows for near-instant response times.
* **Strict Prompt Engineering:** A specialized System Prompt prevents hallucinations, ensuring the AI only reports facts found in the memoir.

---

---Key Features
--------------------------

* **Verified Discography:** Specialized handling for multi-CD albums (e.g., *Proof*, *MOTS 7*) with vertical list formatting.
* **Borahae UI:** A custom-styled **Streamlit** interface featuring signature purple aesthetics and ARMY/BTS avatars.
* **Intelligent Synonyms:** A custom mapping layer in `config.py` that understands BTS-specific terminology (e.g., "Bangtan", "Hwayangyeonhwa").
* **High-Speed Search:** Sub-second retrieval and generation powered by the **Groq API**.

---

---Project Structure
-------------------------

```text
├── app.py              # Streamlit interface & chat session management
├── engene.py           # Mathematical core (Retrieval & Prompt Logic)
├── processor.py        # Data pipeline (PDF parsing & OCR management)
├── config.py           # Global settings, synonym maps, & thresholds
├── assets/             # Branding assets (army.png, bts.png)
└── requirements.txt    # Project dependencies
```
---
---Installation & Setup
-------------------------

**1. Clone & Install**
```Bash
  git clone https://github.com/yourusername/bangtan-faq-ai.git
  cd bangtan-faq-ai
  pip install -r requirements.txt
``` 

**2. Initialize NLP Models**
```python
    import nltk
    # Download necessary resources for the ENGENE pipeline
    nltk.download(['punkt_tab', 'stopwords'])
```

**3. Configure API Key**
   Create a .env file in the root directory and add your Groq API Key:
```Plaintext
GROQ_API_KEY=your_key_here
```

**4. Launch the App**
```Bash
   streamlit run app.py
```

---Tech Stack
---------------------
```text
Language: Python 3.13

Inference Engine: Groq Cloud (Llama 3.3 70B)

NLP & ML: NLTK, Scikit-learn (TF-IDF, Cosine Similarity)

UI Framework: Streamlit

Data Engine: PyMuPDF / PyPDF2
```

---License & Credits
-----------------------
```text
Developed as an AI Internship Project for CodeAlpha.

Author: Doha EL IDRISSI

Topic: Beyond the Story: 10-Year Record of BTS Framework: Open-source AI Development
```
