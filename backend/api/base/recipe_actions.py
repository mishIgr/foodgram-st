from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from recipes.models import Recipe


class BaseRecipeActionView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        serializer = self.serializer_class(
            data={'user': request.user.id, 'recipe': recipe.id},
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        if not Recipe.objects.filter(pk=recipe_id).exists():
            return Response(status=status.HTTP_404_NOT_FOUND)

        deleted_count, _ = self.model.objects.filter(
            user=request.user,
            recipe_id=recipe_id
        ).delete()

        if deleted_count == 0:
            return Response(
                {'detail': self.not_found_message},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(status=status.HTTP_204_NO_CONTENT)
