/**
 * Updates the value displayed in a given location in RAM.
 * @param {number} address The address of the RAM location to update (0-99).
 * @param {number} value The value to change the display to (0-999). 
 * @param {HTMLSpanElement[]} memoryContentsSpans The array of <span> elements that contain the memory contents.
 */
export function updateMemoryLocation(
	address: number,
	value: number,
	memoryContentsSpans: HTMLSpanElement[],
) {
	memoryContentsSpans[address].innerText = value.toString().padStart(3, "0");
}

/**
 * Updates the value displayed in the program counter.
 * @param {number} value The value to display (0-99).
 */
export function updateProgramCounter(value: number) {
	const pcSpan = document.getElementById(
		"programCounterValueSpan",
	) as HTMLSpanElement;
	pcSpan.innerText = value.toString();
}

/**
 * Updates the value displayed in the accumulator.
 * @param {number} value The value to display (0-999). 
 */
export function updateAccumulator(value: number) {
	const accSpan = document.getElementById(
		"accumulatorValueSpan",
	) as HTMLSpanElement;
	accSpan.innerText = value.toString();
}

/**
 * Updates the value displayed in the MAR.
 * @param {number} value The value to display (0-99).
 */
export function updateMar(value: number) {
	const marSpan = document.getElementById("marValueSpan") as HTMLSpanElement;
	marSpan.innerText = value.toString();
}

/**
 * Updates the value displayed in the MDR.
 * @param {number} value The value to display (0-999).
 */
export function updateMdr(value: number) {
	const mdrSpan = document.getElementById("mdrValueSpan") as HTMLSpanElement;
	mdrSpan.innerText = value.toString();
}
