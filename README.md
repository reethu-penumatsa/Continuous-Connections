# Continuous Connections - Network Visualizer

**Continuous Connections** is a Python GUI application that allows users to simulate and visualize computer network connections using an originator and connected systems. It provides an interactive way to understand how data/messages flow across a network, shown visually on a geographic map using real-world locations.

---

## 🚀 Features

- 🎬 Full-screen animated splash screen with background music  
- 🧠 User inputs number of computers and an originator location  
- 🌐 Enter real city names as computer locations  
- 🔗 Define network connections between computers  
- 🗺️ Visualize computer network structure on a real-time Folium map  
- 📡 Animated message propagation using AntPath from originator to others  

---

## 🛠️ Technologies Used

| Technology | Purpose                                    |
|------------|--------------------------------------------|
| Tkinter    | GUI interface                              |
| Folium     | Interactive map rendering                   |
| Geopy      | Location to latitude/longitude conversion  |
| tkvideo    | Video playback in splash screen             |
| pygame     | Background music                           |
| Threading  | Simulated parallel message sending         |

---

## 🧑‍💻 How to Use

- Run the Python script
- Network Map Simulation  
- Splash Screen (Wait for splash screen to finish)
- User Input  
    Enter the number of computers: N  
    Enter the originator's city name: OriginCity
- For Each Computer (1 to N):  
    Enter Location (city name)  
    Enter Connections (space-separated computer numbers)  
- View Map  
    All computers placed on the map according to their city names  
    Lines connecting computers based on connections entered  
    Animated messages flow from originator to all other computers following the connections  

- Example Output (Illustrative)  
    Originator: Computer 1 (OriginCity)  
    Computers: 1 - OriginCity, 2 - CityA, 3 - CityB, 4 - CityC  
    Connections:  
    1 <-> 2  
    1 <-> 4  
    2 <-> 3  
    Map:  
    [OriginCity (1)] ---- [CityA (2)] ---- [CityB (3)]  
    |  
    |  
    [CityC (4)]  
    Messages:  
    OriginCity → CityA: Sending message...  
    CityA → CityB: Forwarding message...  
    OriginCity → CityC: Sending message...
