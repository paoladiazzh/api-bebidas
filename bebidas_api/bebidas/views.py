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
            aws_access_key_id='ASIARDSSQLQUQNBX4IWX',
            aws_secret_access_key='7da/AeNtTIJJbj6meT+81XxzCHPvbbc+3QgqWHJ+',
            aws_session_token='IQoJb3JpZ2luX2VjEC0aCXVzLXdlc3QtMiJHMEUCIQDqq1Mf9hXF+Cf1pqeUkOAyyAkOWDQgmabViqowxnUNhgIgdc6km+U2ZFIYEYxGvj8fhQbucoVo8pBQd476Bcu9uUYqrQII5f//////////ARABGgwwNzY0MDg3MDgxMzciDGT25fzxtep1ge46niqBAmGdKHTU/i4lYj2V2SdYG46VVnYxPjipk+yaOAFNrAi6N8m3BemZc5MO4gqmwBe7pWV1yimgl48R57rnjv+pZa76r6lxj3fo2c45dra9EMelRTivqLreavGDSoplklriPXo516DbfRuFLRoh5WUa7ZQAaFlYN+N4mKbDuxGF6ADTJwbsXF7A6lx1DkVLIOUWplQa1owkDK9AKSJOuhms1aqNPbfUOED4HZQmF/R891eU8X33oWwhofe6tKkaPbPgDL/ewq3hDMmezd2uD8Cdqd8hL+zhe+TOwJAPEyHcvbds4SdkuZj5t0mAOCtFMOpEy8ryK1lK7xRNA4aLTEaz7371MNzvv8EGOp0B3IkPnY/HlEiEzJMbHloT3MxoW5f7mo7F/1bpwXHH6V29D9qm+eMz/aXb2rXFqUQonVz+SVN+DslUENgyVFW1kiIiwZ9J61xw7f2SvEoWOHPJsJ0gyEdkp5X6kkI9aNGHirSsxcNnLw/m/Yn41PvtFFzuiiAhTg+4KDNKXgVyZriJ70HsxfZRo42HoXY9CeaveOHysFM5IjEI6FoTAQ=='
        )
        queue_url = 'https://sqs.us-east-1.amazonaws.com/076408708137/postres-queue'
        sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps(postre_data))

        return Response({"mensaje": "Postre enviado a la cola"}, status=status.HTTP_202_ACCEPTED)
