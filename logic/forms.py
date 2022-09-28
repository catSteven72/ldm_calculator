from django import forms

from .models import Vehicle_Model, Boxes_Model

class VehicleForm(forms.Form):

    truck_length = forms.IntegerField(label='truck length', widget=forms.NumberInput(attrs={'placeholder': 'Truck length'}))
    truck_width = forms.IntegerField(label='truck width', widget=forms.NumberInput(attrs={'placeholder': 'Truck width'}))

    truck_length.initial = 1360
    truck_width.initial = 248

    class Meta:
        model = Vehicle_Model
        fields = [
            'length',
            'width'
        ]

class BoxesForm(forms.Form):

    box_length = forms.IntegerField(label='box length', widget=forms.NumberInput(attrs={'placeholder': 'Box length'}))
    box_width = forms.IntegerField(label='box width', widget=forms.NumberInput(attrs={'placeholder': 'Box width'}))

    box_length.initial = 100
    box_width.initial = 100

    class Meta:
        model = Boxes_Model
        fields = [
            'length',
            'width'
        ]