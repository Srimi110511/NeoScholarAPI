from flask import Flask, request, jsonify
import openai  # Correct import
import os

app = Flask(__name__)

# Home Route to Fix 404 Error
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to NeoScholar API! Use /generate-content to get study notes."})

# Use environment variable for API key
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/generate-content", methods=["POST"])
def generate_content():
    data = request.json
    topic = data.get("topic", "No topic provided")
    mode = data.get("mode", "Comprehensive")

    # 🔹 Improved Prompt for Better Content Structure
    prompt = f"""
    Generate a structured {mode.lower()} study guide for '{topic}'.  
    The guide should include the following sections:

    1️⃣ **Introduction**  
       - Briefly introduce the topic.  
       - Explain why it is important.  

    2️⃣ **Key Theories & Concepts**  
       - Explain major theories or models related to this topic.  
       - Provide relevant examples.  

    3️⃣ **Use Cases & Applications**  
       - Describe real-world applications in different industries.  
       - Provide case studies if applicable.  

    4️⃣ **Challenges & Ethical Considerations**  
       - Discuss any major challenges, limitations, or risks.  
       - Cover ethical concerns related to this topic.  

    5️⃣ **Future Trends & Innovations**  
       - Predict future advancements.  
       - Mention new technologies or research developments.  

    Ensure the response is **detailed, well-structured, and easy to understand**.  
    If applicable, include **bullet points, real-world examples, and references to research.**  
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )

        content_generated = response["choices"][0]["message"]["content"].strip()

        return jsonify({
            "title": f"{mode} Notes for {topic}",
            "content": content_generated
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))