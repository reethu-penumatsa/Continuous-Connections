from tkinter import *
import folium
from geopy.geocoders import Nominatim
import time
import webbrowser
from threading import Thread
from time import sleep
from folium.plugins import AntPath
from tkvideo import tkvideo
import pygame

# Initialize splash screen
splash_screen = Tk()
splash_screen.geometry('1000x1000+10+10')
splash_screen.title('continuous_connection')
splash_screen.attributes("-fullscreen", True)

# Initialize pygame mixer for music
pygame.mixer.init()
pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(-1)

# Global variables
num_computers = 0
counter = 1
network = {}
computer_data = {}
originator = None

# Keep references to images to avoid garbage collection
image_refs = {}

def second_window():
    global num_computers, counter, computer_data, originator

    pygame.mixer.music.stop()
    splash_screen.destroy()

    root = Tk()
    root.geometry('1000x1000+10+10')
    root.title('continuous_connections')
    root.attributes("-fullscreen", True)

    # Load background image and keep reference
    bg = PhotoImage(file="solid background wise.png")
    bgl = bg.zoom(3, 3)
    image_refs['bgl'] = bgl  # keep reference
    imb = Label(root, image=bgl)
    imb.place(x=0, y=0)

    back = PhotoImage(file="second window.png")
    image_refs['back'] = back
    imglbl = Label(root, image=back, bg="grey")
    imglbl.pack()

    def combined_function():
        create_text_boxes()
        third_window()

    def create_text_boxes():
        nonlocal num_computers, originator  # refer to outer scope variables
        originator = originator_entry.get()
        try:
            num_computers = int(num_computers_entry.get())
        except ValueError:
            print("Please enter a valid number for computers")
            return

        num_computers_entry.config(state="disabled")
        create_button.config(state="disabled")
        originator_entry.config(state='disabled')

    def third_window():
        global counter, computer_data, network, originator

        root1 = Toplevel(root)
        root1.geometry('1000x1000+10+10')
        root1.title('continuous_connections')
        root1.attributes("-fullscreen", True)

        bg = PhotoImage(file="solid background wise.png")
        bgl = bg.zoom(3, 3)
        image_refs['bgl1'] = bgl
        imb = Label(root1, image=bgl)
        imb.place(x=0, y=0)

        back = PhotoImage(file="second window.png")
        image_refs['back1'] = back
        imglbl = Label(root1, image=back, bg="grey")
        imglbl.pack()

        location_label = None
        connections_label = None
        location_entry = None
        connections_entry = None

        def create_location_text_box():
            nonlocal location_label, connections_label, location_entry, connections_entry
            global counter, num_computers

            if counter <= num_computers:
                location_label = Label(root1, text=f"Computer {counter} location:", bg="#010B50", fg="#02FFD0", font=("britannic bold", 20))
                location_label.place(x=400, y=100)

                location_entry = Entry(root1, font=("britannic bold", 20), bg="#02FFD0", fg="#010B50")
                location_entry.place(x=800, y=100)

                connections_label = Label(root1, text=f"Computer {counter} connections:", bg="#010B50", fg="#02FFD0", font=("britannic bold", 20))
                connections_label.place(x=400, y=200)

                connections_entry = Entry(root1, font=("britannic bold", 20), bg="#02FFD0", fg="#010B50")
                connections_entry.place(x=800, y=200)

                submit_button.config(command=get_computer_data, state="normal")

            else:
                # No more entries needed, disable submit and create network
                submit_button.config(state="disabled")
                create_network_dict()

        def get_computer_data():
            nonlocal location_label, connections_label, location_entry, connections_entry
            global counter, computer_data

            # Validate inputs
            computer_location = location_entry.get()
            connections_str = connections_entry.get().strip()

            if not computer_location:
                print("Please enter a location")
                return

            try:
                computer_connections_list = connections_str.split()
                computer_connections = [int(c) for c in computer_connections_list] if connections_str else []
            except ValueError:
                print("Connections must be space-separated integers")
                return

            # Save data
            computer_data[counter] = {
                "location": computer_location,
                "connections": computer_connections
            }

            print(f"Computer {counter} Location:", computer_location)
            print(f"Computer {counter} Connections:", computer_connections)

            # Remove widgets for this computer input
            location_label.destroy()
            location_entry.destroy()
            connections_label.destroy()
            connections_entry.destroy()

            counter += 1

            create_location_text_box()

        def create_network_dict():
            global computer_data, network, originator

            network = {}
            for computer_num, data in computer_data.items():
                network[data["location"]] = [computer_data[conn]["location"] for conn in data["connections"]]

            print("Network Dictionary:", network)
            map_button.config(state='normal')

        def map_view():
            global network, originator

            class TreeNode:
                def __init__(self, value):
                    self.value = value
                    self.children = []
                    self.children_count = 0

                def add_child(self, child_value):
                    child_node = TreeNode(child_value)
                    self.children.append(child_node)
                    self.children_count += 1
                    return child_node

            def create_tree(root_value, connections):
                root = TreeNode(root_value)

                stack = [root]
                visited = set()

                while stack:
                    current_node = stack.pop()
                    current_node_value = current_node.value
                    visited.add(current_node_value)

                    for neighbor in connections.get(current_node_value, []):
                        if neighbor not in visited:
                            child_node = current_node.add_child(neighbor)
                            stack.append(child_node)

                return root

            def visualize_connections_on_map(root, connections):
                geolocator = Nominatim(user_agent="city_locator")

                def get_coordinates(city_name):
                    try:
                        location = geolocator.geocode(city_name)
                        if location:
                            return location.latitude, location.longitude
                        else:
                            print(f"Could not geolocate {city_name}")
                            return None, None
                    except Exception as e:
                        print(f"Error geolocating {city_name}: {e}")
                        return None, None

                my_map1 = folium.Map(location=[17.385044, 78.486671], zoom_start=5)

                def add_markers_and_connections(node):
                    for child in node.children:
                        src_coords = get_coordinates(node.value)
                        dest_coords = get_coordinates(child.value)

                        if None in src_coords or None in dest_coords:
                            continue  # skip if location not found

                        folium.Marker(src_coords, popup=node.value, tooltip=node.value).add_to(my_map1)
                        folium.Marker(dest_coords, popup=child.value, tooltip=child.value).add_to(my_map1)
                        folium.PolyLine([src_coords, dest_coords], color="blue", weight=1).add_to(my_map1)

                        add_markers_and_connections(child)

                    if node == root:
                        button_lat, button_long = get_coordinates(node.value)
                        if button_lat is not None:
                            button_marker = folium.Marker(
                                location=[button_lat, button_long],
                                icon=folium.Icon(icon='fa-laptop', color='red', prefix='fa'),
                                popup=node.value, tooltip=node.value
                            ).add_to(my_map1)
                            folium.CircleMarker(location=[button_lat, button_long], radius=25, fill_color='red').add_to(my_map1)
                            my_map1.save("mapin.html")
                            webbrowser.open("mapin.html")
                            send_messages(node)

                def mySort(e):
                    return e.children_count

                message_colors = ["blue", "green", "purple", "orange", "pink", "brown", "gray", "cyan", "magenta"]
                originator_colors = {}

                def send_messages(root):
                    if root is None:
                        return

                    root.children.sort(reverse=True, key=mySort)

                    for i, child in enumerate(root.children):
                        print(f"Message: {root.value} --> {child.value}")
                        ini_lat, ini_long = get_coordinates(root.value)
                        fin_lat, fin_long = get_coordinates(child.value)

                        if None in (ini_lat, ini_long, fin_lat, fin_long):
                            continue

                        color = message_colors[i % len(message_colors)]
                        AntPath([(ini_lat, ini_long), (fin_lat, fin_long)], delay=400, dash_array=[30, 15], color=color, weight=3).add_to(my_map1)
                        folium.Marker([fin_lat, fin_long], icon=folium.Icon(icon='fa-laptop', color='green', prefix='fa'), popup=child.value, tooltip=child.value).add_to(my_map1)
                        my_map1.save("map.html")
                        webbrowser.open("map.html")
                        sleep(3)  # Consider removing or moving this off the main thread
                        send_messages(child)

                add_markers_and_connections(root)
                return my_map1

            tree_root = create_tree(originator, network)
            connections_map = visualize_connections_on_map(tree_root, network)
            connections_map.save("mapsfin.html")
            webbrowser.open("mapsfin.html")

        submit_button = Button(root1, text="Submit", state="disabled", bg="#02FFD0", fg="#010B50")
        submit_button.place(x=500, y=300)

        map_button = Button(root1, text='View Map', command=map_view, state='disabled', bg="#02FFD0", fg="#010B50")
        map_button.place(x=800, y=300)

        create_location_text_box()
        root1.mainloop()

    num_computers_label = Label(root, text="Number of Computers:", font=("britannic bold", 25), bg="#010B50", fg="#02FFD0")
    num_computers_label.place(x=400, y=100)

    num_computers_entry = Entry(root, font=("britannic bold", 20), bg="#02FFD0", fg="#010B50")
    num_computers_entry.place(x=800, y=110)

    originator_label = Label(root, text="Enter the Originator location:", font=("britannic bold", 25), fg="#02FFD0", bg="#010B50")
    originator_label.place(x=400, y=200)

    originator_entry = Entry(root, font=("britannic bold", 20), bg="#02FFD0", fg="#010B50")
    originator_entry.place(x=900, y=210)

    create_button = Button(root, text="Enter", bg="#02FFD0", fg="#010B50", width=15, height=4, command=combined_function)
    create_button.place(x=700, y=300)

    root.mainloop()

# Splash screen UI
bglbl = Label(splash_screen, bg="#151B54", height=70, width=1000)
bglbl.place(x=0, y=0)

lblvideo = Label(splash_screen)
lblvideo.pack()

player = tkvideo("Starting video.mp4", lblvideo, loop=2, size=(1500, 800))
player.play()

# Start second window after 15 seconds
splash_screen.after(15000, second_window)

splash_screen.mainloop()
