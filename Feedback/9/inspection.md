Pair: amazing-squirrels \
Commit: 7657751628d22ebe5fe391e8aa1a2753765cffe \
Score: 173/275 \
Grader: Bhavya Lakhani

README Inspection - [0/30]
- ``-30`` for not adding README.md file in Bazaar\Server. Please write the description of server.py and proxy_player.py and explain the usage of it. Please add a README.md file in Bazaar\Client and explain the usage of client.py and player_json_interface.py in it.


Code Inspection - [138/210]

- ``-10``. You need a get name method to identify the proxy player. Or else you will have to go over the wire to always get it.
- ``-30``. Have a constructor in proxy_player.py and player_json_interface.py which takes in an input stream and an output stream, so you can mock the functionality. Imagine setting up a large infrastructure just to test the functionality for a method. You end up making socket connections just to the test the code. In order to avoid this you can have a constructor with inputstream and output stream and that can help you to mock. You can use this constructor in your test cases now.
- ``-12`` for not having test cases for Bazaar/Server/proxy_player.py and Bazaar/Client/player_json_interface.py. Honesty points are awarded for this.
- ``-20`` because the systems directly raise an exception if the connection fails and it crashes. Your system should ideally wait or shut down gracefully. For the System to shut down gracefully you can log the exception and show the user a meaningful message.

  Design Inspection - [35/35]
