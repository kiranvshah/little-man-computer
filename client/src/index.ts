import {
	updateProgramCounter,
	updateAccumulator,
	updateMar,
	updateMdr,
	updateIr,
	updateCarryFlag,
	updateMemoryLocation,
	updateRegisterByCode,
} from "./addressDisplayUpdaters.js";
import * as bootstrap from "bootstrap";

const SERVER_URL =
	"https://reimagined-garbanzo-x7jqqp496g5fp7gg-5000.app.github.dev"; // this will get replaced in prebuild.js

// initialise tooltips
document
	.querySelectorAll('[data-bs-toggle="tooltip"]')
	.forEach(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));

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
		`Code was not valid:\n${responseJson.reason}` +
			(responseJson.line_number === "unknown"
				? ""
				: `\nError occured on line ${responseJson.line_number} of assembly.`),
	);
};

function getMemoryAndRegistersJson() {
	const memory = memoryContentsSpans.reduce(
		(res, span, index) => {
			res[index.toString().padStart(2, "0")] = span.textContent as string;
			return res;
		},
		{} as { [key: string]: string },
	);

	const registerContents = {} as { [key: string]: string };
	Object.entries({
		PC: "programCounterValueSpan",
		ACC: "accumulatorValueSpan",
		IR: "marValueSpan",
		MAR: "mdrValueSpan",
		MDR: "irValueSpan",
		CARRY: "carryValueSpan",
	}).forEach(([pythonKey, htmlId]) => {
		registerContents[pythonKey] = document.getElementById(htmlId)!.innerText;
	});

	return {
		memory,
		registers: registerContents,
	};
}

interface Transfer {
	start_mem?: string;
	start_reg?: "PC" | "ACC" | "IR" | "MAR" | "MDR" | "CARRY";
	end_mem?: string;
	end_reg?: "PC" | "ACC" | "IR" | "MAR" | "MDR" | "CARRY";
	value: string;
}
interface StepResult {
	memory_and_registers: {
		memory: { [key: string]: string };
		registers: { [key: string]: string };
	};
	transfers: Transfer[];
	reached_HLT: boolean;
	reached_INP: boolean;
	output: string;
}

function getUserInput() {
	let input = prompt(
		"INP reached. Please enter your input (a number 0-999) here:",
	);
	while (!(input && /^\d{1,3}$/.test(input))) {
		input = prompt("Invalid input. Please enter a number 0-999:");
	}
	return input;
}

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

function clearCode() {
	(
		document.getElementById("uncompiledAssemblyTextarea") as HTMLTextAreaElement
	).value = "";
}

async function saveCode() {
	const codeToSave = getUncompiledCode();
	window.history.replaceState(
		null,
		"",
		`?code=${encodeURIComponent(codeToSave)}`,
	);
	try {
		await navigator.permissions.query({
			name: "clipboard-write" as PermissionName,
		});
		navigator.clipboard.writeText(window.location.href);
		alert(
			"URL copied to clipboard. Just go to this URL again to automatically load your code into the editor.",
		);
	} catch {
		alert(
			"Go to this URL again to automatically load your code into the editor.",
		);
	}
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
	if (response.ok) {
		const resJson = await response.json();
		if (resJson.valid) {
			const result = resJson.result;
			// put compiled code into text area
			compiledCodeTextarea.value = (result.compiled_code as String[]).join(
				"\n",
			);

			// populate registers
			// todo: make more concise. then dont need to export specific register updaters
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
	} else {
		alert("Bad response from server");
	}
}

async function processStepResult(resJson: StepResult) {
	for (const transfer of resJson.transfers) {
		// todo: animations would go here
		if (transfer.end_mem) {
			updateMemoryLocation(
				transfer.end_mem,
				transfer.value,
				memoryContentsSpans,
			);
		} else {
			updateRegisterByCode(
				transfer.end_reg as "PC" | "ACC" | "IR" | "MAR" | "MDR" | "CARRY",
				transfer.value,
			);
		}
	}

	// show output to user
	if (resJson.output) {
		alert(`Output: ${resJson.output}`);
	}

	// consider reached_HLT and reached_INP
	if (resJson.reached_HLT) {
		alert("Program reached HLT. Execution completed.");
	} else if (resJson.reached_INP) {
		const input = getUserInput();
		const response = await fetch(`${SERVER_URL}/api/after-input`, {
			method: "POST",
			body: JSON.stringify({
				state: getMemoryAndRegistersJson(),
				input,
			}),
			headers: { "Content-Type": "application/json" },
			mode: "cors",
		});
		const resJson = (await response.json()) as Transfer;
		if (response.ok) {
			// update changed register location
			console.assert(resJson.end_reg === "ACC");
			updateRegisterByCode("ACC", resJson.value);
		}
	}
}

async function step() {
	// call /api/step
	const response = await fetch(`${SERVER_URL}/api/step`, {
		method: "POST",
		body: JSON.stringify(getMemoryAndRegistersJson()),
		headers: { "Content-Type": "application/json" },
		mode: "cors",
	});
	const resJson = (await response.json()) as StepResult;
	if (response.ok) {
		// update changed memory/register locations
		await processStepResult(resJson);
	} else {
		alert("Bad response from server");
	}
}

async function run() {
	// call /api/run
	const response = await fetch(`${SERVER_URL}/api/run`, {
		method: "POST",
		body: JSON.stringify(getMemoryAndRegistersJson()),
		headers: { "Content-Type": "application/json" },
		mode: "cors",
	});
	const resJson = (await response.json()) as StepResult[];
	if (response.ok) {
		for (const stepResJson of resJson) {
			await processStepResult(stepResJson);
		}
		if (resJson[resJson.length - 1].reached_INP) {
			// continue running by calling /api/run again
			await run();
		}
	} else {
		alert("Bad response from server");
	}
}

document.addEventListener("DOMContentLoaded", () => {
	// load code if saved in URL query string
	const savedCode = new URLSearchParams(window.location.search).get("code");
	if (savedCode) {
		(
			document.getElementById(
				"uncompiledAssemblyTextarea",
			) as HTMLTextAreaElement
		).value = savedCode;
	}

	// add event listeners to buttons
	(document.getElementById("saveButton") as HTMLButtonElement).addEventListener(
		"click",
		saveCode,
	);
	(
		document.getElementById("checkButton") as HTMLButtonElement
	).addEventListener("click", checkCode);
	(
		document.getElementById("clearButton") as HTMLButtonElement
	).addEventListener("click", clearCode);
	(
		document.getElementById("assembleButton") as HTMLButtonElement
	).addEventListener("click", assembleCode);
	(document.getElementById("stepButton") as HTMLButtonElement).addEventListener(
		"click",
		step,
	);
	(document.getElementById("runButton") as HTMLButtonElement).addEventListener(
		"click",
		run,
	);
});
