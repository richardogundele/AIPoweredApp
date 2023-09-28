Use this repo as a template to deploy a Python [FastAPI](https://fastapi.tiangolo.com) service on Render.
See https://render.com/docs/deploy-fastapi or follow the steps below:

# Backend Chat App with FastAPI, GPT-4 and SQLite
This is a simple chat application built using FastAPI and SQLite. It allows users to interact with a chatbot that responds to text and speech inputs. Conversations are stored in an SQLite database for future reference.

## Features
- **Text Chat**: Users can input text messages and receive responses from the chatbot.

- **Speech Input**: Users can send speech inputs, which are converted to text and processed.

- **Chat History**: Conversations are saved in an SQLite database, allowing users to retrieve previous chat history.

## Setup
To run this project, follow these steps:

1. **Clone the Repository:**
   
2. **Create a Virtual Environment:**
   
3. **Activate the Virtual Environment:**
- On Windows:
  ``` venv\Scripts\activate  ```
- On macOS and Linux:
  ```  source venv/bin/activate  ```
  
4. **Install Dependencies:**

5. **Database Setup:**
- Create an SQLite database file named `chat_app.db`.
- Run the database setup script to create the necessary tables:
  ```  python database_setup.py  ```

6. **Environment Variables:**
- Create a `.env` file in the project root and configure any necessary environment variables, such as your OpenAI API key and other settings.

7. **Run the Application:**

8. **Access the App:**
Open your web browser and go to `http://localhost:8000` to access the chat application.

## Usage

- Register or log in using your email address.
- Use the text input or speech input to interact with the chatbot.
- Chat history is saved and can be retrieved by clicking on the "History" button.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - A modern, fast, web framework for building APIs.
- [SQLite](https://www.sqlite.org/) - A lightweight, embedded relational database.

## Contributing

Contributions are welcome! Please open an issue or create a pull request if you have any suggestions or improvements for this project.

