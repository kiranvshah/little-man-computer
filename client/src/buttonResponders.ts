import {
	updateMemoryLocation,
	updateRegisterByCode,
	RegisterCode,
} from "./registerAndMemoryUtilities.js";
import { animateTransfer } from "./animations.js";
import { memoryContentsSpans } from "./memoryPopulation.js";
import { Transfer } from "./transferInterface.js";

const SERVER_URL = "%%SERVER_URL%%"; // this will get replaced by prebuild.js

/**
 * Gets the user-written assembly code that is in textarea.
 * @returns {string} the user-written assembly code
 */
function getUncompiledCode() {
	return (
		document.getElementById("uncompiledAssemblyTextarea") as HTMLTextAreaElement
	).value;
}

/**
 * Alerts the user that there was an error trying to assemble the code.
 * @param responseJson An object containing the reason for the error and the line number it occurred.
 */
function reportAssemblyCompilationError(responseJson: {
	reason: string;
	line_number: string;
}) {
	alert(
		`Code was not valid:\n${responseJson.reason}` +
			(responseJson.line_number === "unknown"
				? ""
				: `\nError occured on line ${responseJson.line_number} of assembly.`),
	);
}

/**
 * Gets the current state of the Little Man Computer.
 * @returns An object containing the current contents of the memory and registers.
 */
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

/**
 * The response from the server for one fetch-decode-execute cycle.
 */
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

/**
 * Gets the user to input a three-digit number
 * @returns {string} The number (0-999) that the user inputted.
 */
function getUserInput() {
	let input = prompt(
		"INP reached. Please enter your input (a number 0-999) here:",
	);
	while (!(input && /^\d{1,3}$/.test(input))) {
		input = prompt("Invalid input. Please enter a number 0-999:");
	}
	return input;
}

/**
 * Runs when the "Check" button is pressed. Checks that the user-written assembly code is valid and alerts the user to the result.
 */
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
		alert("Code was valid :)");
	} else reportAssemblyCompilationError(resJson);
}

/**
 * Runs when the "Clear" button is pressed. Clears the contents of the user-written assembly code textarea.
 */
export function clearCode() {
	(
		document.getElementById("uncompiledAssemblyTextarea") as HTMLTextAreaElement
	).value = "";
}

/**
 * Runs when the "Save" button is pressed. Updates the URL to encode the current program and copies URL to clipboard.
 */
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

/**
 * Runs when the "Assemble" button is pressed. Assembles user-written code into object code and machine code, and loads these into the LMC.
 */
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
			compiledCodeTextarea.value = (result.object_code as String[]).join("\n");

			// populate registers
			Object.entries(result.memory_and_registers.registers).forEach(
				([code, value]) =>
					updateRegisterByCode(code as RegisterCode, value as string),
			);

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

/**
 * Runs after response from server for one fetch-decode-execute cycle is receieved.
 * @param {StepResult} resJson The response object from the server representing one FDE cycle
 */
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
			updateRegisterByCode(transfer.end_reg as RegisterCode, transfer.value);
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

/**
 * Runs after the "Step" button is pressed. Sends the state of the LMC to the server and handles response.
 */
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
		alert(`Bad response from server: ${await response.text()}`);
	}
}

/**
 * Runs after the "Run" button is pressed. Sends the state of the LMC to the server and handles response.
 */
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

/**
 * Runs when the "Load example program" button is pressed. Loads the example assembly program into the editor.
 */
export function loadExampleProgram() {
	const uncompiledAssemblyTextarea = document.getElementById(
		"uncompiledAssemblyTextarea",
	) as HTMLTextAreaElement;
	if (
		uncompiledAssemblyTextarea.value &&
		!confirm(
			"Caution: loading example program will overwrite contents of editor. Continue?",
		)
	) {
		return;
	}
	uncompiledAssemblyTextarea.value = `%%EXAMPLE_ASSEMBLY_PROGRAM%%`; // this will get replaced by prebuild.js
}
