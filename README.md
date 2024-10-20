# Medibot 🤖

**Medibot** is an open-source Discord bot designed to facilitate the organization and management of tutoring sessions for various subjects. Built using modern technologies, Medibot streamlines the process of scheduling and tracking sessions, helping students and educators connect efficiently in a virtual environment. The bot is continuously running on a cloud platform to ensure 24/7 availability and security.

## Technologies Used ⚙️

- **Python**: The core programming language used to develop Medibot, chosen for its versatility and strong community support.
- **discord.py**: A Python wrapper for the Discord API, which enables seamless integration of bot commands and interaction with Discord servers.
- **PostgreSQL**: A powerful, open-source relational database system used to store and manage tutoring session data, ensuring persistence and reliability.
- **psycopg2**: A PostgreSQL adapter for Python, providing the bridge between Python code and the PostgreSQL database for efficient data management.
- **Docker**: A platform used to containerize the bot, ensuring consistent development and production environments, simplifying deployment and scaling.
- **fly.io**: A modern cloud platform that hosts Medibot, providing high availability and security, ensuring that the bot runs continuously without interruption.

## Features 🚀

### Available Commands:
1. **`/medibot`** - Displays an informative message ℹ️ about Medibot and its available commands.
2. **`/meditatii`** - Shows all tutoring sessions 📅 on your server, along with the status of each session (Past, Today, or In X days).
3. **`/meditatie`** - Manages tutoring sessions. Accepts the following parameters:
   - **`add <subject> [date]`** - Adds a tutoring session for the specified subject. The date is optional; if not provided, it defaults to today 🕒.
   - **`delete <id>`** - Deletes a tutoring session 🗑️ using its ID.

### Planned Features 🔮:
- User ability to join a tutoring session 🙋.
- Send notifications to participants before a session begins ⏰.
- Automated report generation 📊 for tutoring session participation.
- Feedback system 📝 and progress tracking for users.

## Installation 🛠️

Follow these steps to install and run Medibot locally:

1. Clone the repository:
    ```bash
    git clone https://github.com/mihaiprodann/medibot
    cd medibot
    ```

2. Create the `.env` file:
    ```bash
    cp .env.example .env
    ```

3. Update the `.env` file with the following variables:
    - **TOKEN**: Your Discord bot's token 🤖.
    - **DATABASE_URL**: PostgreSQL connection string 🗄️.

4. Run the bot using Docker 🐳:
    ```bash
    docker-compose up --build
    ```

---

Medibot is built to provide a seamless experience for organizing tutoring sessions on Discord. With easy-to-use commands and future enhancements on the way, it aims to become an essential tool for virtual learning communities.
