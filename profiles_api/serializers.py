import contextlib
from rest_framework import fields, serializers, status
from rest_framework.response import Response
from profiles_api import models
import profiles_api
from .models import Event


class HelloSerializer(serializers.Serializer):
    """Serializes a name field for testing our APIView"""

    name = serializers.CharField(max_length=20)


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""

    class Meta:
        model = models.UserProfile
        fields = ('id', 'email', 'name', 'profile_img', 'password',
                  'is_superuser', 'is_staff')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            },
            'is_superuser': {
                'read_only': True,
            },
            'is_staff': {
                'read_only': True,
            }
        }

    def create(self, validated_data):
        """Create and return a new user"""
        user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            profile_img=validated_data['profile_img'],
            password=validated_data['password'],
        )
        return user


# class ProfileFeedItemSerializer(serializers.ModelSerializer):
#     """Create profile feed item"""

#     class Meta:
#         model = models.ProfileFeedItem
#         fields = ('id', 'user_profile', 'status_text', 'created_on')
#         extra_kwargs = {
#             'user_profile': {
#                 'read_only': True
#             }
#         }


class InventoryItemSerialiser(serializers.ModelSerializer):
    """Create Inventory item serializer"""

    class Meta:
        model = models.InventoryItem
        fields = ('id', 'owner_club', 'item_name', 'item_description',
                  'item_img', 'total_quantity', 'avl_quantity')
        extra_kwargs = {
            'owner_club': {
                'read_only': True
            }
        }


class EventSerialiser(serializers.ModelSerializer):
    """Create Event serializer"""

    class Meta:
        model = models.Event
        fields = ('id', 'owner_club', 'event_name', 'event_description',
                  'status', 'created_on', 'start_date', 'end_date')
        extra_kwargs = {
            'owner_club': {
                'read_only': True
            }
        }


class EventInventorySerialiser(serializers.ModelSerializer):
    """Create Event-Inventory serializer"""

    class Meta:
        model = models.EventInventoryRelationship
        fields = ('id', 'event_id', 'inventory_id',
                  'req_quantity', 'approval_status')
        extra_kwargs = {
            'owner_club': {
                'read_only': True
            },
            'approval_status': {
                'read_only': True
            }
        }

    def create(self, validated_data):

        event_name = validated_data['event_id']
        event = Event.objects.get(event_name=event_name)
        curr_user = self.context['request'].user
        if event.owner_club.id == curr_user.id:
            return super().create(validated_data)
        else:
            error = {'message': 'You are not the creator of this event'}
            raise serializers.ValidationError(error)
