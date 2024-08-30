import matplotlib.pyplot as plt
import pandas as pd
import requests 
import json
import re

# Functions for Plotting
def bar(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    df.mean().plot(kind='bar', ax=ax, color='skyblue', edgecolor='black')
    ax.set_title('Bar Plot')
    ax.set_xlabel('Categories')
    ax.set_ylabel('Mean Values')
    plt.show()

def scatter(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    for column in df:
        ax.scatter(df.index, df[column], label=column)
    ax.set_title('Scatter Plot')
    ax.set_xlabel('Index')
    ax.set_ylabel('Values')
    ax.legend()
    plt.show()

def line(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    df.plot(kind='line', ax=ax, marker='o')
    ax.set_title('Line Plot')
    ax.set_xlabel('Index')
    ax.set_ylabel('Values')
    plt.show()

def histo(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    for column in df:
        ax.hist(df[column], bins=5, alpha=0.5, label=column, edgecolor='black')
    ax.set_title('Histograms')
    ax.set_xlabel('Value')
    ax.set_ylabel('Frequency')
    ax.legend()
    plt.show()

# Request Data from Server
myobj = {
    "data": "",
    "username": "blabla@gmail.com",
    "query": """
    **Task:** Extract and format sales data from the provided text according to the specified structure.

    **Instructions:**
    1. **Input:** You will receive a text.
    2. **Output Format:** Return the extracted data in the following JSON-like format:
       {
         "Categories_column": [<list of names>],
         "Values_column": [<list of corresponding values in integer datatype>]
       }

    text:Product A: With 100 units sold, Product A has the lowest sales among the three products. 
          Product B: Product B's sales of 150 units suggest a moderate level of market success.
          Product C: Product C leads with 200 units sold, indicating it is the most successful product in this dataset.
    """
}
x = requests.post('http://127.0.0.1:5100/askLLM', json=myobj)
y = x.json()

# Extract JSON from the Response
def extract_json(text):
    pattern = r'(?<=```json\n)(\{.*?\})(?=\n```|$)'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        json_data = match.group(1)
        return json.loads(json_data)  # Load the JSON string to a Python dict
    return None

# Process the Response
json_data = extract_json(y['message'])
categories = json_data["Categories_column"]
values = list(map(int, json_data["Values_column"]))  # Convert values to integers

# Create a DataFrame
df = pd.DataFrame({"Values": values}, index=categories)

# Plotting the Data
bar(df)
scatter(df)
line(df)
histo(df)
