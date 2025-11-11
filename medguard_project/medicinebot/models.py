from django.db import models
from django.contrib.auth.models import User

# Model for your medicine dataset (if you are populating it from the CSV)
class Medicine(models.Model):
    name = models.CharField(max_length=200, unique=True)
    content = models.TextField()
    used_for = models.TextField()

    def __str__(self):
        return self.name

# Model for storing user search history
class History(models.Model):
    # Link each history item to a specific user
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Store the text from OCR or the text query (CORRECTED FIELD NAME)
    search_query = models.TextField(blank=True, null=True) 
    
    # Store the final summary from the bot
    analysis_summary = models.TextField(blank=True, null=True)
    
    # Store the base64-encoded image URL (can be blank if it was a text search)
    image_data_url = models.TextField(blank=True, null=True)
    
    # Automatically add the date and time when the item is created
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # This is what you'll see in the Django admin area
        return f"History for {self.user.username} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"