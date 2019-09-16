import pandas as pd
from numpy import inf


# Test Using First Order
def choose_order(sessionid):
    bad_sessionid_msg = 'Session ID ending with "_{Letter}" required to choose stimuli list.'
    assert len(sessionid), bad_sessionid_msg
    order_letter = sessionid[-2:]
    assert order_letter[0] == '_', bad_sessionid_msg
    return order_letter[-1]


def choose_stimlist(order_id, col_id, orderfile, **options):
    """Verify a counterbalance sheet and choose a stim list order.

        order_id: Row Index  ('B')
        col_id: Column Index ('Month 2' or 'Rep 3')
        orderfile: Path to counterbalance csv file
        expected_shape: Expected array shape
        max_value: Maximum value for any list
    """
    if orderfile.endswith('.xlsx'):
        reader = read_stimlist_excel
        reader_options = {'sheet_name': options.get('sheet_name')}
    elif orderfile.endswith('.csv'):
        reader = read_stimlist_csv
        reader_options = {}
    else:
        raise ValueError('orderfile must be either CSV or XLSX')

    order_df = reader(orderfile, **reader_options)

    # Basic sanity checks for the dataframe
    validate_frame(order_df, order_id, col_id, **options)

    # All that for this: Grab the selected cell in the df
    listnum = order_df.loc[order_id, col_id].astype(int)

    # Ensure the selected list number value is valid
    max_value = options.get('max_value', None)
    if max_value:
        max_msg = 'Only lists {} and under are valid for this task.'.format(
            max_value)
        assert listnum <= max_value, max_msg

    # Everything was sane, return the selected list value
    return listnum


def read_stimlist_excel(orderfile=None, sheet_name=None):
    if not orderfile:
        orderfile = 'conditions/Month_By_Order_STAR.xlsx'
    if not sheet_name:
        sheet_name = '6 orders but given monthly'
    return pd.read_excel(orderfile, sheet_name=sheet_name)


def read_stimlist_csv(orderfile=None):
    """
    Load a CSV with assumed defaults.
    """
    if not orderfile:
        orderfile = 'conditions/Month_By_Order_STAR_6orders.csv'

    # Read the Dataframe
    return pd.read_csv(orderfile, index_col=0)


def validate_frame(df, order_id, col_id, expected_shape=(12, 12),
                   max_value=12):
    """Sanity checks for the counterbalance format.


    For the paradigm of differing stim lists counterbalanced across
    returning months: assume you have a csv or excel formatted so that the
    months or reps are listed across the top in columns and the orders are
    listed as rows:

    |     | Month 1 | Month 2 | Month ... 12 |
    | --- | ------- | ------- | ------------ |
    | A   | 2       | 3       | 1            |
    | B   | 3       | 1       | 4            |
    | ... | ...     | ...     | ...          |
    | G   | 1       | 2       | 3            |

    """

    # Check Matrix Shape
    expected_msg = 'Dataframe shape should be {}, was {}'.format(
        expected_shape, df.shape)
    assert df.shape == expected_shape, expected_msg

    # Check Column (Month / Rep) Index
    col_msg = '{} not found in columns: {}.'.format(col_id, list(
        df.columns)) + ' Maybe check your spelling?'
    assert col_id in df.columns, col_msg

    # Check Row Id
    order_msg = '{} not found in rows: {}.'.format(order_id, list(
        df.index)) + 'Maybe check your spelling?'
    assert order_id in df.index
