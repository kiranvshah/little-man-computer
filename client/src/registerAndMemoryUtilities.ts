/**
 * Returns the HTML span element of a memory location given its address.
 * @param {string} address The address of the memory location (0-99).
 * @param {HTMLSpanElement[]} memoryContentsSpans The array of <span> elements that contain the memory contents.
 * @returns {HTMLSpanElement} The HTML span element of the relevant memory address.
 */
export function getMemoryLocationValueSpan(
	address: string,
	memoryContentsSpans: HTMLSpanElement[],
) {
	return memoryContentsSpans[Number(address)];
}

export type RegisterCode = "PC" | "ACC" | "IR" | "MAR" | "MDR" | "CARRY";

/**
 * Returns the HTML span element of a register given its code.
 * @param {RegisterCode} code The 2-5 character long code representing the register.
 * @returns {HTMLSpanElement} The HTML span element of the relevant register.
 */
export function getRegisterValueSpan(code: RegisterCode) {
	return document.getElementById(
		{
			PC: "programCounterValueSpan",
			ACC: "accumulatorValueSpan",
			MAR: "marValueSpan",
			MDR: "mdrValueSpan",
			IR: "irValueSpan",
			CARRY: "carryValueSpan",
		}[code],
	) as HTMLSpanElement;
}

/**
 * Updates the value displayed in a given location in memory.
 * @param {string} address The address of the memory location to update (0-99).
 * @param {string} value The value to change the display to (0-999).
 * @param {HTMLSpanElement[]} memoryContentsSpans The array of <span> elements that contain the memory contents.
 */
export function updateMemoryLocation(
	address: string,
	value: string,
	memoryContentsSpans: HTMLSpanElement[],
) {
	console.assert(value.length == 3);
	getMemoryLocationValueSpan(address, memoryContentsSpans).innerText = value;
}

/**
 * Updates the value displayed in a given register.
 * @param {RegisterCode} code The 2-5 character long code representing the register.
 * @param {string} value The value to update the register to.
 */
export function updateRegisterByCode(code: RegisterCode, value: string) {
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
