import random

class Boxes():
    num_of_boxes = 0
    coordinates = {}
    coords = {}
    list_of_boxes= {}
    empty_x_axis_space = {}
    

    def clear_coordinates(self):
        Boxes.coordinates = {}
        Boxes.coords = {}
    
    def add_box(self, length, width):
        if (width > self.truck_width and length > self.truck_width) or length > self.truck_length:
            return self.coords
        elif width > self.truck_width and width < self.truck_length and length <= self.truck_width:
            length, width = width, length
        self.num_of_boxes += 1
        self.list_of_boxes.update({self.num_of_boxes: {'length': length, 'width': width, 'placed': 0}})
        self.place_x_axis(self.list_of_boxes[self.num_of_boxes], self.num_of_boxes)
        return self.coords
    
    def create_truck(self, truck_length, truck_width):
        self.truck_length = int(truck_length)
        self.truck_width = int(truck_width)
        return
    
    def place_x_axis(self, box, box_num):
        if box['placed'] == 1:
            return
        box_width = box['width']
        box_length = box['length']

        if (box_width > self.truck_width) or (box_length > self.truck_length):
            return

        elif len(self.coords) == 0:
            color = self.generate_color()
            self.coordinates.update(
                    {box_num: {'x1': 0, 'y1': 0, 'x2': box_width, 'y2': box_length}})

            self.coords.update(
                    {box_num: {
                        'x1': 0, 'y1': 0, 'width': box_width, 'length': box_length, 'color_bg': color['color_bg'], 'color_fg': color['color_fg']}})
            self.free_space_under_boxes.update({box_num: {'x1': 0, 'x2': box_width, 'y1': box_length}})
            box['placed'] = 1
            return self.coords

        else:
            self.free_space_under_boxes = dict(sorted(self.free_space_under_boxes.items(), key=lambda item: item[1]['y1']))
            for available_space_below in self.free_space_under_boxes:
                test_y1 = self.free_space_under_boxes[available_space_below]['y1'] + 0.01
                test_y2 = test_y1 + box_length
                
                for x_coord in range(0, self.truck_width-box_width):
                    test_x1 = x_coord
                    test_x2 = test_x1 + box_width
                    self.test_interference(box, test_x1, test_x2, test_y1, test_y2, box_length, box_width, box_num)
                    
                    if box['placed'] == 1:
                        return self.coords

    def generate_color(self):

        first = random.randint(0, 255)
        second = random.randint(0, 255)
        third = random.randint(0, 255)

        if first > 220 and second > 220 and third > 220:
            return self.generate_color()
        elif first < 40 and second < 40 and third < 40:
            return self.generate_color()
        else:
            first_bg = ("%02x"%first)
            second_bg = ("%02x"%second)
            third_bg = ("%02x"%third)

            brightness = (first*299 + second*587 + third*114)/1000
            if brightness < 125:
                color_fg = 'white'
            else:
                color_fg = 'black'

            h = "#"
            
            color_bg = h+first_bg+second_bg+third_bg

            color = {'color_bg': color_bg, 'color_fg': color_fg}
            return color
     
    def update_free_space(self, test_x1, test_x2, test_y1, test_y2):
        for x in self.coordinates:
            y2_of_other_box_for_comparison = round((self.coordinates[x]['y2'] + 0.01), 3)
            max_x2_box_above_test_box = 0
            max_x2_test_box = 0
            test_x1_inside_other_box = (self.coordinates[x]['x1'] < test_x1 < self.coordinates[x]['x2'])
            test_x2_inside_other_box = (self.coordinates[x]['x1'] < test_x2 < self.coordinates[x]['x2'])
            if (
                test_y1 == y2_of_other_box_for_comparison
                ) and (
                max_x2_box_above_test_box < test_x2
                ) and ((
                test_x1_inside_other_box
                ) or (
                test_x2_inside_other_box
                )):
                    if (
                        test_x1_inside_other_box and test_x2_inside_other_box
                        ) or (
                        not test_x1_inside_other_box and test_x2_inside_other_box
                    ):
                        max_x2_box_above_test_box = test_x2
                        self.free_space_under_boxes.update({
                            x: {
                                'x1': test_x2, 
                                'x2': self.coordinates[x]['x2'], 
                                'y1': y2_of_other_box_for_comparison}})
                    elif test_x1_inside_other_box and not test_x2_inside_other_box:
                        max_x2_box_above_test_box = self.coordinates[x]['x2']
                        self.free_space_under_boxes.update({
                            x: {
                                'x1': self.coordinates[x]['x2'],
                                'x2': self.coordinates[x]['x2'], 
                                'y1': y2_of_other_box_for_comparison}})
                        
            elif (
                test_y2 == self.coordinates[x]['y1'] - 0.01
                ) and (
                max_x2_test_box < test_x2
                ) and ((
                test_x1_inside_other_box
                ) or (
                test_x2_inside_other_box
                )):
                    if (
                        test_x1_inside_other_box and test_x2_inside_other_box
                        ) or (
                        not test_x1_inside_other_box and test_x2_inside_other_box
                    ):
                        max_x2_test_box = test_x2
                        self.free_space_under_boxes.update({
                            x: {
                                'x1': test_x2, 
                                'x2': test_x2, 
                                'y1': test_y2}})
                    elif test_x1_inside_other_box and not test_x2_inside_other_box:
                        max_x2_test_box = self.coordinates[x]['x2']
                        self.free_space_under_boxes.update({
                            x: {
                                'x1': self.coordinates[x]['x2'],
                                'x2': test_x2, 
                                'y1': test_y2}})

        max_y2 = max(self.coordinates[key]['y2'] for key in self.coordinates.keys())

        self.free_space_under_boxes.update({
                            'free space after last box': {
                                'x1': 0,
                                'x2': self.truck_width, 
                                'y1': max_y2}})

    def test_interference(self, box, test_x1, test_x2, test_y1, test_y2, box_length, box_width, box_num):
        max_y = self.truck_length
        not_interferes_x_axis = 0
        for key, other_box in self.coordinates.items():

            if ((other_box['x1'] < test_x1 < other_box['x2']) or (
                    other_box['x2'] > test_x2 > other_box['x1']
            )
            ) and ((
                        other_box['y1'] <= test_y1 <= other_box['y2']
                ) or (
                        other_box['y1'] <= test_y2 <= other_box['y2']
                )):
                pass #left or right corner of test_box on other box

            elif (
                test_x1 <= other_box['x1']
                ) and (
                test_x2 >= other_box['x2']
                ) and (
                    other_box['y1'] <= test_y1 <= other_box['y2']
                    ) and (
                        other_box['y1'] <= test_y2 <= other_box['y2']
                    ):
                    pass #test_box cross other box left to right
            elif (
                other_box['x2'] >= test_x1 >= other_box['x1']
            ) and (
                other_box['x1'] <= test_x2 <= other_box['x2']
            ) and (
                test_y1 < other_box['y1']
            ) and (
                test_y2 > other_box['y2']
            ):
                pass #test_box cross other box top to bottom

            elif (
                other_box['x2'] >= test_x1 >= other_box['x1']
            ) and (
            other_box['y1'] <= test_x2 <= other_box['x2']
            ) and (
                other_box['y2'] >= test_y2 >= other_box['y1']
            ):
                pass #lower part of narrow test box inside wider other box

            elif (
            other_box['x2'] >= test_x1 >= other_box['x1']
            ) and (
                other_box['x1'] <= test_x2 <= other_box['x2']
            ) and (
                other_box['y1'] <= test_y1 <= other_box['y2']
            ):
                pass #upper part of narrow test box inside wider other box

            elif (
                test_x1 <= other_box['x1'] <= test_x2
            ) and (
                test_x2 >= other_box['x2'] >= test_x1
            ) and (
                test_y2 >= other_box['y1'] >= test_y1
            ):
                pass #lower part of wider test box over narrow other box
            
            elif (
                test_x1 <= other_box['x1'] <= test_x2
            ) and (
                test_x2 >= other_box['x2'] >= test_x1
            ) and (
                test_y1 <= other_box['y2'] <= test_y2
            ):
                pass #upper part of wider test box over narrow other box

            elif (
                other_box['x2'] > test_x2 > other_box['x1']
            ) and (
                test_x1 < other_box['x1']
            ) and (
                other_box['y2'] >= test_y1 >= other_box['y1']
            ) and (
                other_box['y1'] <= test_y2 <= other_box['y2']
            ):
                pass # narrow test box imposes from the left

            elif (
                other_box['x2'] > test_x1 > other_box['x1']
            ) and (
                test_x2 > other_box['x2']
            ) and (
                other_box['y2'] >= test_y1 >= other_box['y1']
            ) and (
                other_box['y1'] <= test_y2 <= other_box['y2']
            ):
                pass # narrow test box imposes from the right

            elif (
                other_box['x2'] > test_x2 > other_box['x1']
            ) and (
                test_x1 <= other_box['x1']
            ) and (
                test_y1 <= other_box['y1']
            ) and (
                test_y2 >= other_box['y2']
            ):
                pass # larger sized test box imposes from left

            elif (
                other_box['x1'] < test_x1 < other_box['x2']
            ) and (
                test_x2 > other_box['x2']
            ) and (
                test_y1 <= other_box['y1']
            ) and (
                test_y2 >= other_box['y2']
            ):
                pass # larger sized test box imposes from right

            elif (
            other_box['x2'] >= test_x1 >= other_box['x1']
            ) and (
                other_box['x1'] <= test_x2 <= other_box['x2']
            ) and (
                other_box['y1'] <= test_y1 <= other_box['y2']
            ) and (
                other_box['y1'] <= test_y2 <= other_box['y2']
            ):
                pass #test box placed inside other box

            elif (
                test_x1 <= other_box['x1'] <= test_x2
            ) and (
                test_x2 >= other_box['x2'] >= test_x1
            ) and (
                test_y1 <= other_box['y1'] <= test_y2
            ) and (
                test_y2 >= other_box['y2'] >= test_y1
            ):
                pass #test box placed over other box

            elif test_y2 > self.truck_length:
                pass
            elif test_x2 > self.truck_width:
                pass
            else:
                
                not_interferes_x_axis += 1

        if not_interferes_x_axis == len(self.coordinates):
            if box['placed'] == 0:
                color = self.generate_color()
                self.coordinates.update(
                    {box_num: {'x1': test_x1, 'y1': test_y1, 'x2': test_x2, 'y2': test_y2}})
                self.coords.update(
                {box_num: {'x1': test_x1, 'y1': test_y1, 'width': box_width, 'length': box_length, 
                'color_bg': color['color_bg'], 'color_fg': color['color_fg']}})
                self.free_space_under_boxes.update({box_num: {'x1': test_x1, 'x2': test_x2, 'y1': test_y2}})
                self.update_free_space(test_x1, test_x2, test_y1, test_y2)
                box['placed'] = 1
                return True