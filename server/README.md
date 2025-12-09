# Source for the webdash.dev website

This repository contains the source code for the [webdash.dev](https://webdash.dev) website, which showcases the WebDash project.

## Install
1. Clone the repository
   ```bash
    git clone https://github.com/4rchXceed/webdash.dev.git
    cd webdash.dev-server/server
   ```
2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
3. Copy .env.example to .env and set your environment variables (ADMIN_TOKEN=your_token_here)
   ```bash
   cp .env.example .env
   ```
4. Run the development server
   ```bash
   fastapi dev main.py
   ```
6. The api is available at `http://localhost:8000` (use the client to access the website)

## Server

The server is built with [FastAPI](https://fastapi.tiangolo.com/).
It provides a REST API for the client to interact with the portfolio data.
It uses JSON data files to store the portfolio information. (No database required, because it's a simple portfolio. I'll add database support later if needed, see [WhyNotDatabase.md](WhyNotDatabase.md) for more information)

## Client

The client is built with [SvelteKit](https://kit.svelte.dev/) and is available at [Gitea](https://github.com/4rchXceed/webdash.dev).

## Structure

Server:
- `main.py`: The main entry point for the FastAPI server.
- `config.py`: Configuration management.

## Future plans

- Add a blog section to the website
- Add database support (SQLite, PostgreSQL, etc.)

## Contributing

Bah this is a portfolio, what the hell would you want to contribute to it for? Oh and the gitea instance does not accept new accounts so you can't even open a PR.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.