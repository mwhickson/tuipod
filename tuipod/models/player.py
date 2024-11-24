from tuipod.models.episode import Episode

class Player:
    """
    A minimal, abstract player stub for the podcast player.

    TODO: flesh this out...
    """

    def __init__(self, episode: Episode, position_seconds: int) -> None:
        """initialize a podcast player with the episode to play, and the current position/offset within the episode in seconds"""
        self.episode = episode
        self.position_seconds = position_seconds
