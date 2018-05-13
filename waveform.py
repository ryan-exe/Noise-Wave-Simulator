import sys
import os

def parse_arguments():
    """
    Parses command line arguments.

    Returns flags, file.
    """

    flags = {}
    file = False

    for arg in sys.argv[1:]:
        # Collects the flags given in the command line.
        if arg.startswith("--"):
            key, value = arg.strip("--").split("=")
            flags[key] = value
        else:
            # By storing all the flags, we should be left with the remaining arg as the filename.
            file = arg

    if not file:
        # If at this point file was not updated, then no filename was given.
        print("No score file specified.")
        exit()

    return (flags, file)


def parse_wave_file(instrument):
    """
    Takes the given instrument and produces the wave.
    The wave is stored as a dictionary, it's key the y axis, the values being the matrix.
    """
    wave = {}

    try:
        with open("./instruments/" + instrument) as wave_file:
            wave_lines = wave_file.read().splitlines()
            max_len = longest_wave_line(wave_lines)
            for line in wave_lines:
                y, xs = line.strip("\n").split("\t")
                # Pads all the matrix values to be the same length so that the wave can be manipulated.
                xs = xs.ljust(max_len, " ") 
                wave[int(y)] = list(xs)
            return wave
    except FileNotFoundError:
        # If the given instrument name given does not exist, an error is produced.
        print("Unknown source.")
        exit()

def parse_score_file(file):
    """
    Reads and cleans the score file. 
    The instrument and the resulting period (soundwave to be produced) are returned.
    """
    try:
        with open(file) as score:
            instrument = score.readline().strip("\n")
            period = score.readline().strip("\n")
            return (instrument, period)
    except FileNotFoundError:
        print("Invalid path to score file.")
        exit()

def print_wave(wave):
    """
    Prints the wave.
    """
    for y, xs in wave.items():
        if not is_empty_row(xs):
            print("{: d}:\t{}".format(y, "".join(xs)))


def is_empty_row(row):
    """
    This will only print the rows that are used. 
    For example if the piano stops at 5: before reaching it's highest sound of :6, it will not print :6.
    """
    is_empty = True
    for item in row:
        if item != " ":
            return False
    return True

def replace_character(wave, character):
    """
    This function replaces wave with the required character.
    """
    # Produces a copy of the wave with the new character so that the original is not altered. 
    new_wave = wave.copy()  
    for y, xs in new_wave.items():
        replaced_xs = []
        for x in xs:
            # If the space is not blank, replace the character.
            if x != " ":
               replaced_xs.append(character)
            else:
                replaced_xs.append(x)
        new_wave[y] = replaced_xs
    return new_wave # Returns the new wave that now has the correct character.


def get_character(flags):
    """
    Gets the character specified in flags. 
    If no character has been provided, a asterix is used by default.
    """
    if "character" in flags:
        return flags["character"][0]

    return "*"


def longest_wave_line(wave_lines):
    """
    Returns the longest line in the wave matrix. 
    This is required so that each line can be padded to create the full matrix.
    """
    longest = 0
    for wave in wave_lines:
        y, line = wave.split("\t")
        if len(line) > longest:
            longest = len(line)
    return longest


def manipulated_wave(channel, wave, character):
    """
    Manipulates the wave depending on the contents of the channel 
    """
    # Finds the height of the Y axis by decreament with a negative stepper
    ys = range(max(wave), min(wave) - 1, -1) 
    # Creates a blank wave so that the wave can be restarted at the correct length of the channel provided.
    blank_wave = create_blank_wave(wave, channel) 
    # Tracks the position on the x axis for the wave
    wave_x = 0 
    last_symbol = False

    for x, current_symbol in enumerate(channel):
        for y in ys:
            if current_symbol == '-' and last_symbol == '-':
                # Continues the silence.
                blank_wave[0][x] = character
            if current_symbol == '-' and last_symbol == '*':
                # Silences the wave back to 0.
                if character_y_position > 0:
                    # If the wave is above 0, prints y axis downwards.
                    while character_y_position > 0:
                        blank_wave[character_y_position-1][x] = character
                        character_y_position -= 1
                elif character_y_position < 0:
                    # If the wave is above 0, prints y axis upwards.
                    while character_y_position < 0:
                        blank_wave[character_y_position+1][x] = character
                        character_y_position += 1
                else:
                    # If the y position is already at 0, it just prints another character.
                    blank_wave[0][x] = character

            if current_symbol == '*' and last_symbol == '-':
                # Restarts the wave.
                wave_x = 0 # Resets the tracker
                blank_wave[0][x] = character # Begins the new clean wave.

            elif current_symbol == '*' and last_symbol == '*': 
                # Continues the wave from it's current Y position.
                character_y_position = get_character_y_position(wave, wave_x, character)
                blank_wave[character_y_position][x] = character

            else:
                blank_wave[0][x] = character
        # Increments the x axis tracker to ensure the wave is manipulated at the correct position.
        wave_x += 1 
        last_symbol = current_symbol
    return blank_wave

def get_character_y_position(wave, x, character):
    """
    Returns the y position of the character. 
    """
    wave_length = len(wave[0])
    # Determines where the character has been produced in the Y axis and returns the height of that character.
    for y in range(max(wave), min(wave) - 1, -1): 
        if wave[y][x % wave_length] == character: 
            return y

    return 'error' # Throw error if no character found.

def create_blank_wave(wave, channel):
    """
    Finds the length of the channel and produces a blank wave of that 
    length so that the wave can be restarted in the correct spot. 
    """
    blank_wave = {}
    wave_length = len(channel)
    for y in range(max(wave), min(wave) - 1, -1):
        blank_wave[y] = [' '] * wave_length
    return blank_wave

def main():
    """
    Runs all the functions in order and produces a printed wave.
    """
    flags, file = parse_arguments()
    instrument, channel_string = parse_score_file(file) # "piano", "[xxxxxxx]".
    channel = list(channel_string.strip("|")) #Produces channel in format similair to xxxxx-----.
    wave = parse_wave_file(instrument) # parse_wave_file("piano").
    character = get_character(flags) # Returns the character that has been set in a flag or returns the default *.
    character_wave = replace_character(wave, character) # Returns the wave with the new character in it.
    new_wave = manipulated_wave(channel, character_wave, character) # Reads the channel and produces the manipulated wave.
    print(instrument + ":") # Formatting to add the instrument and a colon above the wave/
    print_wave(new_wave) # The best line of all, prints the final wave.

if __name__ == "__main__":
    # Ensures that all the functions won't execute if this file is being imported in another file.
    main()
