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

	return new Promise<void>(resolve => {
		dot.addEventListener("animationend", () => {
			destination.appendChild(dot);
			dot.classList.remove("moving");
			setTimeout(resolve, 1000);
		});
	});
}

async function animateStationary(elementToTranslate: HTMLElement) {
	const dot = elementToTranslate;
	dot.classList.add("stationary-animating");
	dot.addEventListener("animationend", () => {
		dot.classList.remove("stationary-animating");
	});

	return new Promise<void>(resolve => {
		dot.addEventListener("animationend", () => {
			dot.classList.remove("stationary-animating");
			resolve();
		});
	});
}

async function createDotAndAnimate(
	dotInnerText: string,
	start: HTMLElement,
	end: HTMLElement,
) {
	// create dot
	const dot = document.createElement("div");
	dot.classList.add("transfer-dot");
	dot.innerText = dotInnerText;
	start.appendChild(dot);

	if (start === end) {
		console.log("animating in place");
		await animateStationary(dot);
	} else {
		await animateTranslation(dot, end);
	}

	dot.remove();
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

	await createDotAndAnimate(transfer.value, start, end);
}
