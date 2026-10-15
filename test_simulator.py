from scenario import Fault
from simulator import CONFIRM_CYCLES, NOMINAL, SAFE_MODE, Simulator


def run_cycles(simulator, count):
    for cycle in range(count):
        simulator.step(cycle)


def test_stays_nominal_without_fault():
    simulator = Simulator()
    run_cycles(simulator, 10)
    assert simulator.state == NOMINAL


def test_low_voltage_triggers_safe_mode():
    simulator = Simulator(Fault(cycle=0, sensor="battery_voltage", value=2.5))
    run_cycles(simulator, CONFIRM_CYCLES)
    assert simulator.state == SAFE_MODE


def test_large_attitude_error_triggers_safe_mode():
    simulator = Simulator(Fault(cycle=0, sensor="attitude_error_deg", value=60.0))
    run_cycles(simulator, CONFIRM_CYCLES)
    assert simulator.state == SAFE_MODE


def test_single_bad_cycle_is_ignored():
    simulator = Simulator(Fault(cycle=3, sensor="battery_voltage", value=2.5))
    run_cycles(simulator, 4)
    assert simulator.state == NOMINAL
