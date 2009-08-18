requirements = {'events': ['E_0001']}

content = """
self("Hi Yves, how do you do?")
player("Hi Duster. Well, not really good. The game sucks.")
self("Why this?")
add_choice('code_sucks', "Because the code sucks.")
add_choice('graphic_sucks', "Because the graphics sucks.")
add_choice('nevermind', "Nevermind")
show_choice()
"""

code_sucks = """
player("Because the code sucks.")
self("I will talk with Giselher about this problem. Maybe he can solve your problems.")
goto('end')
"""

graphic_sucks = """
player("Because the graphic sucks.")
self("Okay, i will talk with James. Maybe he can make the graphics as you imagine.")
goto('end')
"""

nevermind = """
player("Nevermind.")
self("Okey.")
goto('end')
"""

end = """
player("I am going now.")
self("See ya.")
set('event', 'E_0002')
"""

