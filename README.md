# scrumguard

scrumguard is a dead simple python3 RAG application for bookclub.

## Installation

Clone the repository, the top level dir of the repo is considered `$install_dir`.

scrumguard expects `tox` to be installed locally.

## Running

scrumguard depends on the env var `OPENAI_API_KEY` being set with a valid API key.

### Index Your Knowledge Base

Put whatever epubs and other documents you want indexed in the ingest path.
The ingest path is taken from the env var `INGEST_STORAGE_PATH` which defaults to `$install_dir/data/ingest_store` and is defined in `tox.ini`.

Note that this will consume credits from your `OPENAI_API_KEY`.

run the command: `tox -e index`

### Querying

Edit the queries document to have whatever queries you want to ask to your knowledge base. The queries document is taken from the env var `QUERIES_PATH` which defaults to `$install_dir/data/queries.json` and is defined in `tox.ini`. There are examples queries in `queries.json`.

Note that this will consume credits from your `OPENAI_API_KEY`.

run the command: `tox -e query`
