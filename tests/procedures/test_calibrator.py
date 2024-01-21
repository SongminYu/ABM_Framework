import pytest
from tests.infra.config import cfg_for_calibrator
from Melodie import DataLoader
from tests.procedures.calibrator import CovidCalibrator, CovidModel, CovidScenario


class DFLoader(DataLoader):
    pass


@pytest.mark.timeout(15)
def test_calibrator():
    calibrator = CovidCalibrator(
        cfg_for_calibrator, CovidScenario, CovidModel, DFLoader, processors=2
    )
    calibrator.run()