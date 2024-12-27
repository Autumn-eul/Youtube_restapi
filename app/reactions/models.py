from django.db import models
from common.models import CommonModel

# User : Reaction => User : Reaction, Reaction, Reaction ... => 1 : N(FK)
# Video : Reaction => Video : Reaction, Reaction, Reaction ... => 1 : N(FK)
class Reaction(CommonModel):
    # user = models.Foreignkey(User) # Circular Import Error
    user = models.ForeignKey('users.User', on_delete = models.CASCADE)
    video = models.ForeignKey('videos.Video', on_delete = models.CASCADE)

    LIKE = 1
    DISLIKE = -1
    NO_REACTION = 0

    REACTION_CHOICES = (
        (LIKE, 'Like'),
        (DISLIKE, 'Dislike'),
        (NO_REACTION, 'No Reaction')
    )

    # LIKE(1), DISLIKE(-1), NO_REACTION(0)
    reaction = models.IntegerField(
        choices = REACTION_CHOICES,
        default = NO_REACTION
    )