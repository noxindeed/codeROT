from flask import Flask, request, render_template_string
import sys
import io

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def python_interpreter():
    output = ""
    if request.method == "POST":
        code = request.form.get("code", "")
        try:
            # Redirect stdout to capture print statements
            old_stdout = sys.stdout
            sys.stdout = io.StringIO()
            exec(code)
            output = sys.stdout.getvalue()
        except Exception as e:
            output = f"Error: {e}"
        finally:
            sys.stdout = old_stdout
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Python Interpreter</title>
            <style>
                body {
                    background-color: #121212;
                    color: #ffffff;
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    flex-direction: column;
                    height: 100vh;
                }
                h1 {
                    margin: 10px 0;
                }
                form {
                    width: 100%;
                    max-width: 500px;
                    margin-bottom: 20px;
                }
                textarea {
                    width: 100%;
                    background-color: #1e1e1e;
                    color: #ffffff;
                    border: 1px solid #333333;
                    border-radius: 5px;
                    padding: 10px;
                    resize: none;
                    font-family: 'Courier New', Courier, monospace;
                    font-size: 14px;
                }
                button {
                    background-color: #007bff;
                    color: #ffffff;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 5px;
                    cursor: pointer;
                    font-size: 16px;
                }
                button:hover {
                    background-color: #0056b3;
                }
                pre {
                    width: 100%;
                    max-width: 500px;
                    background-color: #1e1e1e;
                    color: #00ff00;
                    border: 1px solid #333333;
                    border-radius: 5px;
                    padding: 10px;
                    overflow-x: auto;
                }
            </style>
        </head>
        <body>
            <h1>Python Interpreter</h1>
            <form method="post">
                <textarea name="code" rows="10" placeholder="Write your Python code here"></textarea><br>
                <button type="submit">Run</button>
            </form>
            <h2>Output:</h2>
            <pre>{{ output }}</pre>
        </body>
        </html>
    ''', output=output)

if __name__ == "__main__":
    app.run(debug=True)
