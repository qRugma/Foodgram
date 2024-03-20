# import base64

# from django.core.files.base import ContentFile

# from rest_framework import serializers

# from recipe.models import Tag


# class TagListingField(serializers.RelatedField):

#     def to_representation(self, value):
#         return {
#             "id": value.id,
#             "name": value.name,
#             "color": value.color,
#             "slug": value.slug,
#         }

#     def to_internal_value(self, data):
#         try:
#             return Tag.objects.get(pk=data)
#         except Tag.DoesNotExist:
#             raise serializers.ValidationError(f"tag {data} not exists")


# class AuthorField(serializers.RelatedField):
#     def to_representation(self, value):
#         author = value.author
#         return {
#             'email': author.email,
#             'id': author.id,
#             'username': author.username,
#             'first_name': author.first_name,
#             'last_name': author.last_name,
#             # 'is_subscribed': author.is_subscribed,
#         }


# class Base64ImageField(serializers.ImageField):
#     def to_internal_value(self, data):
#         if isinstance(data, str) and data.startswith('data:image'):
#             format, imgstr = data.split(';base64,')
#             ext = format.split('/')[-1]
#             data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
#         return super().to_internal_value(data)
