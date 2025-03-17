const memoryTableBody = document.getElementById(
	"memoryTbody",
) as HTMLTableElement;
export const memoryContentsSpans: HTMLSpanElement[] = [];

// populate memory table with initial values (addresses and 000 for all values)
for (let rowNumber = 0; rowNumber < 10; rowNumber++) {
	const row = document.createElement("tr");
	for (let colNumber = 0; colNumber < 10; colNumber++) {
		const memoryAddress = rowNumber * 10 + colNumber;
		const cell = document.createElement("td");
		cell.classList.add("text-center", "p-0", "font-monospace");

		const memoryAddressLabel = document.createElement("span");
		memoryAddressLabel.classList.add("small", "text-secondary");
		memoryAddressLabel.innerText = memoryAddress.toString().padStart(2, "0");

		const memoryContentsSpan = document.createElement("span");
		memoryContentsSpan.classList.add("transfer-dot-parent");
		memoryContentsSpan.innerText = "000";
		memoryContentsSpans.push(memoryContentsSpan);

		cell.appendChild(memoryAddressLabel);
		cell.appendChild(document.createElement("br"));
		cell.appendChild(memoryContentsSpan);
		row.appendChild(cell);
	}
	memoryTableBody.appendChild(row);
}
