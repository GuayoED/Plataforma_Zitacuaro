from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models.functions import Coalesce
from django.db.models import Sum
from .forms import ReporteForm
from reciclaje.models import Entradas


#Se encarga de generar y mostrar reportes

class ReporteView(TemplateView):
    template_name = 'reportes/reporte.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        print(self.request.user.first_name)
        print(self.request.user.last_name)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_report':
                data = []
                start_date = request.POST.get('start_date', '')
                end_date = request.POST.get('end_date', '')
                search = Entradas.objects.all()
                if len(start_date) and len(end_date):
                    search = search.filter(fecha__range=[start_date, end_date])
                for s in search:
                    data.append([
                        s.id,
                        s.lugar,
                        s.trabajador,
                        s.fecha.strftime('%Y-%m-%d'),
                        s.Curp.first_name,
                        s.DF.nombre,
                        s.Cantidad,
                        s.puntos
                    ])
                cantidad = search.aggregate(r=Coalesce(Sum('Cantidad'), 0.0)).get('r')
                puntos = search.aggregate(r=Coalesce(Sum('puntos'), 0.0)).get('r')

                data.append([
                    '---',
                    '---',
                    '---',
                    '---',
                    '---',
                    'Total',
                    cantidad,
                    puntos

                ])
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)


    def get_context_data(self, **kwars):
        context = super().get_context_data(**kwars)
        context['title'] = 'Reporte de Almacenes'
        context['form'] = ReporteForm
        return context



