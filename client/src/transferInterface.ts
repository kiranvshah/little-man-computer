export interface Transfer {
	start_mem?: string;
	start_reg?: "PC" | "ACC" | "IR" | "MAR" | "MDR" | "CARRY";
	end_mem?: string;
	end_reg?: "PC" | "ACC" | "IR" | "MAR" | "MDR" | "CARRY";
	value: string;
}
