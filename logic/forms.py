from django import forms

from .models import Vehicle_Model, Boxes_Model

class VehicleForm(forms.Form):

    truck_length = forms.IntegerField(label='truck length', widget=forms.NumberInput(attrs={'placeholder': 'Truck length'}))
    truck_width = forms.IntegerField(label='truck width', widget=forms.NumberInput(attrs={'placeholder': 'Truck width'}))
    truck_height = forms.IntegerField(label='truck height', widget=forms.NumberInput(attrs={'placeholder': 'Truck height'}))

    truck_length.initial = 1360
    truck_width.initial = 248
    truck_height.initial = 240

    class Meta:
        model = Vehicle_Model
        fields = [
            'length',
            'width',
            'height'
        ]

class BoxesForm(forms.Form):

    box_length = forms.IntegerField(label='box length', widget=forms.NumberInput(attrs={'placeholder': 'Box length'}))
    box_width = forms.IntegerField(label='box width', widget=forms.NumberInput(attrs={'placeholder': 'Box width'}))
    box_height = forms.IntegerField(label='box height', widget=forms.NumberInput(attrs={'placeholder': 'Box height'}))

    box_length.initial = 100
    box_width.initial = 100
    box_height.initial = 100

    class Meta:
        model = Boxes_Model
        fields = [
            'length',
            'width',
            'height'
        ]

class AmendedBoxesForm(forms.Form):

    amended_box_length = forms.IntegerField(label='box length', widget=forms.NumberInput(attrs={'placeholder': 'Box length'}))
    amended_box_width = forms.IntegerField(label='box width', widget=forms.NumberInput(attrs={'placeholder': 'Box width'}))
    amended_box_height = forms.IntegerField(label='box height', widget=forms.NumberInput(attrs={'placeholder': 'Box height'}))

    class Meta:
        model = Boxes_Model
        fields = [
            'length',
            'width',
            'height'
        ]