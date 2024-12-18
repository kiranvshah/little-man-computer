const fs = require("fs");
const path = require("path");

const indexTsPath = path.join(__dirname, "src", "index.ts");
const serverUrl = process.env.SERVER_URL || "http://localhost:5000";

let contents = fs.readFileSync(indexTsPath);
contents = contents.replace(/%%SERVER_URL%%/g, serverUrl);
