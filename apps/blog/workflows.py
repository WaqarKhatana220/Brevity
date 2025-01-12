import logging
from django.db import models
from viewflow.fsm import State
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
    
    state = models.CharField(
        max_length=50,
        choices=STATE_CHOICES,
        default=STATE_DRAFT
    )
    state_fsm = State(STATE_CHOICES, default=STATE_DRAFT)
    
    class Meta:
        abstract = True
    
    @state_fsm.transition(source=STATE_DRAFT, target=STATE_PUBLISHED)
    def publish_blog(self):
        self.state = self.STATE_PUBLISHED
        logger.info(f'Blog post has been published')
    
    @state_fsm.transition(source=STATE_PUBLISHED, target=STATE_EDITED)
    def edit_blog(self):
        self.state = self.STATE_EDITED
        logger.info(f'Blog post has been edited')
    
    @state_fsm.transition(source=[STATE_DRAFT, STATE_PUBLISHED, STATE_EDITED], target=STATE_ARCHIVED)
    def archive_blog(self):
        self.state = self.STATE_ARCHIVED
        logger.info(f'Blog post has been archived')