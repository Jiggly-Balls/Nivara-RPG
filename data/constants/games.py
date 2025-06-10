# 0 -> Killer
# 1 -> Victim
ROULETTE_KILL_TEXTS: tuple[str, ...] = (
    "{0} blew {1}'s head off!",
    "And that's a headshot! {1} was killed by {0}.",
    "{1} was destroyed by {0}!",
    "{1} killed by {0}. Now that's one step closer to winning!",
)

ROULETTE_MISS_TEXTS: tuple[str, ...] = (
    "{0} tried killing {1} but seems like their luck ran out.",
    "{0} tried killing {1} but they missed their shot!",
    "{0} pulled the trigger at {1} but the chamber was empty!",
)

ROULETTE_SUICIDE_KILL_TEXTS: tuple[str, ...] = (
    "{} decided to gamble it all and died to themself!",
    "Seems like {}'s luck ran out and died to themself!",
)

ROULETTE_SUICIDE_MISS_TEXTS: tuple[str, ...] = (
    "{} decided to gamble it all and survived! They get an extra round to shoot!",
    "{} tried to shoot themself and survived! They get an extra round to shoot!",
)
