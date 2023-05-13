from math import sqrt


def _build_normalized_user_preference(options: list[dict], user: dict) -> list[float]:
    """
    Build a list of preferences for each user with preferences ranging from 0 to 1.
    """
    unNormalized = [sum([option[o] * user[o] for o in option.keys()])
                    for option in options]
    minimum = min(unNormalized)
    # Remove 0 dependence
    if minimum < 0:
        unNormalized = [u - minimum for u in unNormalized]
    total = sum(unNormalized)
    return [u / total for u in unNormalized]


def perform_votes(options: list[dict], users: list[dict]) -> list[int]:
    """
    Returns a list of the number of votes which each option received.
    """
    preferences = [_build_normalized_user_preference(
        options, user) for user in users]
    weighted_votes = [
        sum(sqrt(preferences[i][j]) for i in range(len(users)))
        for j in range(len(options))
    ]
    quadraticVotes = [v**2 for v in weighted_votes]
    return quadraticVotes

