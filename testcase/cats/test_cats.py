import urllib.parse
import os
import pytest
from common import requests
from common import case
class Test_Cats():

    def test_cats(self):
        t_data_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace('\\','/').split('testcase')[0] + 'testdata/cats/cats.yaml'

        p = case.Case()
        p.run_case(case_data_path=t_data_path)
if __name__ == '__main__':
    pytest.main('-vs','./test_cats.py')