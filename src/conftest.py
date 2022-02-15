from baseline import tests


def pytest_configure(config):
    tests.IS_PYTEST_RUNNING = True
