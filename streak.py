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
    """Show contents of all habit CSV files or a specific habit."""
    if habit_name == "all":
        for filename in os.listdir(HABIT_DIR):
            if filename.endswith(".csv"):
                habit_name = os.path.splitext(filename)[0]
                csv_path = os.path.join(HABIT_DIR, filename)
                df = pd.read_csv(csv_path)
                click.echo(f"Habit: {habit_name}")
                click.echo(df.to_string(index=False))
                click.echo("\n" + "=" * 30)
    
    else:
        csv_path = os.path.join(HABIT_DIR, f"{habit_name}.csv")
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            click.echo(f"Habit: {habit_name}")
            click.echo(df.to_string(index=False))
        else:
            click.echo(f"Habit '{habit_name}' not found.")

if __name__ == "__main__":
    if not os.path.exists(HABIT_DIR):
        os.makedirs(HABIT_DIR)
    cli()