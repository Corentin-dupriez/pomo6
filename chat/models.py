from django.db import models

class Thread(models.Model):
    participants = models.ManyToManyField('auth.User',
                                          related_name='threads')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Thread between {' and '.join([user.first_name + ' ' + user.last_name if user.first_name else user.username for user in self.participants.all()])}'

class Message(models.Model):
    thread = models.ForeignKey(Thread,
                               on_delete=models.CASCADE)

    sender = models.ForeignKey('auth.User',
                               on_delete=models.CASCADE,
                               related_name='sender')

    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

