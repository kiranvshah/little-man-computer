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
import { animateTransfer } from "./animations.js";
import { memoryContentsSpans } from "./memoryPopulation.js";
import { Transfer } from "./transferInterface.js";

const SERVER_URL = "%%SERVER_URL%%"; // this will get replaced in prebuild.js

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
export async function checkCode() {
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
export function clearCode() {
	(
		document.getElementById("uncompiledAssemblyTextarea") as HTMLTextAreaElement
	).value = "";
}
export async function saveCode() {
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
export async function assembleCode() {
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
		await animateTransfer(transfer, memoryContentsSpans);
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
		if (response.ok) {
			const resJson = (await response.json()) as Transfer;
			// update changed register location
			console.assert(resJson.end_reg === "ACC");
			updateRegisterByCode("ACC", resJson.value);
		}
	}
}
export async function step() {
	// call /api/step
	const response = await fetch(`${SERVER_URL}/api/step`, {
		method: "POST",
		body: JSON.stringify(getMemoryAndRegistersJson()),
		headers: { "Content-Type": "application/json" },
		mode: "cors",
	});
	if (response.ok) {
		const resJson = (await response.json()) as StepResult;
		// update changed memory/register locations
		await processStepResult(resJson);
	} else {
		console.log(response)
		alert("Bad response from server");
	}
}
export async function run() {
	// call /api/run
	const response = await fetch(`${SERVER_URL}/api/run`, {
		method: "POST",
		body: JSON.stringify(getMemoryAndRegistersJson()),
		headers: { "Content-Type": "application/json" },
		mode: "cors",
	});
	if (response.ok) {
		const resJson = (await response.json()) as StepResult[];
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
