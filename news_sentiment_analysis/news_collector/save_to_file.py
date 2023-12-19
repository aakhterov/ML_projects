import pyarrow as pa
import pyarrow.parquet as pq
import pandas as pd
from typing import List
from datetime import datetime
from collections import OrderedDict

from interfaces import Saver


class SaveToFile(Saver):
    '''
    TODO
    '''

    def save(self, path: str, data: List[None|OrderedDict], format: str):
        filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + "." + format
        path_file = path + filename
        if format == 'csv':
          self.__to_csv(path_file, data)
        elif format == 'parquet':
            self.__to_parquet(path_file, data)
        else:
            raise ValueError("Format parameter must be in ['csv', 'parquet']")
    
    def __to_csv(self, path: str, data: List[None|OrderedDict]):
        '''
        TODO
        :return:
        '''
        if data:
            headers = list(data[0].keys())
            df = pd.DataFrame.from_records(data)
            df.replace('\n', ' ', regex=True, inplace=True)
            df.replace(';', ',', regex=True, inplace=True)
            df.to_csv(path, sep=';', header=headers, index=False)

    def __to_parquet(self, path: str, data: List[None|OrderedDict]):
        '''
        TODO
        :return:
        '''
        if data:
            # df = pd.DataFrame.from_records(data)
            table = pa.Table.from_pylist(mapping=data)
            pq.write_table(table, path)
