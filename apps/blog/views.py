import logging
from .models import Author, Blog
from apps.users.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BlogCreateSerializer
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR

logger = logging.getLogger('django')

class BlogCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):

        serializer = BlogCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        
        try:
            user_obj = request.user

            author_obj, created = Author.objects.get_or_create(user=user_obj)
            if created:
                logger.info(f'New author record created for user {user_obj.username}')


            Blog.objects.create(
                title=validated_data.get('title'),
                content=validated_data.get('content'),
                author=author_obj
            )
        except Exception as e:
            logger.error(f'An error occurred while creating blog: {e}')
            return Response({'message': 'An error occurred!'}, status=HTTP_500_INTERNAL_SERVER_ERROR)

        # Successfully created the blog
        return Response({'message': 'Blog created successfully!'}, status=HTTP_201_CREATED)
