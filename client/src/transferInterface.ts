import { RegisterCode } from "./registerAndMemoryUtilities";

/**
 * A transfer is a movement of data from one place in the LMC to another during the fetch-decode-execute cycle.
 * Multiple transfers will occur during each fetch-decode-execute cycle.
 */
export interface Transfer {
	start_mem?: string;
	start_reg?: RegisterCode;
	end_mem?: string;
	end_reg?: RegisterCode;
	value: string;
}
