from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import os

app = Flask(__name__)

# Store feedbacks in memory (or load from file)
feedbacks = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    data = request.get_json()
    
    name = data.get("name") or "Anonymous"
    location = data.get("location")
    comment = data.get("comment")
    category = data.get("category", "General")
    rating = data.get("rating", "Not Rated")

    if not location or not comment:
        return jsonify({"error": "Missing data"}), 400

    entry = {
        "Name": name,
        "Location": location,
        "Category": category,
        "Rating": rating,
        "Comment": comment
    }

    feedbacks.append(entry)

    # Save to Excel
    df = pd.DataFrame(feedbacks)
    df.to_excel("feedbacks.xlsx", index=False)

    return jsonify({"message": "Feedback saved", "feedbacks": feedbacks})

@app.route('/get_feedbacks')
def get_feedbacks():
    return jsonify(feedbacks)

@app.route('/download_excel')
def download_excel():
    file_path = "feedbacks.xlsx"
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return "No feedback file found", 404

if __name__ == '__main__':
    app.run(debug=True)