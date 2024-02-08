import os
import re
from openai import OpenAI
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Global array to store pathology samples
pathology_samples = []
percentages = []
gleason_score = []
gleason_value = []
@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        path_result = request.form["prostate_path"]
        system_prompt = """Please help process the following pathology report. Please report the samples with prostate cancer with the following format "A. Right Base Gleason Score 3+4 3/4 cores positive (75%), max core length 5mm)". 
        please report samples without cancer as well. keep output clear and succint as possible."""
        print(path_result)
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": path_result}
            ]
        )
        # Splitting the response into individual samples and storing them
        processed_samples = response.choices[0].message.content.split("\n")
        
        for sample in processed_samples:
            if sample.strip():  # Ensure the sample is not just empty space
                pathology_samples.append(sample)

        for sample in processed_samples:
            match = re.search(r"(\d+)%", sample)
            if match:
                percentages.append(int(match.group(1)))

        for sample in processed_samples:
            match = re.search(r"Gleason Score (\d+)\+(\d+) = (\d+)", sample)
            if match:
                gleason_score.append(match.group())
                gleason_value.append(int(match.group(3)))



        return redirect(url_for("index", result=response.choices[0].message.content))

    result = request.args.get("result")
    return render_template("index.html", result=result, samples=pathology_samples, score = gleason_score, value = gleason_value, percentage = percentages)

if __name__ == "__main__":
    app.run(debug=True)
