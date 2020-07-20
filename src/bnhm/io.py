import json
from typing import Dict, Any
import pandas as pd
from folium import Map

from kedro.io import AbstractDataSet, DataSetError

from bnhm.espm_module import GBIFRequest


class GBIFRequestDataSet(AbstractDataSet):
    def __init__(self, scientific_name: str):
        self._scientific_name = scientific_name
        self._req = GBIFRequest()

    def _load(self) -> Any:
        pages = self._req.get_pages({
            'scientificName': self._scientific_name
        })
        records = [rec for page in pages for rec in page['results'] if rec.get('decimalLatitude')]
        records_df = pd.read_json(json.dumps(records))
        return records_df

    def _save(self, data: Any) -> None:
        raise DataSetError('This dataset is ReadOnly')

    def _describe(self) -> Dict[str, Any]:
        return dict(scientific_name=self._scientific_name)


class FoliumHTMLDataSet(AbstractDataSet):
    def __init__(self, filepath: str):
        self._filepath = filepath

    def _load(self) -> None:
        raise DataSetError('This dataset is WriteOnly')

    def _describe(self) -> Dict[str, Any]:
        return dict(filepath=self._filepath)

    def _save(self, data: Map) -> None:
        data.save(self._filepath)


class JSONDataSet(AbstractDataSet):
    def __init__(self, filepath: str):
        self._filepath = filepath

    def _load(self) -> Dict:
        with open(self._filepath, 'r') as f:
            return json.load(f)

    def _save(self, data: Dict) -> None:
        with open(self._filepath, 'w') as f:
            json.dump(data, f)

    def _describe(self) -> Dict[str, Any]:
        return dict(filepath=self._filepath)
