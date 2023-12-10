## KnowledgeQuizBot
Your learning companion on Telegram! Upload PDFs for courses in multiple languages. 
Whether transitioning careers or expanding expertise, simplify your learning journey effortlessly.

[LIVE DEMO](https://t.me/knowledge_quiz_bot)

Key Features:

1. 📑 PDF-Based Learning: Upload your PDF documents, and KnowledgeQuizBot will generate comprehensive educational courses from the content provided, ensuring a seamless learning experience.
2. 🌐 Multilingual Support: Irrespective of the language of the uploaded document, the bot assists in creating courses in multiple languages, aiding in a broader reach and understanding.
3. 🛤️ Customized Learning Paths: Tailored courses are created, helping users grasp new concepts or delve deeper into specific topics essential for their career development.
4. 🧠 Interactive Quizzes: Engage in interactive quizzes and assessments based on the course material to reinforce learning and track progress effectively.
5. 🤝 Seamless Integration: Access your courses anytime, anywhere within Telegram, making learning convenient and accessible on-the-go.

How It Works:

1. 📥 Upload your PDF document, specifying the desired language for the course generation.
2. 🔄 KnowledgeQuizBot processes the content and creates a structured course curriculum.
3. 🎓 Dive into the generated course, participate in quizzes, and expand your knowledge effortlessly.

Start your learning journey with KnowledgeQuizBot today and pave your way to mastery in your chosen field! 🚀🌟

### Run local

Create python environment: 

    python3 -m venv env
    source env/bin/activate

Install requirements:

    pip3 install -r source/backend/bot/requirements.txt

Setup environment variables. Fill in all the variables in the source/backend/example.env
    
    set -o allexport; source source/backend/example.env; set +o allexport

Rub bot:
    
    cd source/backend
    python3 run.py
    
    
