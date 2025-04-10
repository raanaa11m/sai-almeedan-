import folium
from geopy.distance import geodesic


user_location = [24.774265, 46.739586]


m = folium.Map(location=user_location, zoom_start=18)
folium.Marker(user_location, tooltip="موقعك داخل ملعب الملك فهد", icon=folium.Icon(color="blue")).add_to(m)


food_stalls = [
    {"name": "كشك شرقي", "location": [24.774365, 46.739786]},
    {"name": "كشك غربي", "location": [24.774165, 46.739386]},
    {"name": "كشك شمالي", "location": [24.774465, 46.739586]},
]

# تحديد أقرب كشك
nearest_stall = min(food_stalls, key=lambda x: geodesic(user_location, x["location"]).meters)

# عرض الأكشاك على الخريطة
for stall in food_stalls:
    folium.Marker(
        location=stall["location"],
        popup=stall["name"],
        icon=folium.Icon(color="green", icon="cutlery", prefix='fa')
    ).add_to(m)

# رسم خط إلى أقرب كشك
folium.PolyLine(
    [user_location, nearest_stall["location"]],
    color="green",
    weight=3,
    tooltip=f"أقرب كشك: {nearest_stall['name']}"
).add_to(m)

# المقاعد المتوفرة والمشغولة داخل الملعب
seats = [
    {"status": "متاح", "location": [24.774365, 46.739486]},
    {"status": "مشغول", "location": [24.774165, 46.739686]},
    {"status": "متاح", "location": [24.774265, 46.739786]},
]

# تحديد أقرب مقعد متاح
available_seats = [seat for seat in seats if seat["status"] == "متاح"]
nearest_seat = min(available_seats, key=lambda x: geodesic(user_location, x["location"]).meters)

# عرض المقاعد على الخريطة
for seat in seats:
    color = "blue" if seat["status"] == "متاح" else "red"
    folium.CircleMarker(
        location=seat["location"],
        radius=6,
        popup=f"المقعد: {seat['status']}",
        color=color,
        fill=True,
        fill_opacity=0.7
    ).add_to(m)

# رسم خط إلى أقرب مقعد
folium.PolyLine(
    [user_location, nearest_seat["location"]],
    color="orange",
    weight=3,
    tooltip="أقرب مقعد متاح"
).add_to(m)

# حفظ الخريطة
m.save("king_fahd_stadium_map.html")
