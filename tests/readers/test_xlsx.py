import logging
import os
import time
from pathlib import Path
from unittest import TestCase, skipIf

from tests.common import fake

skip = False
try:
    import openpyxl
    from zhtools.io_tools.readers.xlsx import XlsxReader
except ImportError:
    logging.warning('openpyxl not install, skip...')
    skip = True


@skipIf(skip, 'openpyxl not install.')
class TestXlsxReader(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.filename = Path('/tmp') / Path(str(time.time()) + '.xlsx')
        wb = openpyxl.Workbook()
        ws = wb.active

        cls.data = []
        for _ in range(4):
            row = [fake.pyint() for _ in range(3)]
            cls.data.append(row)
            ws.append(row)

        wb.save(cls.filename)
        wb.close()

    @classmethod
    def tearDownClass(cls) -> None:
        os.remove(cls.filename)

    def test_read(self):
        with XlsxReader(self.filename) as f:
            data = f.read()

        self.assertEqual(data, self.data)

    def test_readlines(self):
        with XlsxReader(self.filename) as f:
            data = f.readlines()

        self.assertEqual(data, list(map(tuple, self.data)))

    def test_read_col(self):
        with XlsxReader(self.filename) as f:
            data = list(f.read_col(0))

        self.assertEqual(data, [i[0] for i in self.data])
