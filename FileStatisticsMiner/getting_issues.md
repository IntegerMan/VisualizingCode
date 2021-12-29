# Getting Issues

The best way of pulling issues seems to be using [GitHub's CLI](https://cli.github.com/) via a pair of commands:

```bash
gh auth login
gh issue list --limit 100000 --state all | tr '\t' ',' > issues.csv
```

This will create an `issues.csv` file that you can then use to analyze data.