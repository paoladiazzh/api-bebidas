from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import BebidaSerializer
import boto3
import json

# Lista en memoria
bebidas_data = []

class BebidaListCreate(APIView):
    def get(self, request):
        return Response(bebidas_data)
    
    def post(self, request):
        serializer = BebidaSerializer(data=request.data)
        if serializer.is_valid():
            bebidas_data.append(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BebidaDetail(APIView):
    def get_object(self, pk):
        for bebida in bebidas_data:
            if bebida['id'] == pk:
                return bebida
        return None

    def get(self, request, pk):
        bebida = self.get_object(pk)
        if bebida:
            return Response(bebida)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        bebida = self.get_object(pk)
        if not bebida:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = BebidaSerializer(data=request.data)
        if serializer.is_valid():
            bebidas_data.remove(bebida)
            bebidas_data.append(serializer.data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        bebida = self.get_object(pk)
        if bebida:
            bebidas_data.remove(bebida)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)

# Endpoint especial: enviar postre a la cola SQS
class CrearPostreDesdeBebida(APIView):
    def post(self, request):
        postre_data = request.data

        # Aquí se envía a la cola de SQS (se configurará en AWS)
        sqs = boto3.client(
            'sqs',
            region_name='us-east-1',
            aws_access_key_id='ASIARDSSQLQU7QAVYKR2',
            aws_secret_access_key='HYg9DG+anAMYGypUhQc610MQefKXoiTq3qCsaVNm',
            aws_session_token='IQoJb3JpZ2luX2VjEIj//////////wEaCXVzLXdlc3QtMiJIMEYCIQDskuC91imJ/xhzAljHRU0JR6It52554vA7wNoFKevEVwIhAPcYU9Dk/2NAI9iwkxvYJ6oHFOcCweXvXbqBMNU628/mKqQCCFEQARoMMDc2NDA4NzA4MTM3IgxiksvphppGORcK0QIqgQKeG3EbN1CsWg3uGUA5uI3IQjgpK8qXzYxc8U7Q8K201f7pTeavDH6N/8dxCk5CVJrpyNJAuaEBX7Nh5feqN99nKXMtWHWQ56n8Yh+7o9WHxpzrN1UBSUgbWnV4DfvOuFEK9DWOk0D8UWKbDIvvgHOAtG2hx8LX8OrmJOPYVikoHy+7/qeRkDDT7Hvj5gQik1c6qDPMIFzS5U/QWiw8HwE/JAaP61Y2UpZYBuNx5qPy1YY8V5eVruRvPEFvjwQZbEqifKosiJyIdnPnXOHIxc9OontGhCfGyyOc/gaP6c+2WomkAhLlJmW3XA/WeRV1sjnPMfvrto8tyylHfB+MKNaW9zDbh9TBBjqcAZz85Cv5uvzk/VnP5TGZNVeMlf2WQTq2qBUkr1n5g3tNmNniPq7wsXu4AK1LWlynmac7F7Mb39US1hoMEJyAwTYmLqREorBl6KlRmUlHo7R6IJM1Y3l7qTDydZiKvl7jgxy8H5s/52ANh1Rr3CFpW7sIf1FXQjmxWZ8CGIzEH7CAUX8mnu6phhqS7xJgd5aJd/LYgGUsuLRFrmd7Tw=='
        )
        queue_url = 'https://sqs.us-east-1.amazonaws.com/076408708137/postres-queue'
        sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps(postre_data))

        return Response({"mensaje": "Postre enviado a la cola"}, status=status.HTTP_202_ACCEPTED)
