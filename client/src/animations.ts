async function animateTranslation(elementToTranslateId: string, endId: string) {
	const dot = document.getElementById(elementToTranslateId)!;
	const originParent = dot.parentElement!;
	const destinationParent = document.getElementById(endId)!;

	const startRect = dot.getBoundingClientRect();
	destinationParent.appendChild(dot); // move dot to destination in order to get final coords
	const endRect = dot.getBoundingClientRect();
	originParent.appendChild(dot); // move dot back to origin before animation begins

	const dx = endRect.left - startRect.left + "px";
	const dy = endRect.top - startRect.top + "px";

	dot.style.setProperty("--dx", dx);
	dot.style.setProperty("--dy", dy);
	dot.classList.add("moving");
	dot.addEventListener("animationend", () => {
		destinationParent.appendChild(dot);
		dot.classList.remove("moving");
	});

	return new Promise(resolve => setTimeout(resolve, 3000)); // only return once animation complete
}

export async function createDotAndAnimateFromAToB(
	dotInnerText: string,
	startElementId: string,
	endElementId: string,
) {
	// create dot
	const startParent = document.getElementById(startElementId)!;
	const dot = document.createElement("div");
	dot.classList.add("transfer-dot");
	dot.innerText = dotInnerText;
	dot.id = performance.now().toString(); // unique id in case multiple dots exist at once
	startParent.appendChild(dot);

	await animateTranslation(dot.id, endElementId);

	// destroy dot after 1s
	setTimeout(() => dot.remove(), 1000);
}
