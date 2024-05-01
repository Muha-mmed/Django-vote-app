from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Poll(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    question = models.TextField()
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option1_count = models.IntegerField(default=0)
    option2_count = models.IntegerField(default=0)
    option3_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def total_count(self):
        self.option1_count + self.option2_count + self.option3_count
          
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return self.question
    