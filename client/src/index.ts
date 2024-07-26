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
		cell.classList.add("text-center");
		cell.classList.add("p-0");

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
