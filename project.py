import retro

def display_games():
    strings = retro.data.list_games()
    substrings = ["Kirby"]
    filtered_strings = list(filter(lambda x: any(substring in x for substring in substrings), strings))
    print(filtered_strings)


display_games()
env = retro.make(game='KirbysDreamLand-GameBoy')
