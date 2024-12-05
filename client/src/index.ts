import {
	updateProgramCounter,
	updateAccumulator,
	updateMar,
	updateMdr,
	updateIr,
	updateCarryFlag,
	updateMemoryLocation,
} from "./addressDisplayUpdaters.js";

const SERVER_URL =
	"https://reimagined-garbanzo-x7jqqp496g5fp7gg-5000.app.github.dev";
// todo: is there some way this could be an environment variable? i shouldn't really have a fixed URL in the git

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

const getUncompiledCode = () =>
	(document.getElementById("uncompiledAssemblyTextarea") as HTMLTextAreaElement)
		.value;

const reportAssemblyCompilationError = (responseJson: {
	reason: string;
	line_number: string;
}) => {
	alert(
		`Code was not valid:\n${responseJson.reason}\nError occured on line ${responseJson.line_number} of assembly.`,
	);
};

async function checkCode() {
	const uncompiledCode = getUncompiledCode();
	const response = await fetch(`${SERVER_URL}/api/check`, {
		method: "POST",
		body: JSON.stringify({ uncompiledCode }),
		headers: { "Content-Type": "application/json" },
		mode: "cors",
	});
	if (!response.ok) alert("Bad response from server");
	const resJson = await response.json();
	if (resJson.valid) {
		alert("Code was valid :)"); // todo: is there a bootstrap way of making these alerts look nicer?
	} else reportAssemblyCompilationError(resJson);
}

async function assembleCode() {
	const compiledCodeTextarea = document.getElementById(
		"compiledAssemblyTextarea",
	) as HTMLTextAreaElement;
	const uncompiledCode = getUncompiledCode();
	// use Fetch API & SERVER_URL to run /api/compile
	const response = await fetch(`${SERVER_URL}/api/compile`, {
		method: "POST",
		body: JSON.stringify({ uncompiledCode }),
		headers: { "Content-Type": "application/json" },
		mode: "cors",
	});
	const resJson = await response.json();
	if (resJson.valid) {
		const result = resJson.result;
		// put compiled code into text area
		compiledCodeTextarea.value = (result.compiled_code as String[]).join("\n");

		// populate registers
		updateProgramCounter(result.memory_and_registers.registers.PC);
		updateAccumulator(result.memory_and_registers.registers.ACC);
		updateMar(result.memory_and_registers.registers.MAR);
		updateMdr(result.memory_and_registers.registers.MDR);
		updateIr(result.memory_and_registers.registers.IR);
		updateCarryFlag(result.memory_and_registers.registers.CARRY);

		// populate memory
		for (const [location, contents] of Object.entries(
			result.memory_and_registers.memory,
		)) {
			updateMemoryLocation(location, contents as string, memoryContentsSpans);
		}
	} else reportAssemblyCompilationError(resJson);
}

async function step() {
	// todo
}

async function run() {
	// todo
}

document.addEventListener("DOMContentLoaded", () => {
	(
		document.getElementById("checkButton") as HTMLButtonElement
	).addEventListener("click", checkCode);
	(
		document.getElementById("assembleButton") as HTMLButtonElement
	).addEventListener("click", assembleCode);
	(document.getElementById("stepButton") as HTMLButtonElement).addEventListener(
		"click",
		step,
	);
	(document.getElementById("runButton") as HTMLButtonElement).addEventListener(
		"run",
		step,
	);
});
