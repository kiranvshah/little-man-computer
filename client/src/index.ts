import * as bootstrap from "bootstrap";
import {
	saveCode,
	checkCode,
	clearCode,
	assembleCode,
	step,
	run,
	loadExampleProgram,
} from "./buttonResponders.js";
import {
	animationsAreSwitchedOn,
	turnOffAnimations,
	turnOnAnimations,
} from "./animations.js";

// initialise tooltips
document
	.querySelectorAll('[data-bs-toggle="tooltip"]')
	.forEach(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));

// add event listeners
document.addEventListener("DOMContentLoaded", () => {
	// load assembly code if saved in URL query string
	const savedCode = new URLSearchParams(window.location.search).get("code");
	if (savedCode) {
		(
			document.getElementById(
				"uncompiledAssemblyTextarea",
			) as HTMLTextAreaElement
		).value = savedCode;
	}

	// add event listeners to buttons
	Object.entries({
		saveButton: saveCode,
		clearButton: clearCode,
		checkButton: checkCode,
		assembleButton: assembleCode,
		stepButton: step,
		runButton: run,
		loadExampleProgramButton: loadExampleProgram,
	}).forEach(([buttonId, listenerFunction]) => {
		(document.getElementById(buttonId) as HTMLButtonElement).addEventListener(
			"click",
			listenerFunction,
		);
	});

	const animationsSwitch = document.getElementById(
		"animationsSwitch",
	) as HTMLInputElement;
	// turn animation switch on/off as appropriate
	animationsSwitch.checked = animationsAreSwitchedOn();
	// add event listeners to animations switch
	animationsSwitch.addEventListener("change", () => {
		if (animationsSwitch.checked) {
			turnOnAnimations();
		} else {
			turnOffAnimations();
		}
	});
});
