/**
 * Updates the value displayed in a given location in RAM.
 * @param {string} address The address of the RAM location to update (0-99).
 * @param {string} value The value to change the display to (0-999).
 * @param {HTMLSpanElement[]} memoryContentsSpans The array of <span> elements that contain the memory contents.
 */
export function updateMemoryLocation(
	address: string,
	value: string,
	memoryContentsSpans: HTMLSpanElement[],
) {
	console.assert(value.length == 3);
	memoryContentsSpans[Number(address)].innerText = value;
}

export function updateRegisterByCode(
	code: "PC" | "ACC" | "IR" | "MAR" | "MDR" | "CARRY",
	value: string,
) {
	({
		PC: updateProgramCounter,
		ACC: updateAccumulator,
		MAR: updateMar,
		MDR: updateMdr,
		IR: updateIr,
		CARRY: updateCarryFlag,
	})[code](value);
}

/**
 * Updates the value displayed in the program counter.
 * @param {string} value The value to display (0-99).
 */
export function updateProgramCounter(value: string) {
	console.assert(value.length == 2);
	const pcSpan = document.getElementById(
		"programCounterValueSpan",
	) as HTMLSpanElement;
	pcSpan.innerText = value;
}

/**
 * Updates the value displayed in the accumulator.
 * @param {string} value The value to display (0-999).
 */
export function updateAccumulator(value: string) {
	console.assert(value.length == 3);
	const accSpan = document.getElementById(
		"accumulatorValueSpan",
	) as HTMLSpanElement;
	accSpan.innerText = value;
}

/**
 * Updates the value displayed in the MAR.
 * @param {string} value The value to display (0-99).
 */
export function updateMar(value: string) {
	console.assert(value.length == 2);
	const marSpan = document.getElementById("marValueSpan") as HTMLSpanElement;
	marSpan.innerText = value;
}

/**
 * Updates the value displayed in the MDR.
 * @param {string} value The value to display (0-999).
 */
export function updateMdr(value: string) {
	console.assert(value.length == 3);
	const mdrSpan = document.getElementById("mdrValueSpan") as HTMLSpanElement;
	mdrSpan.innerText = value;
}

/**
 * Updates the value displayed in the instruction register.
 * @param {string} value The value to display (0-9).
 */
export function updateIr(value: string) {
	console.assert(value.length == 1);
	const irSpan = document.getElementById("irValueSpan") as HTMLSpanElement;
	irSpan.innerText = value;
}

/**
 * Updates the value displayed in the carry flag.
 * @param {string} value The value to display (0 or 1).
 */
export function updateCarryFlag(value: string) {
	console.assert(value == "0" || value == "1");
	const carrySpan = document.getElementById(
		"carryValueSpan",
	) as HTMLSpanElement;
	carrySpan.innerText = value;
}
