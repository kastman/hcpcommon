import pandas as pd


# Test Using First Order
def choose_order(sessionid):
    bad_sessionid_msg = 'Session ID ending with "_{Letter}" required to choose stimuli list.'
    assert len(sessionid), bad_sessionid_msg
    order_letter = sessionid[-2:]
    assert order_letter[0] == '_', bad_sessionid_msg
    return order_letter[-1]


def choose_stimlist(order, month_num, orderfile, sheet_name=None):
    if orderfile.endswith('.xlsx'):
        return choose_stimlist_excel(order, month_num, orderfile, sheet_name)
    elif orderfile.endswith('.csv'):
        return choose_stimlist_csv(order, month_num, orderfile)
    else:
        raise ValueError('orderfile must be either CSV or XLSX')


def choose_stimlist_excel(order, month_num, orderfile=None, sheet_name=None):
    if not orderfile:
        orderfile = 'conditions/Month_By_Order_STAR.xlsx'
    if not sheet_name:
        sheet_name = '6 orders but given monthly'
    order_df = pd.read_excel(orderfile, sheet_name=sheet_name)
    assert order_df.shape == (12, 12)
    return order_df.loc[order, 'Month {}'.format(month_num)]


def choose_stimlist_csv(order, month_num, orderfile=None):
    if not orderfile:
        orderfile = 'conditions/Month_By_Order_STAR_6orders.csv'
    order_df = pd.read_csv(orderfile, index_col=0)
    assert order_df.shape == (
        12, 12), 'Dataframe shape should be (12, 12), was {}'.format(df.shape)
    listnum = order_df.loc[order, 'Month {}'.format(month_num)].astype(int)
    assert listnum <= 6, 'Only lists 6 and under are valid for this task.'
    return listnum
