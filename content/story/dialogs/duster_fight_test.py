requirements = {'events' : ['E_0001', 'E_0002']}

content = """
self("Hi Yves. Do you want a practice battle?")
add_choice('fight', "Why not.")
add_choice('no_thanks', "No thanks")
show_choice()
"""

fight = """
self("Okay, let's go.")
fight(['self'])
self("That was good. Try harder.")
"""

no_thanks = """
player("No thanks.")
self("Come again, if you want to fight.")
"""

