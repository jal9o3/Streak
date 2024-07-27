import click
import pandas as pd
import os

# Path to the directory where habit CSV files will be stored
HABIT_DIR = "habits"

@click.group()
def cli():
    pass

@cli.command()
@click.argument("habit_name")
def track(habit_name):
    """
    Track habit intensity for a given habit.
    """
    habit_csv = os.path.join(HABIT_DIR, f"{habit_name}.csv")

    if not os.path.exists(habit_csv):
        # Create a new CSV file for the habit
        df = pd.DataFrame(columns=["date", "intensity"])
        df.to_csv(habit_csv, index=False)

    # Increment intensity for today's date
    today = pd.Timestamp.now().strftime("%Y-%m-%d")
    df = pd.read_csv(habit_csv)
    # TODO: make sure there is an entry for today's date
    # Check if today's date exists in the DataFrame
    if today not in df["date"].values:
        # Create a new row with today's date and initial intensity value
        new_row = {"date": today, "intensity": 0}  # You can adjust the initial value as needed
        df = df._append(new_row, ignore_index=True)


    df.loc[df["date"] == today, "intensity"] = df["intensity"] + 1
    df.to_csv(habit_csv, index=False)

    click.echo(f"Intensity for habit '{habit_name}' incremented for today.")

if __name__ == "__main__":
    if not os.path.exists(HABIT_DIR):
        os.makedirs(HABIT_DIR)
    cli()