# myapp/serializers.py
from rest_framework import serializers
from .models import PoseFrame # Asumimos que este modelo existe

# --- SERIALIZER 1: Para un único frame dentro del lote ---
class PoseFrameSerializer(serializers.ModelSerializer):
    """
    Serializador para un objeto Frame individual dentro de la lista 'frames'.
    """
    
    # Estos campos vienen del cliente en el lote 'frames'
    frame_num = serializers.IntegerField() 
    timestamp = serializers.FloatField()  # Usamos FloatField para el time.time() de Python
    keypoints_data = serializers.JSONField()
    
    class Meta:
        model = PoseFrame
        # No incluimos 'session_id' aquí, ya que se inyectará desde el Serializador del Lote.
        fields = ['frame_num', 'timestamp', 'keypoints_data'] 
        
# --- SERIALIZER 2: Para la estructura completa del Lote ---
class BatchPoseSerializer(serializers.Serializer):
    """
    Serializador principal para validar la petición POST completa del lote.
    """
    session_id = serializers.CharField(max_length=100)
    batch_size = serializers.IntegerField(required=False)
    
    # La clave: 'frames' es una lista de objetos, 
    # y cada objeto es validado por PoseFrameSerializer.
    frames = PoseFrameSerializer(many=True) 

    # Sobrescribir el método save() para manejar el guardado masivo (bulk create)
    def create(self, validated_data):
        session_id = validated_data.pop('session_id')
        frames_data = validated_data.pop('frames')
        
        pose_frames_to_create = []
        
        # Iterar sobre la lista de frames validados para construir los objetos del modelo
        for frame_data in frames_data:
            # Crear una instancia del modelo, inyectando el session_id
            pose_frames_to_create.append(
                PoseFrame(
                    session_id=session_id,
                    frame_num=frame_data['frame_num'],
                    timestamp=frame_data['timestamp'],
                    keypoints_data=frame_data['keypoints_data']
                )
            )
            
        # Usar bulk_create para guardar todos los objetos en una sola consulta a la BD
        # Esto es *mucho* más eficiente que un bucle con save() individual.
        return PoseFrame.objects.bulk_create(pose_frames_to_create)