import os
import base64
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_google_genai import ChatGoogleGenerativeAI
import matplotlib
matplotlib.use('Agg') # Ensure plots are saved to file, not displayed
import matplotlib.pyplot as plt
from dotenv import load_dotenv

# Load environment variables (like GEMINI_API_KEY) from .env file
load_dotenv()

app = FastAPI(title="Titanic Chatbot API")

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    text: str
    image_base64: str | None = None

# Initialize Dataset and Agent globally
try:
    df = pd.read_csv("backend/titanic.csv")
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    agent = create_pandas_dataframe_agent(
        llm, 
        df, 
        verbose=True, 
        allow_dangerous_code=True,
        agent_type="zero-shot-react-description",
    )
except Exception as e:
    print(f"Error initializing agent or loading data: {e}")
    df = None
    agent = None

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    if not agent:
        raise HTTPException(status_code=500, detail="Agent not initialized. Ensure backend/titanic.csv exists and GEMINI_API_KEY is set.")
    
    # Pre-prompt to strictly handle plotting
    system_instruction = """
You are a helpful data analysis assistant for the Titanic dataset. 
If the user asks for a chart, visualization, or plot, you must use matplotlib (plt) or seaborn to create it, save the figure exactly to 'current_plot.png', and clear the plot afterwards using plt.clf().
Always use `plt.savefig('current_plot.png')` when asked to draw a plot.
"""
    
    if os.path.exists('current_plot.png'):
        os.remove('current_plot.png')
        
    try:
        full_query = f"{system_instruction}\n\nUser Question: {request.query}"
        response = agent.invoke({"input": full_query})
        output_text = response.get('output', str(response))
        
        image_b64 = None
        if os.path.exists('current_plot.png'):
            with open('current_plot.png', "rb") as image_file:
                image_b64 = base64.b64encode(image_file.read()).decode('utf-8')
            os.remove('current_plot.png')
            
        return ChatResponse(text=output_text, image_base64=image_b64)
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
