# PragatiPath AI

PragatiPath AI is an innovative video platform that leverages real-time hand gesture recognition to enhance educational engagement. Using OpenCV and MediaPipe, it interprets hand gestures for interactive content illustration, including drawing, erasing, and changing colors.

## 🎥 Demonstration

Watch the demonstration video below to see hand actions for drawing, erasing, and changing colors in action.

https://github.com/VSMourya/PragitiPath_AI/assets/30852815/9d29d43b-aba1-40de-a258-58ee663c950c

## 🚀 Introduction

PragatiPath AI uses advanced machine learning algorithms to process video input, identifying specific hand markers and actions. This project is designed to revolutionize educational technology by making learning more interactive and engaging. Integrated Google Cloud Platform speech-to-text feature with automatic summarization, enabling the platform to transcribe teacher’s lectures and generate concise bullet-point notes, further facilitating an interactive and efficient learning environment.

## 💻 System Requirements

- Python 3.11
- Docker (optional for containerization)
- Node.js (for the ReactJS frontend)

## 🛠 Installation Steps

1. **Clone the repository**
   ```
   git clone https://github.com/VSMourya/PragitiPath_AI.git
   ```
2. **Set up the virtual environment**
   - Create: `python3 -m venv virtual_env`
   - Activate:
     - Windows: `.\virtual_env\Scripts\activate`
     - Linux/MacOS: `source virtual_env/bin/activate`
3. **Install Node Version Manager (nvm)**
   ```
   curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
   source ~/.bash_profile
   ```
4. **Install Node.js**
   ```
   nvm install node
   nvm install 16
   ```
5. **Install Python dependencies**
   ```
   pip install -r requirements.txt
   ```

## 🚀 Running the Project

1. **Server setup**
   - Navigate to `server` directory: `cd server`
   - Start the Flask server: `python3 run.py`
2. **Client setup**
   - Open a new terminal
   - Navigate to `client` directory: `cd client && npm start`

## 📂 File Descriptions

- `detectActions.py`: Logic for detecting hand actions.
- `draw_vid.py`: Drawing output on the video feed.
- `run.py`: Main script to run the project.
- `Dockerfile`: Commands to assemble a Docker image.

## 🐳 Docker Setup (Optional)

To containerize PragatiPath AI with Docker:

1. **Build the Docker image**
   ```
   docker build -t PragatiPath_AI .
   ```
2. **Run the Docker container**
   ```
   docker run -it --name PragatiPath_AI PragatiPath_AI
   ```

## 📚 Additional Information

The project uses a specific hand marker system for tracking, detailed in `hand_marks.png`. Each marker corresponds to a specific hand point tracked by the AI.

---

PragatiPath AI is committed to enhancing educational experiences through technology. For contributions, issues, or further inquiries, please reach out through GitHub issues or pull requests.
