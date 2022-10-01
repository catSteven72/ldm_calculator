let boxes = {
boxes_object: {},
drawn_boxes: {},
coords_list: {},
boxes_for_list: {},
random_boxes_created: false,
remove_all_random_boxes: false
}

var create_box = document.getElementById('add_box_button')

create_box.addEventListener("click", add_box)

var create_truck = document.getElementById('create_truck_btn')
create_truck.addEventListener("click", draw_truck)

var place_boxes_btn = document.getElementById('place_boxes_button')
place_boxes_btn.addEventListener("click", function() {
  boxes.coords_list = {}  
  boxes.boxes_object = {}
  boxes.remove_all_random_boxes = true
  remove_drawn_boxes()
  boxes.remove_all_random_boxes = false
  boxes.random_boxes_created = false
  add_boxes_to_boxes_object()
  add_multiple_boxes_request()
  
})

var create_random_boxes_btn = document.getElementById('create_random_boxes_button')
create_random_boxes_btn.addEventListener("click", function() {
  boxes.coords_list = {}
  boxes.boxes_object = {}
  boxes.remove_all_random_boxes = true
  remove_drawn_boxes()
  boxes.remove_all_random_boxes = false

  boxes.boxes_object = random_boxes_from_interval(30, 248)
  boxes.random_boxes_created = true
  add_multiple_boxes_request()
  boxes.boxes_object = {}
})

function remove_drawn_boxes() {
  
  var check_if_user_drawn_boxes_exist = document.getElementsByClassName('user_boxes')
  var check_if_random_drawn_boxes_exist = document.getElementsByClassName('random_boxes')
  if (!!check_if_user_drawn_boxes_exist) {
    for (var key of Object.keys(boxes.drawn_boxes)) {
      remove_drawn_box(`remove_box${key}`)
    }
  }

  if (!!check_if_random_drawn_boxes_exist)  {
    if (boxes.remove_all_random_boxes == true) {
      while(check_if_random_drawn_boxes_exist.length > 0){
        check_if_random_drawn_boxes_exist[0].parentNode.removeChild(check_if_random_drawn_boxes_exist[0]);
    }
    }
  }
}

function random_boxes_from_interval(min, max) {
  test_boxes = {}
  for (i = 1; i <= 20; i++) {
    test_boxes[i] = {
      'length': (Math.floor(Math.random() * (max - min + 1) + min)), 
      'width': (Math.floor(Math.random() * (max - min + 1) + min))}
  }
  return test_boxes
}

function add_multiple_boxes_request() {

  remove_drawn_boxes()
  var check_if_truck_exists = document.getElementById('truck')

  if (!!check_if_truck_exists){
    var csrf = $("input[name=csrfmiddlewaretoken]").val()

  $("#place_boxes_button").attr('disabled', 'disabled');
  $("#create_random_boxes_button").attr('disabled', 'disabled');

    $.ajax({
      url : '',
      headers: {
        'X-CSRFToken': csrf
      },
      type : 'POST', 
      data : {
        'box_list': boxes.boxes_object,
        'action': 'add_multiple_boxes'
      },
      success: function(response) { 

        draw_boxes_in_truck(response)
        $("#place_boxes_button").removeAttr('disabled');
        $("#create_random_boxes_button").removeAttr('disabled');
      }
    })
    
  } 
}

