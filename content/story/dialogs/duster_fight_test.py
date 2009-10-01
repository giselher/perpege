requirements = {'events' : ['E_0001', 'E_0002']}

content = """
self("Hi Yves. Do you want a practice battle?")
add_choice('fight', "Why not.")
add_choice('no_thanks', "No thanks")
show_choice()
"""

fight = """
self("Okay, let's go.")
set_fight_outcome('won', 'test_fight_won')
set_fight_outcome('lost', 'test_fight_lost')
fight(['self'])
"""

no_thanks = """
player("No thanks.")
self("Come again, if you want to fight.")
"""

test_fight_won = """
self("That was good. I am looking forward to fight you again.")
"""

test_fight_lost = """
self("Bad. You have to try harder and train more.")
"""