# fault-injection-runner

A small command-line test bench that simulates a flight scenario, injects a fault and checks that the system switches to SAFE_MODE within the expected time. Time is counted in simulated cycles, so runs are fast and reproducible.

## Stack

- Python 3.12
- Standard library only (dataclasses, argparse, json, logging)
- pytest for the tests

## Installation and usage

```
python3.12 -m venv .venv
source .venv/bin/activate
pip install pytest
```

Run one or more scenarios:

```
python main.py scenarios/nominal.json scenarios/voltage_drop.json scenarios/attitude_loss.json
```

Options:

- `--report PATH` sets the Markdown report path (default `report.md`)
- `--verbose` logs events while the scenario runs

The program exits with code 0 if all scenarios pass and 1 if at least one fails.

Run the tests:

```
python -m pytest
```

## Example

```
$ python main.py scenarios/voltage_drop.json
[PASS] voltage_drop: all expectations met
    cycle 5: fault injected, battery_voltage = 2.8
    cycle 6: state changed NOMINAL -> SAFE_MODE

Summary: 1 passed, 0 failed
```

## How it works

- `simulator.py` holds the sensors and the state machine. The system goes to SAFE_MODE when the battery voltage is below 3.3 V or the attitude error is above 20 degrees for 2 cycles in a row.
- `scenario.py` loads a scenario from JSON: the fault (sensor, value, cycle) and the expected result.
- `runner.py` plays a scenario cycle by cycle and checks the result.
- `report.py` writes the console output and the Markdown report.

A scenario file looks like this:

```json
{
  "name": "voltage_drop",
  "description": "Battery voltage falls below the minimum at cycle 5.",
  "total_cycles": 20,
  "fault": {"cycle": 5, "sensor": "battery_voltage", "value": 2.8},
  "expected": {"final_state": "SAFE_MODE", "max_cycles_after_fault": 2}
}
```

## Ideas for improvement

- More fault types (sensor noise, stuck value, gradual drift)
- Several faults in one scenario
- A way to return from SAFE_MODE to NOMINAL
- JUnit XML output for continuous integration
