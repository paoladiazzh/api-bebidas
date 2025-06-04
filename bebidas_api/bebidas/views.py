from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .serializers import BebidaSerializer
import boto3
import json
from .models import Bebida

sqs = boto3.client('sqs', region_name=settings.AWS_REGION)

# Vista para el CRUD de Bebidas
class BebidaListCreate(APIView):
    def get(self, request):
        bebidas = Bebida.objects.all()
        serializer = BebidaSerializer(bebidas, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BebidaSerializer(data=request.data)
        if serializer.is_valid():
            bebida = serializer.save()
            
            # --- DETERMINAR EL SABOR ---
            sabor_sugerido = "Vainilla" # Sabor por default
            if bebida.tipo.lower() == 'café':
                sabor_sugerido = "Chocolate"
            elif bebida.tipo.lower() == 'frutal':
                sabor_sugerido = "Fresa"
            elif bebida.tipo.lower() == 'té':
                sabor_sugerido = "Limón"
            # ----------------------------------------------------

            # 🍰 Prepara el mensaje para el postre relacionado
            postre_data = {
                "nombre": f"Postre para {bebida.nombre}",
                "sabor": sabor_sugerido, # ¡Ya no es un valor fijo!
                "tamanio": bebida.tamanio,
                "bebida_sugerida_id": bebida.id
            }

            try:
                # Envía el mensaje a SQS
                sqs.send_message(
                    QueueUrl=settings.SQS_QUEUE_URL,
                    MessageBody=json.dumps(postre_data)
                )
                print(f"Mensaje para postre enviado a SQS para la bebida ID: {bebida.id}")
            except Exception as e:
                print(f"Error enviando a SQS: {e}")
                # Podrías agregar lógica para reintentar o manejar el fallo

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

