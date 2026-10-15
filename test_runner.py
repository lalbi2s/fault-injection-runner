import json
from pathlib import Path

from main import main
from runner import run_scenario
from scenario import Expected, Fault, Scenario, load_scenario

SCENARIOS = Path(__file__).parent / "scenarios"


def make_scenario(max_cycles_after_fault):
    return Scenario(
        name="test",
        description="",
        total_cycles=20,
        fault=Fault(cycle=5, sensor="battery_voltage", value=2.8),
        expected=Expected("SAFE_MODE", max_cycles_after_fault),
    )


def test_provided_scenarios_pass():
    for name in ("nominal", "voltage_drop", "attitude_loss"):
        result = run_scenario(load_scenario(SCENARIOS / f"{name}.json"))
        assert result.passed, f"{name}: {result.reason}"


def test_fails_when_safe_mode_arrives_too_late():
    # The simulator needs 1 cycle after the fault, so a limit of 0 cannot be met.
    result = run_scenario(make_scenario(max_cycles_after_fault=0))
    assert not result.passed
    assert "expected at most 0" in result.reason


def test_fails_when_safe_mode_is_expected_but_never_reached():
    scenario = Scenario(
        name="no_fault",
        description="",
        total_cycles=10,
        fault=None,
        expected=Expected("SAFE_MODE"),
    )
    result = run_scenario(scenario)
    assert not result.passed


def test_exit_code_is_0_when_all_scenarios_pass(tmp_path):
    report = tmp_path / "report.md"
    code = main([str(SCENARIOS / "nominal.json"), "--report", str(report)])
    assert code == 0
    assert report.exists()


def test_exit_code_is_1_when_a_scenario_fails(tmp_path):
    failing = tmp_path / "failing.json"
    failing.write_text(
        json.dumps(
            {
                "name": "too_late",
                "total_cycles": 20,
                "fault": {"cycle": 5, "sensor": "battery_voltage", "value": 2.8},
                "expected": {"final_state": "SAFE_MODE", "max_cycles_after_fault": 0},
            }
        )
    )
    report = tmp_path / "report.md"
    code = main([str(SCENARIOS / "nominal.json"), str(failing), "--report", str(report)])
    assert code == 1
