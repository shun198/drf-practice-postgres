import uuid

from django.db import models

from application.models.user import User


class Author(models.Model):
    """作者"""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_comment="お客様ID",
    )
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_comment="作成日時",
    )
    created_by = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_created_by",
        db_comment="作成者",
    )

    class Meta:
        db_table = "Author"
        db_table_comment = "作者"


class Book(models.Model):
    """本"""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_comment="お客様ID",
    )
    title = models.CharField(max_length=255)
    author = models.ForeignKey(
        Author,
        null=True,
        on_delete=models.CASCADE,
        related_name="%(class)s_author",
        db_comment="作者",
    )
    publication_date = models.DateField()
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_comment="作成日時",
    )
    created_by = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_created_by",
        db_comment="作成者",
    )

    class Meta:
        db_table = "Book"
        db_table_comment = "本"
