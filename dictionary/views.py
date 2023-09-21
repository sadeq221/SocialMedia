from rest_framework.views import APIView
from rest_framework.response import Response


class AddToDict(APIView):
    '''
    A view that gets an entry and return a whole dictionary
    '''

    def post(self, request):
        entry = request.data['entry']

        with open('dictionary/dict_file.txt', 'r', encoding='utf_8') as f:
            text = f.read()

        text = entry + "\n\n" + text

        with open("dictionary/dict_file.txt", "w", encoding="utf_8") as f:
            f.write(text)

        return Response({"data": text})