function draw_boxes_in_truck(response){

  var truck_element = document.getElementById('truck')

  let check_if_boxes_exist = document.getElementById('box1')

  if (!!check_if_boxes_exist) {
    for (var key of Object.keys(boxes.drawn_boxes)) {
      remove_drawn_box(`remove_box${key}`)
    }
  }
  
  boxes.drawn_boxes = {}
  var truck_element = document.getElementById('truck')

  for (var key of Object.keys(response)) {
    boxes.coords_list[key] = {
      'x1': response[key]['x1']/20 + 'vmin',
      'y1': response[key]['y1']/20 + 'vmin',
      'length': response[key]['length']/20 + 'vmin',
      'width': response[key]['width']/20 + 'vmin',
      'color_bg': response[key]['color_bg'],
      'color_fg': response[key]['color_fg']
    }

    var draw_box = document.createElement('div')

    if (boxes.random_boxes_created == true) {
      draw_box.id = 'random_box' + key
      draw_box.className = 'random_boxes'
    }
    else {
      draw_box.id = 'box' + key
      draw_box.className = 'user_boxes'
    } 
    
    draw_box.style.position = 'absolute' 
    draw_box.style.left = boxes.coords_list[key]['x1']
    draw_box.style.top = boxes.coords_list[key]['y1']
    draw_box.style.width = boxes.coords_list[key]['width']
    draw_box.style.height = boxes.coords_list[key]['length']
    draw_box.style.backgroundColor = boxes.coords_list[key]['color_bg']
    draw_box.style.color = boxes.coords_list[key]['color_fg']
    draw_box.style.borderWidth = '0.5px'
    draw_box.style.borderStyle = 'solid'
    draw_box.style.borderColor = 'black'
    draw_box.style.display = 'block'

    var box_number_text = document.createTextNode(key);
    font_size_width = response[key]['width']/22
    font_size_length = response[key]['length']/22
    if (font_size_width <= font_size_length) {
      font_size = font_size_width + 'vmin'
    }
    else {
      font_size = font_size_length + 'vmin'
    }
    draw_box.appendChild(box_number_text)
    draw_box.style.fontSize = font_size
    draw_box.style.textAlign = 'center'
    draw_box.style.lineHeight = boxes.coords_list[key]['length']
    draw_box.style.verticalAlign = 'middle'
    

    boxes.drawn_boxes[key] = draw_box.id

    truck_element.appendChild(draw_box)

  }

}

function remove_box_request(){
  var csrf = $("input[name=csrfmiddlewaretoken]").val()
  $.ajax({
    url : '',
    type : 'POST',
    headers: {
      'X-CSRFToken': csrf
    },
    data : {
      'box_length': box_length,
      'box_width': box_width,
      'action': 'remove_box'
    },
    success: function(response) {
    }
  })
}

function draw_truck(){
  var truck_exists = document.getElementById('truck')
  if (!!truck_exists){
    truck_exists.remove()
    
  }
  
  var truck_form_elem = document.getElementById('truck_form1')
  var truck_length = truck_form_elem['truck_length'].value/20
  var truck_width = truck_form_elem['truck_width'].value/20
  var div_for_truck_element = document.getElementById('div_for_truck')
  var truck_element = document.createElement("div")
  truck_element.id = 'truck'
  div_for_truck_element.appendChild(truck_element)
  truck_element.style.width = truck_width + 'vmin'
  truck_element.style.height = truck_length + 'vmin'
  truck_element.style.borderWidth = '1px'
  truck_element.style.borderStyle = 'solid'
  truck_element.style.borderColor = 'black'
  truck_element.style.display = 'block'
  truck_element.style.left = '50px'
  truck_element.style.position = 'relative'
  truck_element.style.BackgroundColor = 'white'

  var csrf = $("input[name=csrfmiddlewaretoken]").val()
  $.ajax({
    url : '',
    headers: {
      'X-CSRFToken': csrf
    },
    type : 'POST', 
    data : {
      'truck_length': truck_length*20,
      'truck_width': truck_width*20,
      'action': 'create_truck'
    }
  })
}

