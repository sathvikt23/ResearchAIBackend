from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import requests
import json
import re
import io
import base64

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as needed for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RequestData(BaseModel):
    data: str
    username: str
    type: str 

def extract_json(text: str):
    pattern = r'(?<=```json\n)(\{.*?\})(?=\n```|$)'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        json_data = match.group(1)
        return json.loads(json_data)
    return None

def create_dataframe(request_data: RequestData, data, plot_type, username):
    fquery = """
        **Task:** Extract and format sales data from the provided text according to the specified structure.

        **Instructions:**
        1. **Input:** You will receive a text.
        2. **Output Format:** Return the extracted data in the following JSON-like format:
        {
            "Categories_column": [<list of names>],
            "Values_column": [<list of corresponding values in integer datatype>]
        }"""
    fquery += f"text {data}"
    myobj = {
        "data": "",
        "username": f"{username}",
        "query": fquery
    }
    try:
        x = requests.post('http://127.0.0.1:5100/askLLM', json=myobj)
        x.raise_for_status()  # Raise HTTPError for bad responses
        y = x.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Request failed: {e}")

    json_data = extract_json(y['message'])
    if not json_data:
        raise HTTPException(status_code=500, detail="Failed to extract JSON data from response.")

    categories = json_data["Categories_column"]
    values = list(map(int, json_data["Values_column"]))

    df = pd.DataFrame({"Values": values}, index=categories)
    return df

def generate_plot_image(plot_func, df):
    buf = io.BytesIO()
    fig, ax = plt.subplots(figsize=(10, 6))
    plot_func(df, ax)
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def bar_chart(df, ax):
    df.mean().plot(kind='bar', ax=ax, color='skyblue', edgecolor='black')
    ax.set_title('Bar Plot')
    ax.set_xlabel('Categories')
    ax.set_ylabel('Mean Values')

def scatter_chart(df, ax):
    for column in df:
        ax.scatter(df.index, df[column], label=column)
    ax.set_title('Scatter Plot')
    ax.set_xlabel('Index')
    ax.set_ylabel('Values')
    ax.legend()

def line_chart(df, ax):
    df.plot(kind='line', ax=ax, marker='o')
    ax.set_title('Line Plot')
    ax.set_xlabel('Index')
    ax.set_ylabel('Values')

def histogram_chart(df, ax):
    for column in df:
        ax.hist(df[column], bins=5, alpha=0.5, label=column, edgecolor='black')
    ax.set_title('Overlayed Histograms')
    ax.set_xlabel('Value')
    ax.set_ylabel('Frequency')
    ax.legend()

@app.post("/plot")
def generate_plot(request_data: RequestData):
    plot_type = request_data.type
    username = request_data.username
    data = request_data.data
    
    df = create_dataframe(request_data, data, plot_type, username)
    
    if plot_type == 'Bar Graph':
        plot_func = bar_chart
    elif plot_type == 'Scatter Graph':
        plot_func = scatter_chart
    elif plot_type == 'Line Graph':
        plot_func = line_chart
    elif plot_type == 'Histogram':
        plot_func = histogram_chart
    else:
        raise HTTPException(status_code=400, detail="Invalid plot type. Choose from: bar, scatter, line, histogram.")

    # Generate the plot image
    img_base64 = generate_plot_image(plot_func, df)

    # Return the image URL in a JSON response
    return {"imageURL": f"data:image/png;base64,{img_base64}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
