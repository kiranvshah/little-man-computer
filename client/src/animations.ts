export function animateFromIRToPC() {
    const dot = document.getElementById("dot") as HTMLDivElement;
    const originParent = document.getElementById("dotOrigin") as HTMLDivElement;
    const destinationParent = document.getElementById("dotDestination") as HTMLDivElement;

    const startRect = dot.getBoundingClientRect();
    const startX = startRect.left;
    const startY = startRect.top;

    // move dot
    destinationParent.appendChild(dot)
    const endRect = dot.getBoundingClientRect();
    const endX = endRect.left;
    const endY = endRect.top;

    const dx = (startX - endX) + "px";
    const dy = (startY - endY) + "px";
    console.table({startX, endX, dx,dy})
    dot.style.setProperty("--dx", dx)
    dot.style.setProperty("--dy", dy)
    dot.classList.add("mover");
    dot.addEventListener("animationend", () => {
        destinationParent.appendChild(dot)
        dot.classList.remove("mover")
    })
}
