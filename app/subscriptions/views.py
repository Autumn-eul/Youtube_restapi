from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Subscription
from .serializers import SubscriptionSerializer
from rest_framework.exceptions import ValidationError
from django.db.models import Q
from django.contrib.auth import get_user_model
import logging
logger = logging.getLogger(__name__)

User = get_user_model()

class SubscriptionList(APIView):
    def post(self, request):
        logger.info(f"Authenticated user: {request.user}")
        logger.info(f"Request data: {request.data}")

        subscriber = request.user
        subscribed_to_id = request.data.get('subscribed_to')

        # 구독 대상 ID가 없는 경우
        if not subscribed_to_id:
            return Response({"error": "Missing 'subscribed_to' field."}, status = status.HTTP_400_BAD_REQUEST)

        # 본인을 구독하려는 경우
        logger.info(f"Checking if subscriber ({subscriber.id}) is subscribing to themselves ({subscribed_to_id})")
        if int(subscriber.id) == int(subscribed_to_id):  # 형 변환으로 값 비교 확실히
            return Response({"error": "You cannot subscribe to yourself."}, status = status.HTTP_400_BAD_REQUEST)

        # 중복 구독 처리
        if Subscription.objects.filter(subscriber = subscriber, subscribed_to_id = subscribed_to_id).exists():
            return Response({"error": "Subscription already exists."}, status = status.HTTP_400_BAD_REQUEST)

        # request.data를 복사한 데이터로 변경
        mutable_data = request.data.copy()
        mutable_data['subscriber'] = subscriber.id

        serializer = SubscriptionSerializer(data = mutable_data)

        try:
            serializer.is_valid(raise_exception = True)
            serializer.save(subscriber = subscriber)
            return Response(serializer.data, status = status.HTTP_201_CREATED)

        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            return Response(e.detail, status = status.HTTP_400_BAD_REQUEST)


class SubscriptionDetail(APIView):
    def delete(self, request, pk):
        logger.info(f"Delete request: subscriber={request.user}, subscribed_to={pk}")

        subscription = Subscription.objects.filter(subscriber=request.user, subscribed_to=pk).first()
        if not subscription:
            logger.info(f"Subscription not found for subscriber={request.user} and subscribed_to={pk}")
            return Response({"error": "Subscription not found."}, status=status.HTTP_404_NOT_FOUND)
        subscription.delete()
        logger.info(f"Deleted subscription for subscriber={request.user}, subscribed_to={pk}")
        return Response(status=status.HTTP_204_NO_CONTENT)

        # subscriber = request.user
        # subscription = get_object_or_404(Subscription, Q(subscriber = subscriber) & Q(subscribed_to = pk))
        # subscription.delete()
        # logger.info(f"Deleting subscription for subscriber: {subscriber}, subscribed_to: {pk}")
        #
        # return Response(status = status.HTTP_204_NO_CONTENT)