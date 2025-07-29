# 🤖 HR Agent - AI-Powered Offer Letter Generator

An intelligent HR application that generates professional offer letters using AI agents and company policy documents.

## 🚀 Features

- **📄 Document Processing**: Upload and process HR policies (PDF format)
- **🤖 AI-Powered Generation**: Uses CogCache and OpenAI models for intelligent offer letter creation
- **📊 Employee Data Integration**: CSV upload for employee metadata
- **🔍 Vector Search**: Semantic search through policy documents using sentence transformers
- **🎨 Modern UI**: Beautiful Streamlit interface with real-time feedback

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **AI/ML**: LangChain, OpenAI (via CogCache)
- **Vector Database**: ChromaDB
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
- **Document Processing**: PyPDF, Pandas

## 📋 Prerequisites

- Python 3.8+
- CogCache API key
- Required PDF documents (HR policies, sample offer letter)
- Employee metadata CSV file

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/VanadG123/hr-agent.git
   cd hr-agent
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   COGCACHE_API_KEY=your_cogcache_api_key_here
   COGCACHE_LLM_MODEL=gpt-4o-2024-08-06
   OPENAI_API_BASE=https://proxy-api.cogcache.com/v1/
   
   # Vector Store Configuration
   CHROMA_PERSIST_DIRECTORY=./chroma_db
   
   # Model Configuration
   EMBEDDING_MODEL=all-MiniLM-L6-v2
   TEMPERATURE=0.7
   ```

## 🎯 Usage

1. **Run the application**
   ```bash
   streamlit run app.py
   ```

2. **Upload required documents**
   - HR Leave & Work from Home Policy (PDF)
   - HR Travel Policy (PDF)
   - Sample Offer Letter (PDF)
   - Employee Metadata (CSV)

3. **Generate offer letter**
   - Enter candidate name
   - Click "Generate Offer Letter"
   - Review and download the generated letter

## 📁 Project Structure

```
hr-agent/
├── app.py                 # Main Streamlit application
├── agent_setup.py         # AI agent configuration and CogCache integration
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (not in repo)
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## 🔧 Configuration

### Supported Models
- **OpenAI GPT-4o**: `gpt-4o-2024-08-06`
- **OpenAI GPT-4o mini**: `gpt-4o-mini-2024-07-18`
- **Meta Llama models**: Various Llama 3.x variants

### Environment Variables
- `COGCACHE_API_KEY`: Your CogCache API key
- `COGCACHE_LLM_MODEL`: Model to use for generation
- `OPENAI_API_BASE`: CogCache proxy URL
- `TEMPERATURE`: AI model creativity (0.0-1.0)
- `EMBEDDING_MODEL`: Sentence transformer model for embeddings

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [CogCache](https://cogcache.com/) for AI model optimization
- [Streamlit](https://streamlit.io/) for the web interface
- [LangChain](https://langchain.com/) for AI agent framework
- [ChromaDB](https://www.trychroma.com/) for vector storage

## 📞 Support

For support, please open an issue on GitHub or contact the maintainers.

---

**Made with ❤️ for HR professionals**
