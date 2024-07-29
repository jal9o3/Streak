# streak

Command line utility for tracking daily habits

Created using the [click](https://click.palletsprojects.com/en/8.1.x/) package.

## Setup

The recommended way of obtaining `streak` is 
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
  load    Load a backup of the data from a specified directory path.
  ls      List all registered habits.
  rm      Remove the specified habits.
  show    Show contents of ALL habit CSV files OR only a specified habit.
  track   Record the activity for a specified habit.
```

## Usage
As demonstrated in the previous section, you may check the help page using the
`--help` or `-h` options.
### Habit Tracking
You can record the observance of a habit through:
```
streak track "Your Habit"
```
If this is a new habit, streak will prompt for the creation of the habit in the
records. It will then proceed to increment the `intensity` of the habit, which
should represent how often you do a habit.
```
Habit 'Your Habit' does not exist. Create it? (y/n): y
Habit 'Your Habit' created succesfully.
Intensity for habit 'Your Habit' incremented for today.
```
Tracking existing habits will only output the last line.
### Listing Habit Streaks
You can see all your daily habit streaks through:
```
streak ls
```
The output should look like this:
```
Your habit streaks: 
        Example Habit A
                16 DAYS
        Example Habit B
                1 DAY
        Example Habit C
                2 DAYS
        Example Habit D
                500 DAYS
```
### Showing Habit Records
You can see more detailed records through:
```
streak show "Your Habit"
```
The output should be like this:
```
Your Habit
      date  intensity
2024-07-27          1
2024-07-28          4
```
To show all records:
```
streak show all
```
The output should be like this:
```

Example Habit A
      date  intensity
2024-07-27          5

==============================

Example Habit B
      date  intensity
2024-07-27          3

==============================

Example Habit C
      date  intensity
2024-07-28          1

==============================

Example Habit D
      date  intensity
2024-07-28          1

==============================

Example Habit E
      date  intensity
2024-07-27          1
2024-07-28          4

==============================

Example Habit F
      date  intensity
2024-07-28          3

==============================
```
### Removing Habits
You can remove habits through the `rm` command. For example:
```
streak rm "Your Habit" "Another Habit"
```
Output:
```
Remove 2 habit(s)? (y/n): y
Removed Your Habit
Removed Another Habit
```
You can specify as many habits to remove as you want. You may verify the updated
habit list using the `ls` or `show` commands.
### Backing Up Records
Backups could be created using the `backup` command:
```
streak backup ~/Documents/streak
```
You can replace `~/Documents/streak` with the location where you intend 
to store the backup. 
The command should output something similar to this:
```
Backup created at /home/user/Documents/streak/2024-07-28_18-15-01
```
### Restoring from Backup
Restore your backups using `load`.
```
streak load ~/Documents/streak/2024-07-28_16-48-24
```
Replace `~/Documents/streak/2024-07-28_16-48-24` with the path to your backup.
The output should be like this:
```
Loaded backup from /home/romlor/Documents/streak/2024-07-28_16-48-24 successfully.
```
You may verify the record restoration using the `ls` or `show` commands.