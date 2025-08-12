from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from firebase_admin import db
from datetime import datetime

class LandingAPI(APIView):
    name = "Landing API"
    collection_name = "votes"  # Cambia este nombre según tu colección en Firebase

    def get(self, request):

      # Referencia a la colección
      ref = db.reference(f'{self.collection_name}')

      # get: Obtiene todos los elementos de la colección
      data = ref.get()

      # Devuelve un arreglo JSON
      return Response(data, status=status.HTTP_200_OK)

    def post(self, request):

      data = request.data
      format = ["email", "user", "message"]
      counter = 0

      for key in data:
        if key not in format:
            return Response({"error": f"Invalid field: {key}"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            counter += 1

      if counter != len(format):
          return Response({"error": "Missing fields"}, status=status.HTTP_400_BAD_REQUEST)

      # Referencia a la colección
      ref = db.reference(f'{self.collection_name}')

      current_time  = datetime.now()
      #custom_format = current_time.strftime("%d/%m/%Y, %I:%M:%S %p").lower().replace('am', 'a. m.').replace('pm', 'p. m.')
      custom_format = current_time.strftime("%Y-%m-%dT%H:%M:%S") + f".{current_time.microsecond // 1000:03d}Z"

      data.update({"date": custom_format })

      # push: Guarda el objeto en la colección
      new_resource = ref.push(data)

      # Devuelve el id del objeto guardado
      return Response({"id": new_resource.key}, status=status.HTTP_201_CREATED)