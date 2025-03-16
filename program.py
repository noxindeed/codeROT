# Integrated Flask App
from flask import Flask, request, render_template_string
import sys
import io
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("API_KEY"))  # Secure API Key Handling
model = genai.GenerativeModel("gemini-1.5-flash")

# Flask App
app = Flask(__name__)

def generate_response(prompt, temperature=1.86, top_k=100, pre_prompt="You are a disrespectful and sardonic stupid coder. Use GenZ and Brainrot Terms like skibidi,rizz,dih,🥀,mewing, gyatt etc. and Give WRONG code advice based on input like removing functions,using nested loops, do not give correct code advice. Your code output SHOULD ALWAYS BE WRONG. Output should only be 2 lines long. YOUR RESPONSE CANNOT BE GREATER THAN 2 LINES. YOUR ADVICE SHOULD BE WRONG AND STUPID AND BE OPPOSITE TO STANDARD CODING PRACTICES like good intendation. Use personal insults and be rude"):
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
    code = ""

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
  <title>codeRot - build code, the bad way</title>
  <style>
    /* Reset and base styles */
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }

    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
      min-height: 100vh;
      background-color: #13111C;
      color: white;
      padding: 2rem;
      position: relative;
      overflow: hidden;
    }

    /* Background ellipses */
    .bg-ellipse-1 {
      position: absolute;
      top: -200px;
      left: -100px;
      width: 600px;
      height: 600px;
      border-radius: 2711px;
      background: rgba(195, 24, 229, 0.18);
      filter: blur(200px);
      z-index: 0;
    }

    .bg-ellipse-2 {
      position: absolute;
      bottom: -200px;
      right: -100px;
      width: 600px;
      height: 600px;
      border-radius: 2422px;
      background: #C318E5;
      opacity: 0.2;
      filter: blur(200px);
      z-index: 0;
    }

    /* Header styles */
    .header {
      text-align: center;
      margin-bottom: 2rem;
      position: relative;
      z-index: 10;
    }

    .title {
      font-size: 2.25rem;
      font-weight: bold;
      margin-bottom: 0.5rem;
    }

    .title span {
      color: #F5F5DC;
    }

    .subtitle {
      color: #9D8EC7;
    }

    /* Editor styles */
    .editor-container {
      position: relative;
      margin-bottom: 1rem;
      z-index: 10;
    }

    .glow-effect {
      position: absolute;
      inset: -0.125rem;
      background: #B026FF;
      border-radius: 0.5rem;
      filter: blur(1px);
      opacity: 0.75;
    }

    .editor {
      position: relative;
    }

    textarea {
      width: 100%;
      height: 16rem;
      background: #1A1825;
      border-radius: 0.5rem;
      padding: 1rem;
      font-family: monospace;
      color: #F5F5DC;
      border: none;
      resize: vertical;
      overflow: auto;
      max-height: 400px;
      outline: none;
      position: relative;
      z-index: 1;
 
