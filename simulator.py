from scenario import Fault

NOMINAL = "NOMINAL"
SAFE_MODE = "SAFE_MODE"

NOMINAL_VOLTAGE = 4.0
NOMINAL_ATTITUDE_ERROR = 1.0

MIN_VOLTAGE = 3.3
MAX_ATTITUDE_ERROR = 20.0

# A reading must be bad for this many cycles in a row, so one glitch is ignored.
CONFIRM_CYCLES = 2


class Simulator:
    def __init__(self, fault: Fault | None = None):
        self.fault = fault
        self.state = NOMINAL
        self.bad_cycles = 0

    def read_sensors(self, cycle: int) -> dict:
        readings = {
            "battery_voltage": NOMINAL_VOLTAGE,
            "attitude_error_deg": NOMINAL_ATTITUDE_ERROR,
        }
        if self.fault is not None and cycle >= self.fault.cycle:
            readings[self.fault.sensor] = self.fault.value
        return readings

    def step(self, cycle: int) -> None:
        readings = self.read_sensors(cycle)
        is_bad = (
            readings["battery_voltage"] < MIN_VOLTAGE
            or readings["attitude_error_deg"] > MAX_ATTITUDE_ERROR
        )

        if is_bad:
            self.bad_cycles += 1
        else:
            self.bad_cycles = 0

        # SAFE_MODE is final: the system never goes back to NOMINAL by itself.
        if self.bad_cycles >= CONFIRM_CYCLES:
            self.state = SAFE_MODE
