"""
CMPG111 - Practical 6.2: Weather Service
Reads rainfall data from rainfall_data.txt, calculates average rainfall,
identifies the city with the highest rainfall, and writes a summary file.
"""


def read_rainfall_data(filename):
    """Read city and rainfall pairs from the file."""
    cities = []
    rainfalls = []

    try:
        with open(filename, 'r') as file:
            lines = [line.strip() for line in file if line.strip()]

        if not lines:
            print("Error: The file is empty.")
            return None, None

        if len(lines) % 2 != 0:
            print("Error: Incorrect data format.")
            print("Each city must be followed by its rainfall value.")
            return None, None

        for i in range(0, len(lines), 2):
            city = lines[i]
            try:
                rainfall = float(lines[i + 1])
                cities.append(city)
                rainfalls.append(rainfall)
            except ValueError:
                print(f"Error: Invalid rainfall value '{lines[i + 1]}' for city '{city}'.")
                print("Rainfall must be a numeric value.")
                return None, None

    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        print("Please make sure 'rainfall_data.txt' exists in the current directory.")
        return None, None
    except PermissionError:
        print(f"Error: You do not have permission to read '{filename}'.")
        return None, None
    except Exception as e:
        print(f"An unexpected error occurred while reading the file: {e}")
        return None, None

    return cities, rainfalls


def calculate_statistics(cities, rainfalls):
    """Calculate average rainfall and find the city with the highest rainfall."""
    average = sum(rainfalls) / len(rainfalls)
    max_index = rainfalls.index(max(rainfalls))
    highest_city = cities[max_index]
    highest_rainfall = rainfalls[max_index]
    return average, highest_city, highest_rainfall


def display_results(cities, rainfalls, average, highest_city, highest_rainfall):
    """Display the results to the console."""
    print("=" * 45)
    print("         SOUTH AFRICAN RAINFALL DATA")
    print("=" * 45)
    for city, rain in zip(cities, rainfalls):
        print(f"  {city:<20} {rain:.1f} mm")
    print("-" * 45)
    print(f"  Average Rainfall:    {average:.2f} mm")
    print(f"  Highest Rainfall:    {highest_city} ({highest_rainfall:.1f} mm)")
    print("=" * 45)


def write_summary(filename, cities, rainfalls, average, highest_city, highest_rainfall):
    """Write the formatted summary to a text file."""
    try:
        with open(filename, 'w') as file:
            file.write("=" * 45 + "\n")
            file.write("      SOUTH AFRICAN RAINFALL SUMMARY\n")
            file.write("=" * 45 + "\n")
            for city, rain in zip(cities, rainfalls):
                file.write(f"  {city:<20} {rain:.1f} mm\n")
            file.write("-" * 45 + "\n")
            file.write(f"  Average Rainfall:    {average:.2f} mm\n")
            file.write(f"  Highest Rainfall:    {highest_city} ({highest_rainfall:.1f} mm)\n")
            file.write("=" * 45 + "\n")

        print(f"\nSummary successfully written to '{filename}'.")

    except PermissionError:
        print(f"Error: You do not have permission to write to '{filename}'.")
    except Exception as e:
        print(f"An unexpected error occurred while writing the summary: {e}")


def main():
    input_file = "rainfall_data.txt"
    output_file = "rainfall_summary.txt"

    cities, rainfalls = read_rainfall_data(input_file)

    if cities is None or rainfalls is None:
        return

    average, highest_city, highest_rainfall = calculate_statistics(cities, rainfalls)
    display_results(cities, rainfalls, average, highest_city, highest_rainfall)
    write_summary(output_file, cities, rainfalls, average, highest_city, highest_rainfall)


if __name__ == "__main__":
    main()
