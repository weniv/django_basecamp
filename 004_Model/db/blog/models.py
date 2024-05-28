from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    main_image = models.ImageField(upload_to="blog/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # 처음 생성될 때에만
    updated_at = models.DateTimeField(auto_now=True)  # 수정될 때마다

    def __str__(self):
        return self.title
