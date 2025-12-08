# myapp/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import BatchPoseSerializer

class BatchPoseAPIView(APIView):
    """
    Endpoint para recibir lotes de datos de pose del cliente OpenCV.
    """
    def post(self, request, *args, **kwargs):
        
        # 1. Usar el Serializer de Lote para validar el payload completo
        serializer = BatchPoseSerializer(data=request.data)
        
        if serializer.is_valid():
            
            # 2. Llamar a save(), que ejecutará el método create() que definimos 
            #    en BatchPoseSerializer, realizando el bulk_create.
            try:
                # El resultado es la lista de objetos PoseFrame creados
                created_frames = serializer.save() 
                
                return Response({
                    "message": "Lote recibido y guardado exitosamente.",
                    "frames_saved": len(created_frames),
                    "session_id": serializer.validated_data.get('session_id')
                }, status=status.HTTP_201_CREATED)

            except Exception as e:
                # Manejo de errores de base de datos
                return Response({"error": f"Error al guardar los datos: {str(e)}"}, 
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # 3. Si la validación falla, devolver errores
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)