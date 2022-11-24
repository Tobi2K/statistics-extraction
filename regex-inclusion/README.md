# Regular Expression Inclusion

Here you can run the code to find regular expressions included in each other.
This can be run using
``` python
python main.py
```

The file used for regular expression inclusion needs to contain a valid regular expression per line.
We refer to the rule ID, meaning the `line number - 1` in the rule containing file.
Furthermore, "including rule" refers to the rule that is tested as the rule containing others and "included rule" refers to the rule that is tested as the rule contained in another.

`main.py` has three optional parameters:
* `--begin`: The rule ID of the rule to start as the including rule (default: `0`)
* `--end`: The rule ID of the rule to end as the including rule (default: `-1`)
* `--path`: The path to the file containing the regular expressions (default: `./rMinus.txt`)

If `end < begin` or `end` is `-1`, then `end` is ignored. 

An example use is
```shell
python main.py --begin 10 --end 20 --path '../myRuleList.txt'
```

This checks the rules with ids between 10 and 20, against all rules in the file `myRuleList.txt`.
