const fs = require("fs");
const path = require("path");

const indexTsPath = path.join(__dirname, "src", "buttonResponders.ts");
const serverUrl = process.env.SERVER_URL || "http://localhost:5000";

let contents = fs.readFileSync(indexTsPath, "utf-8");
contents = contents.replace(/%%SERVER_URL%%/g, serverUrl);

fs.writeFileSync(indexTsPath, contents);
