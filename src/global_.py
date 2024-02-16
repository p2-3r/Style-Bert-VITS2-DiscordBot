import data as f_data

listen_channel = {}
play_waitlist = {}
prefix = f_data.read()["settings"]["prefix"]
read_limit = f_data.read()["settings"]["read_limit"]
pre_joinvoice = False