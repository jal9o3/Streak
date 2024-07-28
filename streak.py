import click
import pandas as pd
import os
import shutil
from datetime import datetime

# Path to the directory where habit CSV files will be stored
HABIT_DIR = "habits"

@click.group()
def cli():
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
            f"Habit {habit_name} does not exist. Create it? (y/n): ").lower()
        if user_response in ["y", "yes"]:
            # Create a new CSV file for the habit
            df = pd.DataFrame(columns=["date", "intensity"])
            df.to_csv(habit_csv, index=False)
            click.echo(f"Habit {habit_name} created succesfully.")
        else:
            click.echo(f"Habit {habit_name} not created.")
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

@cli.command()
def list():
    """List all registered habits."""
    click.echo("Your habits: ")
    for filename in os.listdir(HABIT_DIR):
        if filename.endswith(".csv"):
            habit_name = os.path.splitext(filename)[0]
            click.echo(f"\t{habit_name}")

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
    if not os.path.exists(HABIT_DIR):
        os.makedirs(HABIT_DIR)
    cli()

