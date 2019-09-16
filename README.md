HCP Common Psychopy Utils
==========================

1. Make sure you have the shared utilities available as a directory in your task, either by using git (preferred if available for updates) or by downloading the tarfile and expanding it:

```bash
    $ git submodule add https://github.com/kastman/hcpcommon.git
```

2. Import the module in a code component "Begin Experiment" at the begginning of a psychopy task.

``` python
    # In "Begin Experiment":
    import hcpcommon
```

3. Use the utilities where desired:

``` python
    # Check screen counts to nicely complain if only one display
    # screen is available:
    hcpcommon.checkScreenCount()

    # Import order counterbalancing file:
    order = 'A'  # Row Name, e.g. "H"
    month = 'Month 1'  # Column Name to choose, e.g. 'Rep 3'
    order_filename = 'conditions/12order_counterbalance.csv'
    stimlistnum = hcpcommon.choose_stimlist(
      order, month, order_filename)
    stims = glob('stimuli/List {}/*.png'.format(stimlistnum))
```

## Counterbalance Loading

For the paradigm of differing stim lists counterbalanced across returning months: assume you have a csv or excel formatted so that the months are listed across the top in columns and the orders are listed as rows:

|     | Month 1 | Month 2 | Month ... 12 |
| --- | ------- | ------- | ------------ |
| A   | 2       | 3       | 1            |
| G   | 1       | 2       | 3            |



Add code in a starting routine to a "Begin Experiment" block:

We assume you assign a participant's Order by appending `"_{Letter}"` to the session ID, and the current month through a variable in the experiment info.

The list to choose is returned by specifying the order, month, and counterbalance sheet (it's nothing special, just indexing a pandas dataframe).
