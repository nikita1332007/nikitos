import pytest


from src.decorators import log


@log(filename=None)
def successful_function(x, y):
    return x + y


@log(filename=None)
def failing_function(x, y):
    return x / y


def test_successful_function(capsys):
    result = successful_function(3, 4)
    captured = capsys.readouterr()
    assert result == 7
    assert "successful_function ok" in captured.out


def test_failing_function(capsys):
    with pytest.raises(ZeroDivisionError):
        failing_function(1, 0)
    captured = capsys.readouterr()
    assert "failing_function error: ZeroDivisionError. Inputs: (1, 0), {}" in captured.out


def test_logging_to_file(tmpdir):
    log_file = tmpdir.join("test_log.txt")

    @log(filename=str(log_file))
    def file_function(x):
        return x * 2

    result = file_function(5)
    assert result == 10
    with open(log_file) as f:
        log_contents = f.read()
    assert "file_function ok" in log_contents


if __name__ == "__main__":
    pytest.main()
