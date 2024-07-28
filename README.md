# streak

Command line utility for tracking daily habits

Created using the [click](https://click.palletsprojects.com/en/8.1.x/) package.

## Setup

The recommended way of obtaining streak is 
by cloning from the git repository.

```
git clone https://github.com/jal9o3/Streak.git
```

Then, `cd` into the cloned directory. 

### Creating an Environment
You may setup `virtualenv` as recommended 
by the [click documentation](https://click.palletsprojects.com/en/8.1.x/quickstart/#virtualenv).

Alternatively, you may utilize a [conda](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) environment.


### Installation
You can now install using `pip`.
```
python -m pip install --editable .
```

### Verification
You may verify that installation is successful by running:
```
streak --help
```
The output should be like this:
```
Usage: streak [OPTIONS] COMMAND [ARGS]...

  streak is a minimalist cli tool for tracking daily habits.

Options:
  -h, --help  Show this message and exit.

Commands:
  backup  Create a backup of all habit data at a specified directory path.
  list    List all registered habits.
  load    Load a backup of the data from a specified directory path.
  rm      Remove the specified habits.
  show    Show contents of ALL habit CSV files OR only a specified habit.
  track   Record the activity for a specified habit.
```