import os
import openai
from flask import Flask, request, render_template
from PyPDF2 import PdfReader

app = Flask(__name__)

# Configure sua API Key


def extract_text_from_file(file):
    extension = os.path.splitext(file.filename)[1].lower()
    if extension == ".txt":
        return file.read().decode("utf-8", errors="ignore")
    elif extension == ".pdf":
        reader = PdfReader(file)
        pages = [page.extract_text() for page in reader.pages]
        return "\n".join(pages)
    return ""

def classify_email(email_text: str) -> str:
    try:
        prompt = f"""
O usuário enviou este email:
\"\"\"{email_text}\"\"\"

Classifique como:
- "Produtivo" se o email requer ação ou resposta (ex: suporte técnico, pergunta, etc.).
- "Improdutivo" se for apenas felicitações, agradecimentos ou não requer ação.

Retorne SOMENTE a palavra "Produtivo" ou "Improdutivo".
"""
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um sistema de classificação de emails."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=10,
            temperature=0.0
        )
        classification_text = response.choices[0].message.content.strip()  # <- aqui mudamos para .content

        if "produtivo" in classification_text.lower():
            return "Produtivo"
        else:
            return "Improdutivo"
    except Exception as e:
        print("Erro na classificação:", e)
        return "Improdutivo"

def generate_response(category: str, email_text: str) -> str:
    if category.lower() == "produtivo":
        try:
            prompt = f"""
O usuário enviou este email em português:
\"\"\"{email_text}\"\"\"

Responda de forma breve (até 3 frases), profissional e em português.
"""
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Você é um assistente que responde e-mails em português de forma profissional e breve."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.7
            )
            generated_text = response.choices[0].message.content.strip()  # <- também aqui
            return generated_text
        except Exception as e:
            print("Erro ao gerar resposta:", e)
            return "Não foi possível gerar a resposta no momento."
    else:
        return "Obrigado pelo seu email! Não há ação necessária no momento."

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("emailFile")
        user_text = request.form.get("emailText", "")

        if file and file.filename:
            extracted_text = extract_text_from_file(file)
            if extracted_text.strip():
                user_text = extracted_text

        if not user_text.strip():
            return render_template("index.html", error="Nenhum conteúdo fornecido!")

        # Classificar
        classification = classify_email(user_text)
        # Gerar resposta
        response_text = generate_response(classification, user_text)

        return render_template(
            "index.html",
            original_text=user_text,
            classification=classification,
            response_suggestion=response_text
        )

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
