export function updateMemoryLocation(
	address: number,
	value: number,
	memoryContentsSpans: HTMLSpanElement[],
) {
	memoryContentsSpans[address].innerText = value.toString().padStart(3, "0");
}
