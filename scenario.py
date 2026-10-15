import json
from dataclasses import dataclass

SENSORS = ("battery_voltage", "attitude_error_deg")


@dataclass
class Fault:
    cycle: int
    sensor: str
    value: float


@dataclass
class Expected:
    final_state: str
    max_cycles_after_fault: int | None = None


@dataclass
class Scenario:
    name: str
    description: str
    total_cycles: int
    fault: Fault | None
    expected: Expected


def load_scenario(path: str) -> Scenario:
    with open(path, encoding="utf-8") as file:
        data = json.load(file)

    fault = None
    if data.get("fault") is not None:
        fault = Fault(**data["fault"])
        if fault.sensor not in SENSORS:
            raise ValueError(f"{path}: unknown sensor '{fault.sensor}'")

    return Scenario(
        name=data["name"],
        description=data.get("description", ""),
        total_cycles=data["total_cycles"],
        fault=fault,
        expected=Expected(**data["expected"]),
    )
