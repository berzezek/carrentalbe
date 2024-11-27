from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Требуется аутентификация
def current_user_view(request):
    user = request.user  # Получаем текущего пользователя из токена
    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
    })
