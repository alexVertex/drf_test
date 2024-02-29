import csv
import xlsxwriter

from django.http import HttpResponse
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializers import *

# Create your views here.


class CarsViewList(generics.ListAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class CarsViewCreate(generics.CreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = (IsAdminUser,)


class CarsViewUpdate(generics.UpdateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = (IsAdminUser,)


class CarsViewDelete(generics.DestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = (IsAdminUser,)


###########################################################
class CountryViewList(generics.ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class CountryViewCreate(generics.CreateAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = (IsAdminUser,)


class CountryViewUpdate(generics.UpdateAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = (IsAdminUser,)


class CountryViewDelete(generics.DestroyAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = (IsAdminUser,)


###########################################################
class ManufactureViewList(generics.ListAPIView):
    queryset = Manufacture.objects.all()
    serializer_class = ManufactureSerializer


class ManufactureViewCreate(generics.CreateAPIView):
    queryset = Manufacture.objects.all()
    serializer_class = ManufactureSerializer
    permission_classes = (IsAdminUser,)


class ManufactureViewUpdate(generics.UpdateAPIView):
    queryset = Manufacture.objects.all()
    serializer_class = ManufactureSerializer
    permission_classes = (IsAdminUser,)


class ManufactureViewDelete(generics.DestroyAPIView):
    queryset = Manufacture.objects.all()
    serializer_class = ManufactureSerializer
    permission_classes = (IsAdminUser,)


###########################################################


class CommentaryViewList(generics.ListAPIView):
    queryset = Commentary.objects.all()
    serializer_class = CommentarySerializer


class CommentaryViewCreate(generics.CreateAPIView):
    queryset = Commentary.objects.all()
    serializer_class = CommentarySerializer


class CommentaryViewUpdate(generics.UpdateAPIView):
    queryset = Commentary.objects.all()
    serializer_class = CommentarySerializer
    permission_classes = (IsAdminUser,)


class CommentaryViewDelete(generics.DestroyAPIView):
    queryset = Commentary.objects.all()
    serializer_class = CommentarySerializer
    permission_classes = (IsAdminUser,)

###########################################################


def make_csv(filename, model, model_serializer):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="'+filename+'.csv"'
    serializer = model_serializer(model.objects.all(), many=True)
    header = model_serializer.Meta.fields
    writer = csv.DictWriter(response, fieldnames=header)
    writer.writeheader()
    for row in serializer.data:
        writer.writerow(row)
    return response


def make_xlsx(filename, model, model_serializer):
    # create our spreadsheet.  I will create it in memory with a StringIO
    buffer = io.BytesIO()

    workbook = xlsxwriter.Workbook(buffer)
    worksheet = workbook.add_worksheet()
    serializer = model_serializer(model.objects.all(), many=True)
    header = model_serializer.Meta.fields
    for col_num in range(len(header)):
        worksheet.write(0, col_num, header[col_num])
    row_num = 1
    for row in serializer.data:
        col_num = 0
        for cell in row:
            data = str(row[cell])
            worksheet.write(row_num, col_num, data)
            col_num += 1
        row_num += 1
    workbook.close()
    # create a response
    response = HttpResponse(content_type='application/vnd.ms-excel')
    # tell the browser what the file is named
    response['Content-Disposition'] = 'attachment;filename="'+filename+'.xlsx"'
    # put the spreadsheet data into the response
    response.write(buffer.getvalue())
    # return the response
    return response


def export(type_export, filename, model, model_serializer):
    if type_export == 'CSV':
        return make_csv(filename, model, model_serializer)
    elif type_export == 'XLSX':
        return make_xlsx(filename, model, model_serializer)
    else:
        return Response({"error": type_export + " is unknown format. CSV and XLSX is allowed."})


class ExportCSVCountries(APIView):
    def get(self, request, *args, **kwargs):
        export_type = request.query_params.get('type')
        return export(export_type, "countryExport", Country, CountrySerializer)


class ExportCSVManufactures(APIView):
    def get(self, request, *args, **kwargs):
        export_type = request.query_params.get('type')
        return export(export_type, "manufactureExport", Manufacture, ManufactureSerializer)


class ExportCSVCars(APIView):
    def get(self, request, *args, **kwargs):
        export_type = request.query_params.get('type')
        return export(export_type, "carsExport", Car, CarSerializer)


class ExportCSVCommentaries(APIView):
    def get(self, request, *args, **kwargs):
        export_type = request.query_params.get('type')
        return export(export_type, "commentaryExport", Commentary, CommentarySerializer)

# class CarViewSet(viewsets.ModelViewSet):
#    queryset = Car.objects.all()
#    serializer_class = CarSerializer
#
#    @action(methods=['get'], detail=False)
#    def manufacture(self, request):
#        manufactures = Manufacture.objects.all()
#        return Response({'mans': [m.name for m in manufactures]})

# class CarAPIList(generics.ListCreateAPIView):
#    queryset = Car.objects.all()
#    serializer_class = CarSerializer
#
#
# class CarAPIGetUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
#    queryset = Car.objects.all()
#    serializer_class = CarSerializer



# class CarsAPIView(generics.ListAPIView):
#    serializer_class = CarSerializer
#
#    def get(self, request):
#        carsData = Car.objects.all()
#        return Response({'GET': CarSerializer(carsData, many=True).data})
#
#    def post(self, request):
#        serializer = CarSerializer(data=request.data)
#        serializer.is_valid(raise_exception=True)
#        serializer.save()
#        return Response({'ADD': serializer.data})
#
#    def put(self, request, *args, **kwargs):
#        pk = kwargs.get('pk',None)
#        if not pk:
#            return Response({"Error": "No instance for update has been chosen"})
#
#        try:
#            instance = Car.objects.get(pk=pk)
#        except:
#            return Response({"Error": "Instance for update doesn't exists"})
#
#        serializer = CarSerializer(data=request.data,instance=instance)
#        serializer.is_valid(raise_exception=True)
#        serializer.save()
#        return Response({'UPDATE': serializer.data})
#
#
#    def delete(self, request, *args, **kwargs):
#        pk = kwargs.get('pk',None)
#        if not pk:
#            return Response({"Error": "No instance for delete has been chosen"})
#
#        try:
#            instance = Car.objects.get(pk=pk)
#        except:
#            return Response({"Error": "Instance for delete doesn't exists"})
#
#        instance.delete()
#
#        return Response({'Remove': "Instance removed " +str(pk)})
