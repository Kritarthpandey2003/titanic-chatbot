# Titanic Dataset Chat Agent 🚢

A friendly chatbot that analyzes the famous Titanic dataset, allowing users to ask questions in plain English and receive text answers along with visual insights.

## Architecture Stack
* **Backend**: Python with FastAPI
* **Agent Framework**: LangChain (Pandas DataFrame Agent) using Gemini (`gemini-1.5-pro`)
* **Frontend**: Streamlit

## Setup Instructions

1. **Install Prerequisites**:
   Ensure you have Python 3.9+ installed.

2. **Clone/Navigate to Project Folder**:
   Open a terminal in the `titanic-chatbot` directory.

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up the Dataset**:
   Run the following script to download `titanic.csv` into the `backend/` folder:
   ```bash
   python setup_data.py
   ```

5. **Set Environment Variable**:
   You must set your Gemini API key:
   - **Windows**: `set GEMINI_API_KEY=your_api_key_here` (or `$env:GEMINI_API_KEY="your_api_key_here"` in PowerShell)
   - **Mac/Linux**: `export GEMINI_API_KEY=your_api_key_here`

## Running the Application Locally

The easiest way to run everything is using the provided starter script. **Make sure you have put your Gemini API key in the `.env` file first.**

```bash
python run_all.py
```
This will start the API backend and automatically open the Streamlit UI in your browser.

---

## 🚀 How to get a Public URL for your Submission

The assignment requires you to "Share a working Streamlit URL". Since this project has two separate parts (a FastAPI backend and a Streamlit frontend), the fastest way to get a URL to submit is to run it on your laptop and generate a public link using **LocalTunnel** or **Ngrok**.

### Using LocalTunnel (Easiest)
1. Run `python run_all.py` to start the app.
2. Ensure you have Node.js installed on your computer.
3. Open a new terminal and run:
   ```bash
   npx localtunnel --port 8501
   ```
4. It will give you a public URL (e.g., `https://smooth-cat-42.loca.lt`). **This is the link you can submit for your assignment!** Note: Keep your laptop and the terminal running while they review it.

*(Alternatively, you can deploy the FastAPI backend to Render.com and the Streamlit frontend to Streamlit Community Cloud, but that takes much longer to set up).*

## Example Queries
Try asking the bot:
- *"What percentage of passengers were male on the Titanic?"*
- *"Show me a histogram of passenger ages"*
- *"What was the average ticket fare?"*
- *"How many passengers embarked from each port?"*
