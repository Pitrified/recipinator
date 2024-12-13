from loguru import logger as lg


def test():
    pass


def standard_mod(a=1) -> int:
    lg.success(f"Starting standard with {a=}")
    lg.info(f"Function standard called with arg: {a}")
    b = a + 1
    lg.debug(f"Function standard returning: {b}")
    return b


def another_mod(a=1) -> int:
    lg.success(f"Starting another with {a=}")
    lg.info(f"Function another called with arg: {a}")
    b = a + 1
    lg.debug(f"Function another returning: {b}")
    return b
