# Options Studio — Lecture 1 revision

One studio, with the original exploration tools plus a guided Lecture 1 route.
The five lecture problems cover single options, protective puts, covered calls,
collars, and calls-based merger replication. They use the revised lecture's fixed
quotes. The original tools retain their separate model-generated market.

Each lecture problem includes an objective, the lecture problem, steps, hints,
worked solutions, applications, and a takeaway. Symbolic calculators accept
expressions such as `=max(ST-K,0)-premium`, with buttons for inserting symbols
and transferring results into answer boxes. Reset restores the lecture example.
Put-call parity and alternative put-based replication remain Lecture 2 topics.

## Run locally

Tested with Python 3.13.9. From this directory:

```shell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Upload

Upload the contents of this folder to the root of the studio's GitHub repository.
Include `.streamlit/config.toml`, even if your file browser hides dot folders.
Keep the files together; `app.py` is the Streamlit entry point.
The ZIP contains these same runtime files at its root. Extract it before upload.
Do not upload the whole textbook project or the `older_files` folder.
Use Python 3.13 for the tested dependency set. This package has not been deployed
or tested on the remote hosting service.

## Links from lecture or chapter

Append one of these suffixes to your deployed studio address:

| Problem | URL suffix |
|---|---|
| Single options | `?page=lecture1&case=single-options` |
| Protective put | `?page=lecture1&case=protective-put` |
| Covered call | `?page=lecture1&case=covered-call` |
| Collar | `?page=lecture1&case=collar` |
| Merger | `?page=lecture1&case=merger` |

The live address is not assigned by this package. Students may also select each
problem within the Lecture 1 menu. Practice solutions are intentionally visible;
this is an ungraded learning studio, not an assignment submission system.

## Maintenance

`lecture_engine.py` holds the lecture benchmarks and calculations;
`lecture_pages.py` holds its teaching interface. Other modules retain the
original exploration tools. Runtime dependencies are pinned to tested versions.
The sibling `Options_Studio_Lecture1_v1_validation` directory holds local tests
and the validation record; it is not needed on the hosting service.