function add_box(){
  var check_if_truck_exists = document.getElementById('truck')
  if (!check_if_truck_exists){
    return
  }
  else{

    var box_elem = document.getElementById('box_form1')
    var box_length = parseInt(box_elem['box_length'].value, 10)
    var box_width = parseInt(box_elem['box_width'].value, 10)

    var box_num = Object.keys(boxes.boxes_for_list).length + 1

    var box_list_elem = document.getElementById('boxes_list')
    var box_for_list = document.createElement("li")
    var box_length_label = document.createElement("label")
    var box_length_input = document.createElement("input")
    var box_width_label = document.createElement("label")
    var box_width_input = document.createElement("input")
    var box_remove_button = document.createElement("input")

    box_for_list.id = 'box_li' + box_num
    boxes.boxes_for_list[box_num] = box_for_list

    box_length_label.id = 'length_label' + box_num
    box_width_label.id = 'width_label' + box_num

    box_length_input.type = "text"
    box_length_input.value = box_length
    box_length_input.id = 'box_length_input' + box_num

    box_width_input.type = "text"
    box_width_input.value = box_width
    box_width_input.id = 'box_width_input' + box_num

    box_remove_button.type = "button"
    box_remove_button.value = "X"
    box_remove_button.id = 'remove_box' + box_num

    var length_node = document.createTextNode("Length: ")
    var width_node = document.createTextNode("Width: ")
    box_length_label.appendChild(length_node)
    box_width_label.appendChild(width_node)
    box_for_list.appendChild(box_length_label)
    box_for_list.appendChild(box_length_input)
    box_for_list.appendChild(box_width_label)
    box_for_list.appendChild(box_width_input)
    box_for_list.appendChild(box_remove_button)
    box_list_elem.appendChild(box_for_list)
    box_remove_button.addEventListener("click", function(e) {

      remove_drawn_box(e.target.id)
      remove_box_elements(e.target.id)
      
    })
  }
}

function add_boxes_to_boxes_object() {

  for (var [box_num, value] of Object.entries(boxes.boxes_for_list)) {
    var box_length_entry = boxes.boxes_for_list[box_num].children[`box_length_input${box_num}`]
    var box_width_entry = boxes.boxes_for_list[box_num].children[`box_width_input${box_num}`]
    boxes.boxes_object[box_num] = {'length': box_length_entry.value, 'width': box_width_entry.value}
    
    var box_width_element = document.getElementById(box_width_entry.id)
    box_width_element.addEventListener("change", function(){
      box_width = box_width_element.value
      boxes.boxes_object[box_num]['width'].replace(box_width)
    })

    var box_length_element = document.getElementById(box_length_entry.id)
    box_length_element.addEventListener("change", function(){
      box_length = box_length_element.value
      boxes.boxes_object[box_num]['length'].replace(box_length)
    })
  }
}

function remove_drawn_box(e_target_id){

  id_num = e_target_id.slice(10,)
  id_num_int = parseInt(id_num, 10)
 
  var drawn_box_to_remove = document.getElementById('box' + id_num)
  delete boxes.drawn_boxes[id_num_int]

  if (!drawn_box_to_remove){
    return
  }

  drawn_box_to_remove.remove()
}

function remove_box_elements(e_target_id){
  var id_num = e_target_id.slice(10,)
  var id_num_int = parseInt(id_num, 10)
  delete boxes.boxes_object[id_num_int]
  delete boxes.boxes_for_list[id_num_int]

  for (key of Object.keys(boxes.boxes_for_list)){
    var key_int = parseInt(key, 10)
    if (key_int > id_num_int) {
      var new_length_input_id = `box_length_input${key_int-1}`
      var new_width_input_id = `box_width_input${key_int-1}`
      var new_box_remove_button_id = `remove_box${key_int-1}`
      boxes.boxes_object[key_int-1] = boxes.boxes_object[key_int]
      boxes.boxes_for_list[key_int-1] = boxes.boxes_for_list[key_int]
      boxes.boxes_for_list[key_int-1].children[`box_length_input${key_int}`].id = new_length_input_id
      boxes.boxes_for_list[key_int-1].children[`box_width_input${key_int}`].id = new_width_input_id
      boxes.boxes_for_list[key_int-1].children[`remove_box${key_int}`].id = new_box_remove_button_id
      boxes.boxes_for_list[key_int-1].id = `box_li${key_int-1}`

      delete boxes.boxes_object[key_int]
      delete boxes.boxes_for_list[key_int]
    }
  }
  
  var box_to_remove_from_list_elem = document.getElementById('box_li' + id_num_int)
  box_to_remove_from_list_elem.remove()
  
}