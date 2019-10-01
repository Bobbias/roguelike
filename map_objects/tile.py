class Tile:
    """
    A tile on a map. It may or may not be blocked, and may or may not block sight.
    """
    def __iit__(self, blocked, block_sight=None):
        self.blocked = blocked

        if block_sight is None:
            block_sight = blocked

        self.block_sight
