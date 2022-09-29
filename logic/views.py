from django.shortcuts import render
from .models import Vehicle_Model, Boxes_Model
from .forms import VehicleForm, BoxesForm
from .box_coordinates import Boxes
from django.views import View
from django.http import HttpResponse,JsonResponse 
import logging


class View1(View):

    truck_form = VehicleForm
    box_form = BoxesForm
    initial_truck = {'truck_length': 1360, 'truck_width': 248}
    initial_box = {'box_length': 100, 'box_width': 100}
    template_name = 'logic/home.html'
    truck = Boxes()

    

    def get(self, request):
        form1 = self.truck_form(initial=self.initial_truck)
        form2 = self.box_form(initial=self.initial_box)
        context = {
            'truck_form': form1,
            'box_form': form2,
            'truck_length': 0,
            'truck_width': 0,
        }

        return render(request, self.template_name, context)
    
    def post(self, request):
        logger = logging.getLogger('testlogger')
        #logger.info('request', request)
        coords = {}

        if request.POST['action'] == 'add_box':
            coords = self.add_box(request)

        elif request.POST['action'] == 'recalculate_coordinates':
            coords = self.recalculate_coords(request)

        elif request.POST['action'] == 'remove_box':
            coords = self.remove_box(request)

        elif request.POST['action'] == 'create_truck':
            self.truck.create_truck(int(request.POST['truck_length']), int(request.POST['truck_width']))
            self.truck.coords = {}
            self.truck.coordinates = {}
            self.truck.num_of_boxes = 0
            self.truck.list_of_boxes = {}
            return HttpResponse()

        elif request.POST['action'] == 'add_multiple_boxes':
            self.truck.empty_x_axis_space = {y_coord: [0] for y_coord in range(self.truck.truck_length+2)}
            self.truck.empty_y_axis_space = {x_coord: [0] for x_coord in range(self.truck.truck_width)}
            self.truck.free_space_under_boxes = {
                0: {'x1': 0, 'x2': self.truck.truck_width, 'y1': 0}}
            num_range = int((len(request.POST)-1)/2)
            
            self.truck.list_of_boxes = {}
            self.truck.coordinates = {}
            self.truck.coords = {}
            self.truck.num_of_boxes = 0
            for i in range(1, num_range+1):
                box_length = request.POST[f'box_list[{i}][length]']
                box_width = request.POST[f'box_list[{i}][width]']
                coords = self.add_box(int(box_length), int(box_width))

        if coords == None:
            coords = {}

        
        logger.info('coords', coords)
        logger.info('truck length', self.truck.truck_length)
        logger.info('truck width', self.truck.truck_width)
        return JsonResponse(coords, safe=True)

    def add_box(self, length, width):
        
        coords = self.truck.add_box(length, width)

        return coords