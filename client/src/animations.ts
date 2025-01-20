export function animateTranslation(endId: string) {
	const dot = document.getElementById("dot") as HTMLDivElement;
	const originParent = dot.parentElement!;
	const destinationParent = document.getElementById(endId) as HTMLDivElement;

	const startRect = dot.getBoundingClientRect();
	destinationParent.appendChild(dot); // move dot to destination in order to get final coords
	const endRect = dot.getBoundingClientRect();
	originParent.appendChild(dot); // move dot back to origin before animation begins

	const dx = endRect.left - startRect.left + "px";
	const dy = endRect.top - startRect.top + "px";

	dot.style.setProperty("--dx", dx);
	dot.style.setProperty("--dy", dy);
	dot.classList.add("mover");
	dot.addEventListener("animationend", () => {
		destinationParent.appendChild(dot);
		dot.classList.remove("mover");
	});
}
