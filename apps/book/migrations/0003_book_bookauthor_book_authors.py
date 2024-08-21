# Generated by Django 5.1 on 2024-08-20 10:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("book", "0002_tag"),
    ]

    operations = [
        migrations.CreateModel(
            name="Book",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                (
                    "isbn",
                    models.CharField(max_length=13, primary_key=True, serialize=False),
                ),
                ("title", models.CharField(max_length=50)),
                ("description", models.TextField(blank=True, null=True)),
                ("page_count", models.PositiveSmallIntegerField()),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("pr", "programming"),
                            ("ar", "art"),
                            ("hi", "history"),
                            ("po", "politics"),
                            ("ot", "others"),
                        ],
                        default="pr",
                        max_length=2,
                    ),
                ),
                ("published_date", models.IntegerField()),
                ("publisher", models.CharField(max_length=50)),
                ("lang", models.CharField(max_length=50)),
                ("edition", models.SmallIntegerField(blank=True, null=True)),
                (
                    "book_format",
                    models.CharField(
                        choices=[("eb", "ebook"), ("hc", "hardcover")],
                        default="eb",
                        max_length=2,
                    ),
                ),
                ("tags", models.ManyToManyField(to="book.tag")),
            ],
            options={
                "ordering": ("-title",),
                "default_related_name": "%(app_label)s_%(model_name)s",
            },
        ),
        migrations.CreateModel(
            name="BookAuthor",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "role",
                    models.CharField(
                        choices=[
                            ("author", "Author"),
                            ("co_author", "Co-Author"),
                            ("editor", "Editor"),
                        ],
                        default="author",
                        max_length=10,
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="book.author"
                    ),
                ),
                (
                    "book",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="book.book"
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Books and Authors",
            },
        ),
        migrations.AddField(
            model_name="book",
            name="authors",
            field=models.ManyToManyField(through="book.BookAuthor", to="book.author"),
        ),
    ]
