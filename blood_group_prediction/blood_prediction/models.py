from django.db import models

class Fingerprint(models.Model):
    image = models.ImageField(upload_to='fingerprints/')  # Stores uploaded image
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Timestamp of upload

    def __str__(self):
        return f"Fingerprint {self.id} uploaded at {self.uploaded_at}"
