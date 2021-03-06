from rest_framework import status
from rest_framework import viewsets
from rest_framework import authentication
from rest_framework import filters

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated

from profiles_api import serializers, models
from profiles_api import permissions


class HelloApiView(APIView):
    """Test API View"""
    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        """returns a list of APIView features"""
        an_apiview = [
            'Uses HTTP methors as function(get,post,patch,put,delete)',
            'Is similar to a traditional DJango View',
            'Gives yout he most control over the application logic',
            'is mapped manually to URLs',
        ]

        return Response({'message': 'Hello!', 'an_apiview': an_apiview})

    def post(self, request):
        """Create a hello message with our name"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello, {name}'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def put(self, request, pk=None):
        """Handle updating an object"""
        return Response({'method': 'PUT'})

    def patch(self, request, pk=None):
        """Handle a partial update of an object"""
        return Response({'method': 'PATCH'})

    def delete(self, request, pk=None):
        """Delete an object"""
        return Response({'method': 'DELETE'})


class HelloViewSet(viewsets.ViewSet):
    """Test API ViewSets"""
    serializer_class = serializers.HelloSerializer

    def list(self, request):
        """Return a hello message"""

        a_viewset = [
            'Uses actions: list, create, retrieve, update, partial_update',
            'Autmoatically maps ato URLs using Routers',
            'Provides more functionality with less code',
        ]

        return Response({'message': 'Hello', 'a_viewset': a_viewset})

    def create(self, request):
        """Create a new hello message"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello, {name}'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self, request, pk=None):
        """Handle getting an object by its ID"""
        return Response({'htpp_method': 'GET'})

    def update(self, request, pk=None):
        """Handle updating an object"""
        return Response({'http_method': 'PUT'})

    def partial_update(self, request, pk=None):
        """Handle a partial update of an object"""
        return Response({'http_method': 'PATCH'})

    def destroy(self, request, pk=None):
        """Handle deleting an object"""
        return Response({'htpp_method': 'DELETE'})


class UserProfileViewset(viewsets.ModelViewSet):
    """Handle creating and updating viewsets"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)


class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


# class UserProfileFeedViewsSet(viewsets.ModelViewSet):
#     """Handles creating, reading and updating profile feed items"""
#     authentication_classes = (TokenAuthentication,)
#     serializer_class = serializers.ProfileFeedItemSerializer
#     queryset = models.ProfileFeedItem.objects.all()
#     permission_classes = (
#         permissions.UpdateOwnFeedItem,
#         IsAuthenticated
#     )

#     def perform_create(self, serializer):
#         """set the user profile to the logged in user"""
#         serializer.save(user_profile=self.request.user)


class InventoryItemViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating of Inventory Items"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.InventoryItemSerialiser
    queryset = models.InventoryItem.objects.all()
    permission_classes = (
        permissions.UpdateOwnInventoryItem,
        IsAuthenticated
    )

    def perform_create(self, serializer):
        """set the user profile to the logged in user"""
        serializer.save(owner_club=self.request.user)


class EventViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating of Events"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.EventSerialiser
    queryset = models.Event.objects.all()
    permission_classes = (
        permissions.UpdateOwnEvent,
        IsAuthenticated
    )

    def perform_create(self, serializer):
        """set the user profile to the logged in user"""
        serializer.save(owner_club=self.request.user)


class EventInventoryViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating of EventInventory"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.EventInventorySerialiser
    queryset = models.EventInventoryRelationship.objects.all()
    permission_classes = (
        permissions.UpdateOwnEventInventory,
        IsAuthenticated
    )

    def get_serializer_context(self):
        context = super(EventInventoryViewSet, self).get_serializer_context()
        context.update({'request': self.request})
        return context
