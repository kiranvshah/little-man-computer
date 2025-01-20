import {
	getMemoryLocationValueSpan,
	getRegisterValueSpan,
} from "./addressDisplayUpdaters.js";
import { Transfer } from "./transferInterface.js";

async function animateTranslation(
	elementToTranslate: HTMLElement,
	destination: HTMLElement,
) {
	const dot = elementToTranslate;
	const origin = dot.parentElement!;

	const startRect = dot.getBoundingClientRect();
	destination.appendChild(dot); // move dot to destination in order to get final coords
	const endRect = dot.getBoundingClientRect();
	origin.appendChild(dot); // move dot back to origin before animation begins

	const dx = endRect.left - startRect.left + "px";
	const dy = endRect.top - startRect.top + "px";

	dot.style.setProperty("--dx", dx);
	dot.style.setProperty("--dy", dy);
	dot.classList.add("moving");
	dot.addEventListener("animationend", () => {
		destination.appendChild(dot);
		dot.classList.remove("moving");
	});

	return new Promise(resolve => setTimeout(resolve, 3000)); // only return once animation complete
}

async function createDotAndAnimateFromAToB(
	dotInnerText: string,
	origin: HTMLElement,
	destination: HTMLElement,
) {
	// create dot
	const dot = document.createElement("div");
	dot.classList.add("transfer-dot");
	dot.innerText = dotInnerText;
	origin.appendChild(dot);

	await animateTranslation(dot, destination);

	// destroy dot after 1 sec, then return
	return new Promise<void>(resolve => {
		setTimeout(() => {
			dot.remove();
			resolve();
		}, 1000);
	});
}

export async function animateTransfer(
	transfer: Transfer,
	memoryContentsSpans: HTMLSpanElement[],
) {
	if (
		!(transfer.start_mem || transfer.start_reg) ||
		!(transfer.end_mem || transfer.end_reg)
	) {
		console.warn("Not animating transfer due to no start or no end");
		return;
	}

	const start = transfer.start_mem
		? getMemoryLocationValueSpan(transfer.start_mem, memoryContentsSpans)
		: getRegisterValueSpan(transfer.start_reg!);
	const end = transfer.end_mem
		? getMemoryLocationValueSpan(transfer.end_mem, memoryContentsSpans)
		: getRegisterValueSpan(transfer.end_reg!);

	await createDotAndAnimateFromAToB(transfer.value, start, end);
}
