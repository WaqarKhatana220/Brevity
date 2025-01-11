import logging
from django.db import models
from django_fsm import transition, FSMField
from ..constants import DRAFT, PUBLISHED, EDITED, ARCHIVED

logger = logging.getLogger('django')

class PostWorkflow(models.Model):
    STATE_DRAFT = DRAFT
    STATE_PUBLISHED = PUBLISHED
    STATE_EDITED = EDITED
    STATE_ARCHIVED = ARCHIVED
    
    STATE_CHOICES = (
        (STATE_DRAFT, 'Draft'),
        (STATE_PUBLISHED, 'Published'),
        (STATE_ARCHIVED, 'Archived')
    )
    
    state = FSMField(choices=STATE_CHOICES, default=STATE_DRAFT)
    
    class Meta:
        abstract = True
    
    @transition(field=state, source=STATE_DRAFT, target=STATE_PUBLISHED)
    def publish_blog(self):
        logger.info(f'Blog post {self.id} has been published')
    
    @transition(field=state, source=STATE_PUBLISHED, target=STATE_EDITED)
    def edit_blog(self):
        logger.info(f'Blog post {self.id} has been edited')
    
    @transition(field=state, source=[STATE_DRAFT, STATE_PUBLISHED, STATE_EDITED], target=STATE_ARCHIVED)
    def archive_blog(self):
        logger.info(f'Blog post {self.id} has been archived')