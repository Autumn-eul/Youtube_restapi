from django.db import models
from common.models import CommonModel


class Comment(CommonModel):
    user = models.ForeignKey('users.User', on_delete = models.CASCADE)
    video = models.ForeignKey('videos.Video', on_delete = models.CASCADE)
    # 법적인 이슈랑 연결됨 (정보 통신 보호법 + Euro 6)

    content = models.TextField()
    like = models.PositiveIntegerField(default = 0)
    dislike = models.PositiveIntegerField(default = 0)

    # 대댓글
    # parent = models.ForeignKey('self', on_delete = models.CASCADE, null = True, blank = True)