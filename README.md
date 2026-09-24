# Options Studio — integrated version 2

## Upload and Python version

Use **Python 3.13** in Streamlit deployment Advanced settings. This build was
tested on Python 3.13.9 with the versions pinned in requirements.txt. Python 3.14
is not the tested environment and caused the reported PyArrow build failure.
If the existing deployment uses 3.14, select 3.13 when recreating the deployment.

Upload all files in this folder into the app repository, including
`.streamlit/config.toml`. Keep `app.py` as the entry point. If using the ZIP,
extract it first and upload its contents, not the ZIP itself. There are no new
dependencies compared with version 1. Do not upload the textbook workspace,
older_files, homework, or the separate validation folder.

## Changes

- Removed the separate Lecture 1 examples navigation section.
- Basics opens with the lecture call problem, then the original single-position
  exploration. Payoff, profit, and break-even have separate checked answer boxes.
  The shared calculator has a destination selector; enter one expression at a time.
- Guided applications offers protective put, covered call, and collar cases,
  alongside Additional applications, which retains the original four case tabs.
- Replication problem sets includes the supplied-quote lecture merger problem
  alongside all original problems and the custom payout laboratory.
- Strategy builder, strategy design problems, sensitivity analysis, and the
  knowledge bank remain available. Fixed lecture quotes and model-generated
  exploration prices are kept separate and labeled.
- Each integrated example has a reset, hints, worked solution, and takeaway.

## Direct links

Append these suffixes to the deployed app address:

| Example | Suffix |
|---|---|
| Single options | `?page=basics&case=single-options` |
| Protective put | `?page=applications&case=protective-put` |
| Covered call | `?page=applications&case=covered-call` |
| Collar | `?page=applications&case=collar` |
| Merger | `?page=replication&case=merger` |

Old `?page=lecture1&case=...` links also open the appropriate integrated section.
Public hosting has not been performed or verified for this version.

## Local use

```
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

For local tests, copy the sibling validation folder's `tests` directory into this
folder, install pytest==8.4.2, then run `python -m pytest tests -q`.
