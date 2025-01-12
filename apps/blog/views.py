import logging
from .models import Author, Blog
from .filters import BlogListingFilter
from .mixins import ValidateAuthorMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BlogCreateSerializer
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_403_FORBIDDEN
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from django_fsm import TransitionNotAllowed
from .serializers import BlogListSerializer

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
                title=validated_data.get("title"),
                content=validated_data.get("content"),
                author=author_obj
            )
        except Exception as e:
            logger.error(f'An error occurred while creating blog: {e}')
            return Response({'message': 'An error occurred!'}, status=HTTP_500_INTERNAL_SERVER_ERROR)

        # Successfully created the blog
        return Response({'message': 'Blog created successfully!'}, status=HTTP_201_CREATED)

class BlogListView(ListAPIView):
    filter_backends = [DjangoFilterBackend]
    filterset_class = BlogListingFilter
    serializer_class = BlogListSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user_obj = self.request.user
        author_obj = Author.objects.filter(user=user_obj).first()
        return Blog.objects.filter(author=author_obj)

class BlogDeleteView(ValidateAuthorMixin, APIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, blog_id, *args, **kwargs):
        try:
            _, blog_obj = self.validate_blog_author(request, blog_id)
            
            blog_obj.delete()
            return Response({'message': 'Blog deleted successfully!'}, status=HTTP_200_OK)
        except Blog.DoesNotExist as e:
            return Response({'message': str(e)}, status=HTTP_404_NOT_FOUND)
        except Author.DoesNotExist as e:
            return Response({'message': str(e)}, status=HTTP_400_BAD_REQUEST)
        except PermissionError as e:
            return Response({'message': str(e)}, status=HTTP_403_FORBIDDEN)
        except Exception as e:
            logger.error(f'An error occurred while deleting blog: {e}')
            return Response({'message': 'An error occurred!'}, status=HTTP_500_INTERNAL_SERVER_ERROR)
        

class BaseBlogUpdateView(ValidateAuthorMixin, APIView):
    def post(self, request, blog_id, *args, **kwargs):

        serializer = BlogCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        
        try:
            print('here 0')
            _, blog_obj = self.validate_blog_author(request, blog_id)
            print('here 1')

            blog_obj.title = validated_data.get('title')
            blog_obj.content = validated_data.get('content')
            
            return blog_obj, None

        except Author.DoesNotExist as e:
            return None, Response({'message': str(e)}, status=HTTP_400_BAD_REQUEST)
        except Blog.DoesNotExist as e:
            return None, Response({'message': str(e)}, status=HTTP_404_NOT_FOUND)
        except PermissionError as e:
            return None, Response({'message': str(e)}, status=HTTP_403_FORBIDDEN)
        except Exception as e:
            logger.error(f'An error occurred while updating blog: {e}')
            return None, Response({'message': 'An error occurred!'}, status=HTTP_500_INTERNAL_SERVER_ERROR)


class BlogPublishView(BaseBlogUpdateView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, blog_id, *args, **kwargs):
        
        blog_obj, error_response = super().post(request, blog_id)
        if error_response:
            return error_response
        
        try:
            if blog_obj.state == Blog.STATE_PUBLISHED:
                return Response({'message': 'Blog already published!'}, status=HTTP_400_BAD_REQUEST)

            blog_obj.publish_blog(request.user)
            blog_obj.save()
        except TransitionNotAllowed as e:
            logger.error(f'Blog with id {blog_id} cannot be published: {str(e)}')
            return Response({'message': 'Blog cannot be published!'}, status=HTTP_400_BAD_REQUEST)
        
        return Response({'message': 'Blog published successfully!'}, status=HTTP_200_OK)

class BlogEditView(BaseBlogUpdateView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, blog_id, *args, **kwargs):
        
        blog_obj, error_response = super().post(request, blog_id)
        if error_response:
            return error_response
        
        try:
            blog_obj.edit_blog(request.user)
            blog_obj.save()
        except TransitionNotAllowed as e:
            logger.error(f'Blog with id {blog_id} cannot be edited: {str(e)}')
            return Response({'message': 'Blog cannot be edited!'}, status=HTTP_400_BAD_REQUEST)

        return Response({'message': 'Blog edited successfully!'}, status=HTTP_200_OK)


class BlogArchiveView(ValidateAuthorMixin, APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, blog_id, *args, **kwargs):
        try:
            _, blog_obj = self.validate_blog_author(request, blog_id)
            
            if blog_obj.state == Blog.STATE_ARCHIVED:
                return Response({'message': 'Blog already archived!'}, status=HTTP_400_BAD_REQUEST)

            blog_obj.archive_blog()
            blog_obj.save()

        except Blog.DoesNotExist as e:
            return Response({'message': str(e)}, status=HTTP_404_NOT_FOUND)
        except Author.DoesNotExist as e:
            return Response({'message': str(e)}, status=HTTP_400_BAD_REQUEST)
        except PermissionError as e:
            return Response({'message': str(e)}, status=HTTP_403_FORBIDDEN)
        except TransitionNotAllowed as e:
            logger.error(f'Blog with id {blog_id} cannot be archived: {str(e)}')
            return Response({'message': 'Blog cannot be archived!'}, status=HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f'An error occurred while archiving blog: {e}')
            return Response({'message': 'An error occurred!'}, status=HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({'message': 'Blog archived successfully!'}, status=HTTP_200_OK)
