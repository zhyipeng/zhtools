import abc
from typing import Any, Union

from zhtools.exceptions import ModuleRequired

try:
    from tqdm import tqdm
except ImportError:
    tqdm = lambda it: it


class XlsxExporterInterface(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def export(self,
               header: list[str],
               data: list[list[Any]],
               path: str) -> None:
        """
        :param header: excel headers
        :param data: exported data
        :param path: file path

        >>> h = ['ColA', 'ColB', 'ColC']
        >>> d = [[1, 2, 3], [2, 2, 3]]
        >>> XlsxExporterInterface().export(h, d, '/tmp/test.xlsx')
        """
        pass

    @abc.abstractmethod
    def export_dict(self,
                    header: dict[str, str],
                    data: list[dict[str, Any]],
                    path: str) -> None:
        """
        :param header: excel headers
        :param data: exported data
        :param path: file path

        >>> h = {'col1': 'ColA', 'col2': 'ColB', 'col3': 'ColC'}
        >>> d = [{'col1': 1, 'col2': 2, 'col3': 3}, {'col1': 2, 'col2': 2, 'col3': 4}]
        >>> XlsxExporterInterface().export_dict(h, d, '/tmp/test.xlsx')
        """
        pass


class XlsxExporter(XlsxExporterInterface):

    def _export(self, writer, header, data, path: str, sheetname: str = None):
        try:
            import openpyxl
        except ImportError:
            raise ModuleRequired('openpyxl', '3.0.6')

        wb = openpyxl.Workbook()
        ws = wb.active
        if sheetname:
            ws.title = sheetname

        writer(ws, header, data)
        wb.save(path)

    def export(self,
               header: list[str],
               data: list[list[Union[str, int, float]]],
               path: str,
               sheetname: str = None,
               ):
        self._export(self.write_sheet, header, data, path, sheetname)

    def export_dict(self,
                    header: dict[str, str],
                    data: list[dict[str, Union[str, int, float]]],
                    path: str,
                    sheetname: str = None):
        self._export(self.write_sheet2, header, data, path, sheetname)

    @staticmethod
    def write_sheet(ws,
                    header: list[str],
                    data: list[list[Union[str, int, float]]]):
        ws.append(header)
        for row in tqdm(data):
            ws.append(row)

    @staticmethod
    def write_sheet2(ws,
                     header: dict[str, str],
                     data: list[dict[str, Union[str, int, float]]]):
        ws.append(list(header.values()))
        for item in tqdm(data):
            ws.append([item.get(k, '') for k in header])
