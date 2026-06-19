# 🎓 Smart StudyMate AI

An AI-based student assistant that helps in studying efficiently by summarizing notes, extracting key topics, generating quiz questions, and converting summaries into speech.

## 🚀 Features

- **📝 Smart Summarization**: Automatically summarizes large notes or PDF files into concise, digestible content
- **🔑 Keyword Extraction**: Intelligently extracts important keywords and topics from your study materials
- **❓ Quiz Generation**: Generates short quiz questions for effective revision and knowledge testing
- **🔊 Text-to-Speech**: Converts summaries into audio format for auditory learning
- **🎨 Interactive UI**: Clean, user-friendly web interface built with Gradio

## 🧩 Tech Stack

- **Language**: Python
- **NLP Model**: Transformers (BART Model for summarization)
- **UI Framework**: Gradio
- **NLP Library**: NLTK for text processing
- **Audio**: gTTS (Google Text-to-Speech) for speech synthesis

## 📋 Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

## 🔧 Installation

1. **Clone the repository**:
```bash
git clone https://github.com/0harshitsingh1/Smart-StudyMate-AI.git
cd Smart-StudyMate-AI
```

2. **Create a virtual environment** (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

## 💻 Usage

### Running the Application

```bash
python app.py
```

The application will launch a Gradio web interface in your browser.

### Using the Features

1. **Summarize**: Paste your notes or upload a file to get an AI-generated summary
2. **Extract Keywords**: Get the most important keywords from your text
3. **Generate Quiz**: Create practice quiz questions based on your study material
4. **Convert to Speech**: Listen to the summaries with automatic text-to-speech

## 📁 Project Structure

```
Smart-StudyMate-AI/
├── README.md
├── requirements.txt
├── app.py
├── src/
│   ├── summarizer.py
│   ├── keyword_extractor.py
│   ├── quiz_generator.py
│   └── text_to_speech.py
└── examples/
    └── sample_notes.txt
```

## 📦 Dependencies

See `requirements.txt` for the complete list of dependencies. Key packages include:
- `transformers` - For BART model
- `gradio` - For web UI
- `nltk` - For NLP tasks
- `gtts` - For text-to-speech

## 🎯 How It Works

1. **Input**: Accepts text or file input from users
2. **Processing**: Uses advanced NLP models to analyze and process the content
3. **Output**: Generates summaries, extracts keywords, creates quizzes, and produces audio

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**Harshit Singh** - [@0harshitsingh1](https://github.com/0harshitsingh1)

## 🆘 Support

If you encounter any issues or have questions:
- Open an [issue on GitHub](https://github.com/0harshitsingh1/Smart-StudyMate-AI/issues)
- Contact the project maintainer

## 🙏 Acknowledgments

- Thanks to all contributors who have helped improve this project
- Inspired by the need to make studying more efficient and effective for students
- Built with open-source AI and NLP tools

---

**Happy Studying! 📚✨**
