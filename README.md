# 📧 Classificador de Emails com IA 🤖

![Flask](https://img.shields.io/badge/Flask-3.1.0-blue?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--3.5-turbo-ff69b4?style=flat-square)
![Render](https://img.shields.io/badge/Deployed%20on-Render-46a2f1?style=flat-square)

## 🚀 Sobre o Projeto
Este é um classificador de emails que utiliza **Inteligência Artificial (OpenAI GPT-3.5)** para classificar emails em **Produtivo** ou **Improdutivo**. Além disso, ele sugere respostas automáticas para emails produtivos.

O projeto possui uma interface web moderna, desenvolvida com **Flask** e **Bootstrap**, permitindo o upload de arquivos `.txt` e `.pdf` para análise.

---

## 🎥 Demonstração
Acesse a aplicação online clicando no link abaixo:

🔗 **[Classificador de Emails - Deploy no Render](https://case-pratico.onrender.com/)**

*(Caso o serviço esteja em suspensão, pode levar alguns segundos para iniciar após o primeiro acesso.)*

---

## 📂 Funcionalidades
✅ **Classificação de Emails:** Define se um email é **Produtivo** ou **Improdutivo**  
✅ **Geração de Respostas Automáticas:** Sugere respostas profissionais para emails produtivos  
✅ **Upload de Arquivos:** Suporta arquivos **.txt** e **.pdf**  
✅ **Design Moderno:** Interface estilizada com **Bootstrap**  
✅ **Feedback Instantâneo:** Exibição de resultado em tempo real  

---

## 🛠️ Tecnologias Utilizadas
- **Python 3.11**
- **Flask 3.1**
- **OpenAI GPT-3.5 API**
- **Bootstrap 5**
- **NLTK para pré-processamento de texto**
- **PyPDF2 para extração de texto de PDFs**

---

## 🔧 Como Rodar o Projeto Localmente

### 📌 Pré-requisitos
- Python 3.11+ instalado
- Criar um ambiente virtual `venv`
- API Key da OpenAI

### 1️⃣ Clone o repositório
```bash
git clone https:/(https://github.com/Alejandroo19/teste_tecnico.git)
```

### 2️⃣ Crie um ambiente virtual e ative-o

- Criar o ambiente virtual
python -m venv venv

- Ativar no Windows:
venv\Scripts\activate

- Ativar no Mac/Linux:
source venv/bin/activate
source venv/bin/activate

### 3️⃣ Instale as dependências
- pip install -r requirements.txt

### 5️⃣ Rode o servidor Flask

```bash
python app.py
```
