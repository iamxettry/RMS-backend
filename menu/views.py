from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .serializers import MenuSerializers
from .models import MenuItem


from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from random import sample
import random
# menu view
class MenuViews(APIView):
    def post(self, request):
        serializer=MenuSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message":"Menu created Successfully"}, status=status.HTTP_201_CREATED,content_type="application/json")
        return Response(serializer.error_messages,status=status.HTTP_400_BAD_REQUEST,content_type="application/json")


    def get(self, request, format=None):
        queryset=MenuItem.objects.all()
        serializer=MenuSerializers(queryset,many=True)
        count=queryset.count()
        for item in serializer.data:
            item['img'] = request.build_absolute_uri(item['img'])
        data={
            "url":request.build_absolute_uri(),
            "result":serializer.data,
            "count":count
        }
        return Response(data,status=status.HTTP_200_OK)
    
    def put(self,request,p_id):
        p_id=int(p_id)
        try:
            item_shelf =MenuItem.objects.get(id=p_id)
        except MenuItem.DoesNotExist:
            return Response({'error': 'Menu not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer=MenuSerializers( instance=item_shelf,data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            # serializer.data['img'] = request.build_absolute_uri(serializer.data['img'])
            return Response({"message":"Menu updated successfully!",'result':serializer.data},content_type="application/json")
        return Response({"error":serializer.errors,"message": "Menu Update failed."}, status=status.HTTP_400_BAD_REQUEST,content_type="application/json")

class Menu_Item(APIView):
    def get(self, request, p_id):
        p_id = int(p_id)
        try:
            instance = MenuItem.objects.get(id=p_id)
            serializer = MenuSerializers(instance)
            # Build absolute URL for the 'img' field
            if instance.img:
                img_absolute_url = request.build_absolute_uri(instance.img.url)
                serializer.data['img'] = img_absolute_url

            return Response(serializer.data, status=status.HTTP_200_OK)
        except MenuItem.DoesNotExist:
            return Response({'error': "Item Not Found!"}, status=status.HTTP_404_NOT_FOUND)
    def delete(self, request, p_id):
        try:
            item = MenuItem.objects.get(id=p_id)
            item.delete()
            return Response({"message": "Item deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except MenuItem.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

class CategoryListAPIView(APIView):
      def get(self, request, category=None):
        if category is None:
            # No category provided, list all categories
            categories = MenuItem.objects.values('category').distinct()
            result = []
            for cat in categories:
                category_name = cat['category']
                
                # Retrieve all items for the current category
                items = MenuItem.objects.filter(category=category_name)
                
                # Serialize the items for the category
                serialized_items = MenuSerializers(items, many=True).data

                # Shuffle the items randomly
                # randomized_items = sample(serialized_items, len(serialized_items))
                # Build image URLs for each item in the category
                for item in serialized_items:
                    item['img'] = request.build_absolute_uri(item['img'])

                
                # Add the category and its items to the result list
                result.append({
                    "category": category_name,
                    "data": serialized_items
                })
            
            return Response({"result": result}, status=status.HTTP_200_OK)
        else:
            # Filter food items based on the provided category
            food_items = MenuItem.objects.filter(category=category)

            # Serialize the filtered food items
            serializer = MenuSerializers(food_items, many=True)
            for item in serializer.data:
                item['img'] = request.build_absolute_uri(item['img'])

            # Return the serialized data as a JSON response
            return Response(serializer.data, status=status.HTTP_200_OK)
        

class VegFoodCategoryAPIView(APIView):
    def get(self, request, veg):
        if veg.lower() == 'none':
            itemtype = MenuItem.NONE
        elif veg.lower() == 'veg':
            itemtype = MenuItem.VEG
        elif veg.lower() == 'nonveg':
            itemtype = MenuItem.NON_VEG
        else:
            # Handle invalid input here, e.g., return an error response
            return Response({"msg": "Invalid input"}, status=status.HTTP_400_BAD_REQUEST)

            
        # Filter food items based on whether they are vegetarian or non-vegetarian
        food_items = MenuItem.objects.filter(itemtype=itemtype)
     

        # Serialize the filtered food items
        serializer = MenuSerializers(food_items, many=True)
        
        for item in serializer.data:
            item['img'] = request.build_absolute_uri(item['img'])

        # Return the serialized data as a JSON response
        return Response({"msg":"Success","result":serializer.data}, status=status.HTTP_200_OK) 



class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuSerializers
    parser_classes = (MultiPartParser, FormParser)

    def list(self, request):
        serializer = self.get_serializer(self.queryset, many=True, context={'request': request})

        # Get the 'num_items' and 'category' query parameters
        num_items = request.query_params.get('num_items', None)
        category = request.query_params.get('category', None)

        if category:
            queryset = self.queryset.filter(category=category)
        else:
            queryset = self.queryset

         # Convert the queryset to a list and shuffle it randomly
        queryset_list = list(queryset)
        random.shuffle(queryset_list)
        print(queryset_list)
        if num_items is not None:
            try:
                num_items = int(num_items)
                if num_items > 0:
                    # Limit the queryset to num_items
                    queryset_list = queryset_list[:num_items]
            except ValueError:
                return Response({"error": "Invalid 'num_items' parameter. Please provide a valid integer."}, status=status.HTTP_400_BAD_REQUEST)

        serialized_data = serializer.to_representation(queryset_list)
        return Response(serialized_data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Menu created successfully", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        try:
            instance = self.get_object()
            instance.delete()
            return Response({"message": "Item deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except MenuItem.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)


