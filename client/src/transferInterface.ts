import { RegisterCode } from "./registerAndMemoryUtilities";

export interface Transfer {
	start_mem?: string;
	start_reg?: RegisterCode;
	end_mem?: string;
	end_reg?: RegisterCode;
	value: string;
}
