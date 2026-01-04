# 2026-01-03
Playing around with map chunks for the planetary surface (large)
# 2025-12-23
Considering how to identify items across worlds! Using "face", "iid", or ...?
# 2025-12-20
Implementing client/server command for picking up an item
# 2025-12-17
Server side has items, food parcels and backpack, and the client side can present them when
the player uses the pickup action. The presentation is using the menus - just have to find out
how to tell the server that one item has been picked up.
# 2025-12-13
Recorded the game with 500 NPCs from the community client running around in the starship
# 2025-12-08
Every actor from the community looks the same.
Added random face and skin colour on the client side.
Face and skin colour is communicated to the server side for other clients to use.
Ran community with 50 actors, client saw the community actors with different face and skin colours.
# 2025-12-07
Established the simple community client that controls a group of actors (10, 50, 100, 500)
# 2025-12-06
Established the actors list on the server side.
Field of sense (FOS) response now includes the actors within the FOS.
Test with several clients connected to the server at the same time, can see other actors.