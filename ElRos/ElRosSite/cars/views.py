import csv
import io
import xlsxwriter

from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .permissions import CommentaryPermission
from .serializers import *

# region models_viewsets


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class ManufactureViewSet(viewsets.ModelViewSet):
    queryset = Manufacture.objects.all()
    serializer_class = ManufactureSerializer


class CommentaryViewSet(viewsets.ModelViewSet):
    queryset = Commentary.objects.all()
    serializer_class = CommentarySerializer
    permission_classes = (CommentaryPermission,)

# endregion

# region export_viewsets


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
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename="'+filename+'.xlsx"'
    response.write(buffer.getvalue())
    return response


def export(request, filename, model, model_serializer):
    type_export = request.query_params.get('type')
    if type_export is not 'str':
        return Response({'error: cant read type get param.'})
    if type_export == 'CSV':
        return make_csv(filename, model, model_serializer)
    elif type_export == 'XLSX':
        return make_xlsx(filename, model, model_serializer)
    else:
        return Response({'error: ' + type_export + ' is unknown format. CSV and XLSX is allowed.'})


class ExportViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['get'])
    def country(self, request, *args, **kwargs):
        return export(request, 'countryExport', Country, CountrySerializer)

    @action(detail=False, methods=['get'])
    def manufacture(self, request, *args, **kwargs):
        return export(request, 'manufactureExport', Manufacture, ManufactureSerializer)

    @action(detail=False, methods=['get'])
    def car(self, request, *args, **kwargs):
        return export(request, 'carExport', Car, CarSerializer)

    @action(detail=False, methods=['get'])
    def commentary(self, request, *args, **kwargs):
        return export(request, 'commentaryExport', Commentary, CommentarySerializer)
