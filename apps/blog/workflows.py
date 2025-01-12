import logging
from django.db import models
from django_fsm import transition, FSMField
from ..constants import DRAFT, PUBLISHED, EDITED, ARCHIVED

logger = logging.getLogger('django')

class BlogWorkflow(models.Model):
    STATE_DRAFT = DRAFT
    STATE_PUBLISHED = PUBLISHED
    STATE_EDITED = EDITED
    STATE_ARCHIVED = ARCHIVED
    
    STATE_CHOICES = (
        (STATE_DRAFT, 'Draft'),
        (STATE_PUBLISHED, 'Published'),
        (STATE_EDITED , 'Edited'),
        (STATE_ARCHIVED, 'Archived')
    )
    
    state = FSMField(choices=STATE_CHOICES, default=STATE_DRAFT)
    
    class Meta:
        abstract = True
    
    @transition(field=state, source=STATE_DRAFT, target=STATE_PUBLISHED)
    def publish_blog(self, user):
        self.create_change_log(self.state, self.STATE_PUBLISHED, user)
        logger.info(f'Blog post with id {self.id} has been published')
    
    @transition(field=state, source=[STATE_PUBLISHED, STATE_EDITED], target=STATE_EDITED)
    def edit_blog(self, user):
        self.create_change_log(self.state, self.STATE_EDITED, user)
        logger.info(f'Blog post with id {self.id} has been edited')
    
    @transition(field=state, source=[STATE_DRAFT, STATE_PUBLISHED, STATE_EDITED], target=STATE_ARCHIVED)
    def archive_blog(self, user):
        self.create_change_log(self.state, self.STATE_ARCHIVED, user)
        logger.info(f'Blog post with id {self.id} has been archived')
        
    def create_change_log(self, source, target, user):
        from .models import BlogChangeLog
        blog = BlogChangeLog.objects.create(
            blog=self,
            changed_by=user,
            source=source,
            target=target
        )
        
        if blog:
            logger.info(f'Blog change log with id {blog.id} has been created')
        else:
            logger.error('Failed to create blog change log')