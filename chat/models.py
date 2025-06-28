from django.db import models
from django.contrib.auth import get_user_model

class Thread(models.Model):
    participants = models.ManyToManyField(get_user_model(),
                                          related_name='threads')

    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'Thread between {' and '.join([user.get_username() for user in self.participants.all()])}'

class Message(models.Model):
    thread = models.ForeignKey(Thread,
                               on_delete=models.CASCADE)

    sender = models.ForeignKey(get_user_model(),
                               on_delete=models.CASCADE,
                               related_name='sender')

    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

