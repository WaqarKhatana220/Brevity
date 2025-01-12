import logging
from .models import Author, Blog

logger = logging.getLogger('django')

class ValidateAuthorMixin:
    def validate_blog_author(self, request, blog_id):
        user_obj = request.user
        author_obj = Author.objects.filter(user=user_obj).first()
        blog_obj = Blog.objects.filter(id=blog_id).first()
        
        if not author_obj:
            logger.error(f'Author not found for user {request.user.username}')
            raise Author.DoesNotExist("Author does not exist")
        
        if not blog_obj:
            logger.error(f'Blog with id {blog_id} not found')
            raise Blog.DoesNotExist("Blog does not exist")
        
        if not blog_obj.is_author(author_obj):
            logger.error('User does not have permission for this action')
            raise PermissionError("Permission denied!")
                
        return author_obj, blog_obj