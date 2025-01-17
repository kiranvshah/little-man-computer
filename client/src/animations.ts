export function animateTranslation(endId: string) {
	const dot = document.getElementById("dot") as HTMLDivElement;
	const destinationParent = document.getElementById(endId) as HTMLDivElement;

	const startRect = dot.getBoundingClientRect();

	// move dot
	destinationParent.appendChild(dot);
	const endRect = dot.getBoundingClientRect();

	const dx = startRect.left - endRect.left + "px";
	const dy = startRect.top - endRect.top + "px";
	dot.style.setProperty("--dx", dx);
	dot.style.setProperty("--dy", dy);
	dot.classList.add("mover");
	dot.addEventListener("animationend", () => {
		destinationParent.appendChild(dot);
		dot.classList.remove("mover");
	});
}
