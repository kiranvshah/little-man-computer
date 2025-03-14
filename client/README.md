# LMC Frontend

## Structure

- `.vscode/` contains editor settings for VS Code
- `assets/` contains static files (that are served "as is")
  - `assets/styles/` contains CSS
- `src/` contains TypeScript source code (entry point is `index.ts`). See below for descriptions of each file.
- `index.html` is the main HTML file for the web page.
- `prebuild.js` runs before the TS build process, and is responsible for accessing an environment variable on host machine for the server API URL, and subtituting it into `index.ts`

### TypeScript files

- `src/animations.ts` contains the code that runs the animations during the fetch-decode-execute cycle. It also has the logic to turn animations on and off.
- `src/buttonResponders.ts` contains the code that runs whenever a button is clicked. It therefore contains lots of calls to the backend.
- `src/index.ts` is the entry point (i.e. it is run by `index.html`).
- `src/memoryPopulation.ts` is run on page load to add values (initially 000 to each memory location). It also exports a list of `span` elements, each representing a different memory location.
- `src/registerAndMemoryUtilities.ts` exports helper functions that can update the value of or return the HTML element of every memory location and every register.
- `src/transferInterface.ts` exports the TypeScript interface describing a `Transfer` object (a movement of data between memory/registers).

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
