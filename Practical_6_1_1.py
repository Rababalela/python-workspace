"""
CMPG111 - Practical 6.1: Music Concert
Reads artist names from concert_artist.txt, displays them, and counts total.
"""

def read_artists(filename):
    """Read and display artists from the given file."""
    try:
        with open(filename, 'r') as file:
            artists = [line.strip() for line in file if line.strip()]

        if not artists:
            print("The file is empty. No artists found.")
            return

        print("=" * 40)
        print("   ARTISTS PERFORMING AT THE CONCERT")
        print("=" * 40)

        for index, artist in enumerate(artists, start=1):
            print(f"  {index}. {artist}")

        print("=" * 40)
        print(f"  Total artists performing: {len(artists)}")
        print("=" * 40)

    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        print("Please make sure the file exists in the current directory.")
    except PermissionError:
        print(f"Error: You do not have permission to read '{filename}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def main():
    filename = "concert_artist.txt"
    read_artists(filename)


if __name__ == "__main__":
    main()
