# Source for the webdash.dev website

This repository contains the source code for the [webdash.dev](https://webdash.dev) website, which showcases the WebDash project.

## Install
1. Clone the repository
   ```bash
   git clone https://webdash.dev/git/WebDash/webdash.dev
   cd webdash.dev
   ```
2. Install dependencies
   ```bash
   npm install
   ```
3. Modify `src/lib/globals.ts` -> API_URL to point to your own server (if you have one)
4. Run the development server
   ```bash
   npm run dev -- --open
   ```
5. Open [http://localhost:5173](http://localhost:5173) in your browser

## Server

The server is avilable at [Gitea](https://webdash.dev/git/WebDash/webdash.dev-server) and is built with [FastAPI](https://fastapi.tiangolo.com/).
It serves the API endpoints.

## Client

The client is built with [SvelteKit](https://kit.svelte.dev/).


## Structure

Client:
- Admin panel (xyz/admin)
    1. Manage the content of the "portfolio" (Who am I, Projects, Hobbies, Skills, Footer, Timeline)
- Public website (xyz/)
    1. Landing page (portfolio)

## Future plans

- Add a blog section to the website
- Improve the design and user experience

## Contributing

Bah this is a portfolio, what the hell would you want to contribute to it for? Oh and the gitea instance does not accept new accounts so you can't even open a PR.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.