# 🧠 Smart Stock Advisor


A Python-powered multi-engine stock market search system combining LLMs, vector databases, and real-time search APIs — all within an interactive notebook and Gradio UI.

![Gradio Screenshot](gradio-sample.png)

## 🔍 What This Project Does

This project demonstrates **four distinct search strategies** for stock market-related queries:

1. **Generic Search API**  
   A flexible web search engine with customizable parameters for general stock market news or topics.

2. **DuckDuckGo Search**  
   A privacy-respecting real-time search engine for retrieving the latest news and information.

3. **Traversaal Search**  
   A specialized search interface tailored for financial and stock-related metadata retrieval.

4. **Qdrant Local Semantic Search**  
   Embedding-based vector search using Qdrant to perform fast, intelligent queries on local stock data.

> Combine traditional keyword search with **LLM-powered reasoning** and **vector similarity search** to surface more relevant stock market insights.

---

## 🚀 Installation

Clone this repository and install dependencies:

```bash
git clone https://github.com/yourusername/stock-search-demo.git
cd stock-search-demo
pip install -r requirements.txt
```

### 📦 Environment Setup

Create a `.env` file at the project root (already included) and set your required keys:

```
TRAVERSAAL_API_KEY=your_key_here
OTHER_API_KEYS=as_needed
```

---

## 💡 How to Use

### 🧪 Jupyter Notebook Mode

Run the interactive search demo via the notebook:

```bash
jupyter notebook notebooks/005-stock_search.ipynb
```

Explore results from all four engines side by side.

### 🌐 Gradio Web Interface (Optional)

If the Gradio UI is set up, you can launch it like this:

```bash
python src/app.py
```

> The UI enables easy comparison of responses from the search engines.

---

## 📁 Project Structure

```
├── notebooks/
│   └── 005-stock_search.ipynb      # Main demo notebook
├── data/
│   └── *.csv                       # Sample stock data
├── src/
│   └── search_engines/            # Engine implementations
├── storage/
│   └── embeddings, qdrant_vdb/    # Semantic search assets
├── gradio-sample.png              # UI Screenshot
├── .env                           # API credentials (excluded from GitHub)
├── requirements.txt               # Dependencies
└── README.md
```

---

## 🧩 Dependencies

Key packages used:

- `sentence-transformers`
- `qdrant-client`
- `duckduckgo-search`
- `gradio`
- `pandas`, `requests`, `python-dotenv`, `pydantic`

Install all with:

```bash
pip install -r requirements.txt
```

---

## 🤝 Contributing

Contributions, improvements, and bug reports are welcome! Please fork the repo and submit a pull request.

---

## 📜 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for more details.

---

## 👨‍💻 Author

**Bhuvanesh Gopalarathnam**  
**Kiran Ramanna**  
Feel free to reach out via bhuv666@gmail.com or [LinkedIn - Bhuvanesh](https://www.linkedin.com/in/bhuvanesh) | [LinkedIn - Kiran](https://www.linkedin.com/in/kiran)
