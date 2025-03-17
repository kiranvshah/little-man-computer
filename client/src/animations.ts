import {
	getMemoryLocationValueSpan,
	getRegisterValueSpan,
} from "./registerAndMemoryUtilities.js";
import { Transfer } from "./transferInterface.js";

/**
 * Runs the animation of a transfer between two elements.
 * @param {HTMLElement} elementToTranslate the HTML element of the dot that needs to be animated. It should already be at the starting location.
 * @param {HTMLElement} destination a HTML element at the destination location of the dot
 * @returns {Promise<void>} promise is resolved once animation is complete
 */
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

	const dx = endRect.left - startRect.left;
	const dy = endRect.top - startRect.top;

	// work out distance to find duration
	const distance = Math.sqrt(dx ** 2 + dy ** 2);
	const duration = 0.5 + distance / 150;
	dot.style.animationDuration = duration + "s";

	dot.style.setProperty("--dx", dx + "px");
	dot.style.setProperty("--dy", dy + "px");
	dot.classList.add("moving");

	return new Promise<void>(resolve => {
		dot.addEventListener("animationend", () => {
			destination.appendChild(dot);
			dot.classList.remove("moving");
			dot.style.removeProperty("animation-duration");
			resolve();
		});
	});
}

/**
 * Animates a dot in-place to demonstrate a change that doesn't involve movement (e.g. incrementing the program counter)
 * @param {HTMLElement} elementToAnimate the HTML element of the dot that needs animating. It should already be at the right location.
 * @returns {Promise<void>} promise is resolved once animation is complete
 */
async function animateStationary(elementToAnimate: HTMLElement) {
	const dot = elementToAnimate;
	dot.classList.add("stationary-animating");

	return new Promise<void>(resolve => {
		dot.addEventListener("animationend", () => {
			dot.classList.remove("stationary-animating");
			resolve();
		});
	});
}

/**
 * Creates an animation from A to B (A can equal B)
 * @param {string} dotInnerText text to display inside the dot being animated 
 * @param {HTMLElement} start the HTML element to begin the animation at 
 * @param {HTMLElement} end the HTML element to end the animation at 
 * @returns {Promise<void>} promise is resolved once animation is complete
 */
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
		await animateStationary(dot);
	} else {
		await animateTranslation(dot, end);
	}

	return new Promise<void>(resolve => {
		setTimeout(() => {
			dot.remove();
			resolve();
		}, 1000);
	});
}

/**
 * Displays an appropriate animation for one transfer
 * @param {Transfer} transfer the transfer object containing information about the animation 
 * @param {HTMLSpanElement[]} memoryContentsSpans the array of <span> elements that contain the memory contents
 * @returns {Promise<void>} promise is resolved once animation is complete
 */
export async function animateTransfer(
	transfer: Transfer,
	memoryContentsSpans: HTMLSpanElement[],
) {
	if (!animationsAreSwitchedOn()) {
		return new Promise<void>(resolve => {
			setTimeout(resolve, 300);
		});
	}

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

/**
 * Checks whether animations have been switched on or off by the user
 * @returns {boolean} true if animations are on, false if they're off
 */
export function animationsAreSwitchedOn() {
	return localStorage.getItem("animationsToggle") != "off";
}

/**
 * Turns animations on and stores this in localStorage
 */
export function turnOnAnimations() {
	localStorage.setItem("animationsToggle", "on");
}

/**
 * Turns animations off and stores this in localStorage
 */
export function turnOffAnimations() {
	console.log("animations turned off");
	localStorage.setItem("animationsToggle", "off");
}
