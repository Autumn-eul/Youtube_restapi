from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Video
from .serializers import VideoListSerializer, VideoDetailSerializer


# 1. VideoLost
# api/v1/videos
# [GET[]: 전체 비디오 목록 제외
# [post]: 새로운 비디오 생성
# [PUT], [DELETE]: X
class VideoList(APIView):
    def get(self, request):
        videos = Video.objects.all() # objects => QuerySet[Video, Video, Video ...]

        # objects -> Json (직렬화)
        serializer = VideoListSerializer(videos, many = True)

        return Response(serializer.data, status = status.HTTP_200_OK)

    def post(self, request):
        user_data = request.data # Json -> object (역직렬화)

        serializer = VideoListSerializer(data = user_data)

        if serializer.is_valid():
            serializer.save(user = request.user)
            return Response(serializer.data, status = status.HTTP_201_CREATED)

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


# 2. VideoDetail
# api/v1/videos/{video_id}
# [GET]: 특정 비디오 조회
# [POST]: X
# [PUT]: 특정 비디오 업데이트
# [DELETE]: 특정 비디오 삭제
class VideoDetail(APIView):
    def get(self, request, pk):
        try:
            video_obj = Video.objects.get(pk = pk)
        except Video.DoesNotExist:
            raise NotFound

        serializer = VideoDetailSerializer(video_obj)

        return Response(serializer.data, status = status.HTTP_200_OK)

    def put(self, request, pk):
        video_obj = Video.objects.get(pk = pk)
        user_data = request.data

        serializer = VideoDetailSerializer(video_obj, user_data)
        serializer.is_valid(raise_exception = True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request, pk):
        video_obj = Video.objects.get(pk = pk)
        video_obj.delete()

        return Response(status = status.HTTP_204_NO_CONTENT)

# 테스트 코드 실행
# docker-compose run --rm app sh -c "python manage.py test videos"