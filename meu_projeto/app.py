import os
import openai
import re
import unicodedata
from flask import Flask, request, render_template
from PyPDF2 import PdfReader

app = Flask(__name__)

# ✅ Função de Pré-processamento (sem NLTK)
def preprocess_text(text):
    """
    Faz o pré-processamento do texto:
    - Converte para minúsculas
    - Remove acentos
    - Remove pontuações
    - Remove números
    - Remove múltiplos espaços
    """
    if not text:
        return ""

    # Converte para minúsculas
    text = text.lower()

    # Remove acentos
    text = ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )

    # Remove pontuação e caracteres especiais
    text = re.sub(r'[^\w\s]', '', text)

    # Remove números
    text = re.sub(r'\d+', '', text)

    # Remove múltiplos espaços
    text = re.sub(r'\s+', ' ', text).strip()

    return text

# ✅ Função para extrair texto de arquivos PDF/TXT
def extract_text_from_file(file):
    extension = os.path.splitext(file.filename)[1].lower()
    if extension == ".txt":
        return file.read().decode("utf-8", errors="ignore")
    elif extension == ".pdf":
        reader = PdfReader(file)
        pages = [page.extract_text() for page in reader.pages]
        return "\n".join(pages)
    return ""

# ✅ Função para classificar email (inclui pré-processamento)
def classify_email(email_text: str) -> str:
    try:
        # 🔥 Aplica pré-processamento ANTES de enviar para a IA
        cleaned_text = preprocess_text(email_text)

        prompt = f"""
O usuário enviou este email:
\"\"\"{cleaned_text}\"\"\"  

Classifique como:
- "Produtivo" se o email requer ação ou resposta (ex: suporte técnico, pergunta, etc.).
- "Improdutivo" se for apenas felicitações, agradecimentos ou não requer ação.

Exemplos:
1. "Olá, como você está?" → Improdutivo  
2. "Preciso de ajuda para acessar o sistema" → Produtivo  
3. "Obrigado pelo suporte!" → Improdutivo  
4. "Qual o status do meu pedido?" → Produtivo  

Retorne SOMENTE a palavra "Produtivo" ou "Improdutivo".
"""
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um classificador de emails."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=10,
            temperature=0.0
        )
        classification_text = response.choices[0].message.content.strip()

        return "Produtivo" if "produtivo" in classification_text.lower() else "Improdutivo"

    except Exception as e:
        print("Erro na classificação:", e)
        return "Improdutivo"

# ✅ Função para gerar resposta baseada na classificação
def generate_response(category: str, email_text: str) -> str:
    if category.lower() == "produtivo":
        try:
            prompt = f"""
O usuário enviou este email em português:
\"\"\"{email_text}\"\"\"  

Responda de forma breve (até 3 frases), profissional e objetiva.  
Não adicione assinaturas como "Atenciosamente" ou "[Seu Nome]".
"""
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Você é um assistente que responde e-mails de forma profissional e breve."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.7
            )
            generated_text = response.choices[0].message.content.strip()
            return generated_text
        except Exception as e:
            print("Erro ao gerar resposta:", e)
            return "Não foi possível gerar a resposta no momento."
    else:
        return "Obrigado pelo seu email! Não há ação necessária no momento."

# ✅ Rota principal do Flask
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

        # 🔥 Aplica pré-processamento antes da classificação
        processed_text = preprocess_text(user_text)

        # 🔥 Classifica o email
        classification = classify_email(processed_text)

        # 🔥 Gera resposta automática
        response_text = generate_response(classification, user_text)

        return render_template(
            "index.html",
            original_text=user_text,
            classification=classification,
            response_suggestion=response_text
        )

    return render_template("index.html")

# ✅ Executa o servidor Flask
if __name__ == "__main__":
    app.run(debug=True)
