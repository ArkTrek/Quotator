# Quotator 🖋️

Quotator is a premium, mobile-friendly Flask application designed for discovering, sharing, and discussing world-famous quotes. Featuring a unique "Ink Pen on Parchment" aesthetic, it combines modern functionality with a classic, hand-drawn feel.

![Quotator Sample](<img width="1899" height="860" alt="Screenshot 2026-05-02 215912" src="https://github.com/user-attachments/assets/36e026d4-1ccc-4472-af6c-c87682bee421" />
)

## ✨ Features

- **Ink-Pen Aesthetic**: A beautiful UI featuring parchment textures, elegant typography (Caveat & Playfair Display), and realistic post-it note quote cards.
- **AI-Powered Safety**: Utilizes a local LLM (Ollama) to perform real-time safety checks on all user-submitted quotes and comments.
- **Interactive System**: Like and comment on your favorite quotes.
- **Guest Access**: Seamlessly browse and interact even without a formal account.
- **Mobile Optimized**: Fully responsive design with cascading transitions and custom mobile UI refinements.
- **Premium Animations**: Features a custom "scribbling" preloader and smooth staggered page entrance effects.

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- [Ollama](https://ollama.com/) (with `qwen2.5-coder:1.5b` model installed)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/arktrek/Quotator.git
   cd Quotator
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Ensure Ollama is running and pull the model:
   ```bash
   ollama pull qwen2.5-coder:1.5b
   ```

4. Run the application:
   ```bash
   python app.py
   ```

5. Access the app at `http://localhost:5000` (or your local IP for mobile access).

## 🛠️ Built With

- **Backend**: Flask (Python)
- **Database**: TOON Data Manager (`python-toon`)
- **AI**: Ollama API (`qwen2.5-coder:1.5b`)
- **Frontend**: HTML5, Vanilla CSS3, JavaScript
- **Icons**: Phosphor Icons

## 👤 Author

**ARPIT RAMESAN**
- GitHub: [@arktrek](https://github.com/arktrek)
- Portfolio: [Arpit Ramesan](https://arpitramesansportfolio.pythonanywhere.com/)
- Email: arpitramesan777@gmail.com

---
*Preserving the world's wisdom in ink.*
