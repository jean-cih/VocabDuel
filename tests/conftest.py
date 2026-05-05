import pytest
import tempfile

@pytest.fixture
def temp_dict_file():
    """create the temp file with dict"""

    content = """1. **apple** - яблоко
    2. **grape** - виноград
    3. **banana** - банан"""

    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
        temp_file.write(content)
        path = temp_file.name

    yield path
    os.unlink(path)


