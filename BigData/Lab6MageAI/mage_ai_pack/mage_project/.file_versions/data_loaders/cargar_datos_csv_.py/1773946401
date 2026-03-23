import pandas as pd

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data(*args, **kwargs):
    df = pd.read_csv('/home/src/data/supermarket_sales_small.csv')
    return df


@test
def test_output(output, *args) -> None:
    assert output is not None, 'El output es None'
    assert len(output) > 0, 'El DataFrame está vacío'