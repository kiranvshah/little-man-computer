# LMC Frontend

## Structure

- `.vscode/` contains editor settings for VS Code
- `assets/styles/` contains CSS
- `src/` contains TypeScript source code (entry point is `index.ts`)
- `prebuild.js` runs before the TS build process, and is responsible for accessing an environment variable on host machine for the server API URL, and subtituting it into `index.ts`

## Setup

- Ensure pnpm is installed
- Run `pnpm install` in the `client` directory in a terminal

## Running

To run, there needs to be an environment variable on the host machine named `SERVER_URL` that contains the URL of the server, e.g. `https://www.example.com`.

### Development

In VS Code:

- Run `pnpm watch` in a terminal
- Go to `index.html` and run "Live Preview: Show Preview (External Browser)"

### Production

I host the frontend on Netlify. Configuration:

- Base directory set to `client`
- Build command set to `pnpm build`
