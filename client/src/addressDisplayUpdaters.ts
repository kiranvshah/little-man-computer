export function updateMemoryLocation(
	address: number,
	value: number,
	memoryContentsSpans: HTMLSpanElement[],
) {
	memoryContentsSpans[address].innerText = value.toString().padStart(3, "0");
}

export function updateProgramCounter(value: number) {
	const pcSpan = document.getElementById(
		"programCounterValueSpan",
	) as HTMLSpanElement;
	pcSpan.innerText = value.toString();
}

export function updateAccumulator(value: number) {
	const accSpan = document.getElementById(
		"accumulatorValueSpan",
	) as HTMLSpanElement;
	accSpan.innerText = value.toString();
}

export function updateMar(value: number) {
	const marSpan = document.getElementById("marValueSpan") as HTMLSpanElement;
	marSpan.innerText = value.toString();
}

export function updateMdr(value: number) {
	const mdrSpan = document.getElementById("mdrValueSpan") as HTMLSpanElement;
	mdrSpan.innerText = value.toString();
}
