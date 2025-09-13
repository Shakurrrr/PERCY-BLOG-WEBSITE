from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Post, Comment

@receiver(post_migrate)
def create_groups(sender, **kwargs):
    if sender.name != "blog":
        return
    admin_group, _ = Group.objects.get_or_create(name="Admin")
    editor_group, _ = Group.objects.get_or_create(name="Editor")
    reader_group, _ = Group.objects.get_or_create(name="Reader")

    post_ct = ContentType.objects.get_for_model(Post)
    comment_ct = ContentType.objects.get_for_model(Comment)
    perms = Permission.objects.filter(content_type__in=[post_ct, comment_ct])

    admin_group.permissions.set(perms)
    editor_group.permissions.set(perms.filter(codename__in=[
        "add_post","change_post","view_post","add_comment","change_comment","view_comment"
    ]))
    reader_group.permissions.set(Permission.objects.filter(
        codename__in=["add_comment","view_post","view_comment"]
    ))
