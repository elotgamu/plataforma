from django.dispatch import receiver
from django.db.models.signals import post_save
from django.models import Administrator
from django.contrib.auth import Group


@receiver(post_save, sender=Administrator)
def assign_admin_to_group(sender, **kwargs):
    '''just add my activated admin to the admin group'''
    if kwargs['created'] is False:
        if kwargs['instance'].groups.filter(name='Administrator').exists():
            '''the admin is alreary in the group'''
            print('This admin already exists in administrator group')
        else:
            admin_group = Group.objects.get(name='Administrator')
            admin_group.user_set.add(kwargs['instance'])
            print('The new admin has been grouped in the Administrator group')
