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

function getMemoryAndRegistersJson() {
	const memory = memoryContentsSpans.reduce(
		(res, span, index) => {
			res[index.toString().padStart(2, "0")] = span.textContent as string;
			return res;
		},
		{} as { [key: string]: string },
	);

	// todo: could the following register bit be done more succintly?
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
	start_reg?: string;
	end_mem?: string;
	end_reg?: string;
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
}

async function step() {
	// get contents of memory and registers as JSON
	const memoryAndRegistersContents = getMemoryAndRegistersJson();

	// call /api/step
	const response = await fetch(`${SERVER_URL}/api/step`, {
		method: "POST",
		body: JSON.stringify(memoryAndRegistersContents),
		headers: { "Content-Type": "application/json" },
		mode: "cors",
	});
	const resJson = (await response.json()) as StepResult;
	if (response.ok) {
		// update changed memory/register locations
		for (const transfer of resJson.transfers) {
			// todo: animations would go here
			if (transfer.end_mem) {
				updateMemoryLocation(
					transfer.end_mem,
					transfer.value,
					memoryContentsSpans,
				);
			} else {
				const codesToUpdaters = {
					"PC": updateProgramCounter,
					"ACC": updateAccumulator,
					"MAR": updateMar,
					"MDR": updateMdr,
					"IR": updateIr,
					"CARRY": updateCarryFlag,
				};
				codesToUpdaters[transfer.end_reg as keyof typeof codesToUpdaters](transfer.value);
			}
		}
		// todo: consider reached_HLT and reached_INP
	} else {
		// todo
	}
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
		run,
	);
});
