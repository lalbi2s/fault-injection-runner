import logging
from dataclasses import dataclass

from scenario import Scenario
from simulator import SAFE_MODE, Simulator

logger = logging.getLogger(__name__)


@dataclass
class Result:
    name: str
    passed: bool
    reason: str
    events: list[str]


def run_scenario(scenario: Scenario) -> Result:
    simulator = Simulator(scenario.fault)
    events = []
    safe_mode_cycle = None

    for cycle in range(scenario.total_cycles):
        if scenario.fault is not None and cycle == scenario.fault.cycle:
            events.append(
                f"cycle {cycle}: fault injected, "
                f"{scenario.fault.sensor} = {scenario.fault.value}"
            )

        previous_state = simulator.state
        simulator.step(cycle)

        if simulator.state != previous_state:
            events.append(
                f"cycle {cycle}: state changed "
                f"{previous_state} -> {simulator.state}"
            )
            if simulator.state == SAFE_MODE:
                safe_mode_cycle = cycle

    for event in events:
        logger.info("%s: %s", scenario.name, event)

    passed, reason = check_result(scenario, simulator.state, safe_mode_cycle)
    return Result(scenario.name, passed, reason, events)


def check_result(scenario, final_state, safe_mode_cycle):
    expected = scenario.expected

    if final_state != expected.final_state:
        return False, f"expected {expected.final_state}, got {final_state}"

    limit = expected.max_cycles_after_fault
    if limit is not None and scenario.fault is not None:
        delay = safe_mode_cycle - scenario.fault.cycle
        if delay > limit:
            return False, (
                f"SAFE_MODE reached {delay} cycles after the fault, "
                f"expected at most {limit}"
            )

    return True, "all expectations met"
