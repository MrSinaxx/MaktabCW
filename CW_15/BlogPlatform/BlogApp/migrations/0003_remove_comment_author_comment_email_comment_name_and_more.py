# Generated by Django 4.1 on 2023-07-14 11:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("BlogApp", "0002_post_category_alter_comment_author_and_more"),
    ]

    operations = [
        migrations.RemoveField(model_name="comment", name="author",),
        migrations.AddField(
            model_name="comment",
            name="email",
            field=models.EmailField(default=1, max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="comment",
            name="name",
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="comment",
            name="post",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="BlogApp.post"
            ),
        ),
    ]
