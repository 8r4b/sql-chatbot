SQL Chatbot
This project is a conversational AI chatbot that interacts with your database using natural language. Built with LangChain and Streamlit, it allows users to query their database by simply asking questions.

🚀 Getting Started
Follow these steps to get your SQL Chatbot up and running.

📦 Install Dependencies
First, install the necessary Python packages:

```bash
pip install -r requirements.txt
```

⚙️ Configure Your Environment
Create a file named .env in the root directory of your project and add the following environment variables. Remember to replace the placeholder values with your actual credentials.

```env
OPENAI_API_KEY=your_openai_key
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=your_db_name
```

🏃‍♀️ Run the Chatbot
Once your dependencies are installed and your .env file is configured, you can launch the chatbot:

```bash
streamlit run main.py
```

🧠 Technologies Used
LangChain: For orchestrating the conversational AI logic.
Streamlit: For creating the interactive web interface.
OpenAI GPT-3.5: The large language model powering the chatbot's understanding and generation.
SQLAlchemy: For interacting with the database.
python-dotenv: For managing environment variables.
📂 Folder Structure
```
sql_chatbot/
├── main.py
├── requirements.txt
├── .env
├── .gitignore
├── README.md
└── screenshots/
└── demo.png
```

📬 Contact
Made with ❤️ by Mohamed Osama
