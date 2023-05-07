# funes
Using a vector database to give generative AI long term memory

## Setup

This project uses Poetry. On a fresh install, run:

```sh

# install poetry
curl -sSL https://install.python-poetry.org | python3 -

# update
poetry self update

# enable completions
poetry completions bash >> ~/.bash_completion

# set virtualenv to be in project
poetry config virtualenvs.in-project true

# enter poetry shell
poetry shell

# install dependencies
poetry install

# at this point, you should be able to run the project
# either in shell, or through the pre-configured run configs
# in VSCode
```