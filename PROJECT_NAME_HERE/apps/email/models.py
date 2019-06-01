from django.db import models

app_name = "email"

class Email(models.Model):

    from_email = models.EmailField()
    to_email = models.EmailField()

    subject = models.CharField(max_length=255)

    html_text = models.TextField()
    plain_text = models.TextField()

    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "<%s:%s> %s" % (self.from_email, self.to_email, self.subject)

class EmailQueue(models.Model):

    PENDING = 'pending'
    SENDING  = 'sending'
    SENT = 'sent'
    FAILED = 'failed'

    status_choices = (
        (PENDING, 'Pending'),
        (SENDING, 'Sending'),
        (SENT, 'Sent'),
        (FAILED, 'Failed')
    )

    email = models.ForeignKey(Email, on_delete=models.CASCADE)
    
    status = models.CharField(max_length=10, choices = status_choices, default = PENDING)
    status_msg = models.CharField(max_length=500, null=True)

    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "[%s] %s" % (self.status, self.email)
