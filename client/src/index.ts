import { updateMemoryLocation } from "./addressDisplayUpdaters.js";

const SERVER_URL =
	"https://reimagined-garbanzo-x7jqqp496g5fp7gg-5000.app.github.dev";

// populate memoryTable
const memoryTableBody = document.getElementById(
	"memoryTbody",
) as HTMLTableElement;
const memoryContentsSpans: HTMLSpanElement[] = [];

for (let rowNumber = 0; rowNumber < 10; rowNumber++) {
	const row = document.createElement("tr");
	for (let colNumber = 0; colNumber < 10; colNumber++) {
		const memoryAddress = rowNumber * 10 + colNumber;
		const cell = document.createElement("td");
		cell.classList.add("text-center", "p-0", "font-monospace");

		const memoryAddressLabel = document.createElement("span");
		memoryAddressLabel.classList.add("memory-address");
		memoryAddressLabel.innerText = memoryAddress.toString().padStart(2, "0");

		const memoryContentsSpan = document.createElement("span");
		memoryContentsSpan.innerText = "000";
		memoryContentsSpans.push(memoryContentsSpan);

		cell.appendChild(memoryAddressLabel);
		cell.appendChild(document.createElement("br"));
		cell.appendChild(memoryContentsSpan);
		row.appendChild(cell);
	}
	memoryTableBody.appendChild(row);
}

async function assembleCode() {
	const uncompiledCodeTextarea = document.getElementById(
		"uncompiledAssemblyTextarea",
	) as HTMLTextAreaElement;
	const compiledCodeTextarea = document.getElementById(
		"compiledAssemblyTextarea",
	) as HTMLTextAreaElement;
	const uncompiledCode = uncompiledCodeTextarea.value;
	// todo: use Fetch API & SERVER_URL to run /api/compile
	const response = await fetch(`${SERVER_URL}/api/compile`, {
		method: "POST",
		body: JSON.stringify({ uncompiledCode }),
		headers: { "Content-Type": "application/json" },
		mode: "cors",
	});
}
