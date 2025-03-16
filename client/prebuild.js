const fs = require("fs");
const path = require("path");

const scriptPath = path.join(__dirname, "src", "buttonResponders.ts");
const serverUrl = process.env.SERVER_URL || "http://localhost:5000";

const exampleAssemblyProgram = fs.readFileSync(
	path.join(__dirname, "..", "example_assembly_program.txt"),
);

let contents = fs.readFileSync(scriptPath, "utf-8");
contents = contents.replace(/%%SERVER_URL%%/g, serverUrl);
contents = contents.replace(
	/%%EXAMPLE_ASSEMBLY_PROGRAM%%/g,
	exampleAssemblyProgram,
);

fs.writeFileSync(scriptPath, contents);
