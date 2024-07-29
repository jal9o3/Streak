import click
import pandas as pd
import os
import shutil
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

# Path to the directory where habit CSV files will be stored
HABIT_DIR = str(Path.home().expanduser()) + "/streak"

if not os.path.exists(HABIT_DIR):
    os.makedirs(HABIT_DIR)

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """
    streak is a minimalist cli tool for tracking daily habits.
    """
    pass

@cli.command()
@click.argument("habit_name")
def track(habit_name):
    """
    Record the activity for a specified habit.
    """
    habit_csv = os.path.join(HABIT_DIR, f"{habit_name}.csv")

    if not os.path.exists(habit_csv):

        user_response = input(
            f"Habit '{habit_name}' does not exist. Create it? (y/n): ").lower()
        if user_response in ["y", "yes"]:
            # Create a new CSV file for the habit
            df = pd.DataFrame(columns=["date", "intensity"])
            df.to_csv(habit_csv, index=False)
            click.echo(f"Habit '{habit_name}' created succesfully.")
        else:
            click.echo(f"Habit '{habit_name}' not created.")
            return

    # Get the current date
    today = pd.Timestamp.now().strftime("%Y-%m-%d")
    # Read the appropriate CSV
    df = pd.read_csv(habit_csv)

    # Check if today's date exists in the DataFrame
    if today not in df["date"].values:
        # Create a new row with today's date and initial intensity value
        new_row = {"date": today, "intensity": 0}  # Set initial intensity to 0
        df = df._append(new_row, ignore_index=True)

    # Increment intensity for today's date
    df.loc[df["date"] == today, "intensity"] = df["intensity"] + 1
    df.to_csv(habit_csv, index=False)

    click.echo(f"Intensity for habit '{habit_name}' incremented for today.")

@cli.command()
@click.argument("habit_name")
def show(habit_name):
    """
    Show contents of ALL habit CSV files OR only a specified habit.
    """
    if habit_name == "all":
        for filename in os.listdir(HABIT_DIR):
            if filename.endswith(".csv"):
                habit_name = os.path.splitext(filename)[0]
                csv_path = os.path.join(HABIT_DIR, filename)
                df = pd.read_csv(csv_path)
                click.echo(f"\n{habit_name}")
                click.echo(df.to_string(index=False))
                click.echo("\n" + "=" * 30)
    
    else:
        csv_path = os.path.join(HABIT_DIR, f"{habit_name}.csv")
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            click.echo(f"\n{habit_name}")
            click.echo(df.to_string(index=False))
            click.echo("\n")
        else:
            click.echo(f"Habit '{habit_name}' not found.")

def calculate_streak(df):
    logging.basicConfig(level=logging.FATAL)
    logger.debug(f"Rows: {df.shape[0]}")

    # Initialize streak counter
    streak = 0

    # Convert 'date' column to datetime objects
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
    
    # Get today's date
    today = pd.to_datetime('today').normalize()
    logger.debug(f"Today: {today}")
    logger.debug(f"Date Values: {df['date'].values}")

    for i, value in enumerate(df['date'].values):
        # Check if there's an entry for today
        if today in df['date'].values:
            streak += 1
        # Handle if current date is not yet recorded
        elif today not in df['date'].values and i == 0:
            # Get yesterday's date
            today -= pd.Timedelta("1 day")
            if today in df['date'].values:
                streak += 1
                continue
        elif i > 0: # If missing entry is not current date
            streak = 0
        
        # Get yesterday's date
        today -= pd.Timedelta("1 day")
        

    return streak

@cli.command()
def ls():
    """List all registered habits."""
    click.echo("Your habit streaks: ")
    for filename in os.listdir(HABIT_DIR):
        if filename.endswith(".csv"):
            habit_name = os.path.splitext(filename)[0]
            click.echo(f"\t{habit_name}")
            csv_path = os.path.join(HABIT_DIR, filename)
            df = pd.read_csv(csv_path)
            streak = calculate_streak(df)
            click.echo(f"\t\t{streak} DAY", nl=False)
            # Handle when streak is only one day
            if streak == 1:
                click.echo()
            else:
                click.echo("S")

@cli.command()
@click.argument('habits', nargs=-1)
def rm(habits):
    """Remove the specified habits."""
    user_response = input(
            f"Remove {len(habits)} habit(s)? (y/n): ").lower()
    if user_response in ["y", "yes"]:
        for habit in habits:
            csv_file = os.path.join(HABIT_DIR, f"{habit}.csv")
            if os.path.exists(csv_file):
                os.remove(csv_file)
                click.echo(f"Removed {habit}")
            else:
                click.echo(f"{habit} does not exist.")
    else:
        click.echo("Removal cancelled.")
        return

@cli.command()
@click.argument("path")
def backup(path): 
    """
    Create a backup of all habit data at a specified directory path.
    """
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
    backup_dir_name = f"{path}/{formatted_datetime}"
    shutil.copytree(HABIT_DIR, backup_dir_name)
    click.echo(f"Backup created at {backup_dir_name}")

@cli.command()
@click.argument("path")
def load(path): 
    """
    Load a backup of the data from a specified directory path.
    """
    # Verify that the backup format is correct.
    try:
        if datetime.strptime(path.split("/")[-1], "%Y-%m-%d_%H-%M-%S"):
            # Remove all the currently stored data
            shutil.rmtree(HABIT_DIR)
            # Copy contents from the backup directory to the active HABIT_DIR
            shutil.copytree(path, HABIT_DIR, dirs_exist_ok=True)
            click.echo(f"Loaded backup from {path} successfully.")
    except ValueError:
        click.echo("Invalid backup path format. Please provide a valid format.")

if __name__ == "__main__":
    cli()

