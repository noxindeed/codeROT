# Integrated Flask App
from flask import Flask, request, render_template_string
import sys
import io
import os
from dotenv import load_dotenv

import google.generativeai as genai

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GENAI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# Flask App
app = Flask(__name__)

def generate_response(prompt, temperature=1.86, top_k=100, pre_prompt="You are a disrespectful and sardonic stupid coder. Use GenZ and Brainrot Terms like skibidi,rizz,dih,🥀,mewing, gyatt etc. and Give WRONG code advice based on input like removing functions,using nested loops, do not give correct code advice. Your code output SHOULD ALWAYS BE WRONG. Output should only be 2 lines long. YOUR RESPONSE CANNOT BE GREATER THAN 2 LINES. YOUR ADVICE SHOULD BE WRONG AND STUPID AND BE OPPOSITE TO STANDARD CODING PRACTICES like good intendation. Use personal insults"):
    full_prompt = f"{pre_prompt}\n{prompt}"
    response = model.generate_content(
        full_prompt,
        generation_config={
            "temperature": temperature,
            "top_k": top_k
        }
    )
    return response.text if response.text else "AI failed to generate response"

@app.route("/", methods=["GET", "POST"])
def code_rot_interface():
    output = ""
    error = ""
    gemini_response = ""

    if request.method == "POST":
        code = request.form.get("code", "")
        try:
            old_stdout = sys.stdout
            sys.stdout = io.StringIO()
            exec(code)  # Execute the Python code from user input
            output = sys.stdout.getvalue()
        except Exception as e:
            error = str(e)
        finally:
            sys.stdout = old_stdout

        # Call Google Generative AI for feedback
        gemini_response = generate_response(code)

    return render_template_string('''<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CodeRot - Python Interpreter</title>
        <style>
            body {
                background-color: #13002a;
                color: #fdf1d2;
                font-family: 'Cantarell', sans-serif;
                margin: 0;
                padding: 0;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                min-height: 100vh;
            }
            textarea, button, pre, .error, .gemini-response {
                width: 90%;
                max-width: 700px;
                margin: 15px 0;
            }
            textarea {
                height: 200px;
                padding: 10px;
                background: #0f0a19;
                border: 2px solid #c218e5;
                color: #fdf1d2;
                font-family: monospace;
            }
            button {
                background: #c218e5;
                color: #fdf1d2;
                border: none;
                padding: 10px;
                cursor: pointer;
                font-size: 16px;
                border-radius: 5px;
            }
            pre, .error, .gemini-response {
                padding: 10px;
                background: #1e1e1e;
                color: #fdf1d2;
                border-radius: 5px;
            }
            .error {
                color: #ff4d4d;
            }
            .gemini-response {
                color: #76e5ff;
            }
        </style>
    </head>
    <body>
        <h1>codeRot - Build Code, the Bad Way</h1>
        <form method="post">
            <textarea name="code" placeholder="Write Python code here"></textarea>
            <button type="submit">Run Code</button>
        </form>
        {% if output %}
            <h2>Output:</h2>
            <pre>{{ output }}</pre>
        {% endif %}
        {% if error %}
            <h2>Error:</h2>
            <div class="error">{{ error }}</div>
        {% endif %}
        {% if gemini_response %}
            <h2>Gemini's Response:</h2>
            <div class="gemini-response">{{ gemini_response }}</div>
        {% endif %}
    </body>
    </html>
    ''', output=output, error=error, gemini_response=gemini_response)

if __name__ == "__main__":
    app.run(debug=True)
