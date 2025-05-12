import folium
import pandas as pd
from geopy.distance import geodesic

# Load and clean Zillow rental data
df = pd.read_csv("Zillow_Chicago_Rental_Data.csv")
df = df.dropna(subset=['latitude', 'longitude', 'price'])

# Load Divvy bike station data
divvy_df = pd.read_csv("Divvy_Bicycle_Stations_20250512.csv")
divvy_df = divvy_df.dropna(subset=['Latitude', 'Longitude'])

# Create sample amenity data (grocery, library, gym, CTA)
amenities = [
    {"name": "Trader Joe's", "lat": 41.8715, "lon": -87.6475, "type": "Grocery"},
    {"name": "ALDI", "lat": 41.8623, "lon": -87.6465, "type": "Grocery"},
    {"name": "Harold Washington Library", "lat": 41.8763, "lon": -87.6280, "type": "Library"},
    {"name": "UIC Student Recreation Facility", "lat": 41.8706, "lon": -87.6503, "type": "Gym"},
    {"name": "UIC-Halsted Station", "lat": 41.8757, "lon": -87.6498, "type": "CTA Station"}
]

# Calculate city-wide average rent
avg_price = df['price'].mean()

# Create map centered on Chicago with a bigger view
m = folium.Map(location=[41.8781, -87.6298], zoom_start=11, width='100%', height='100%')

# Add a prominent marker for UIC
uic_location = [41.8708, -87.6505]  # University of Illinois at Chicago
folium.Marker(
    location=uic_location,
    popup="<b>University of Illinois at Chicago (UIC)</b>",
    icon=folium.Icon(color='blue', icon='university', prefix='fa', icon_color='white')
).add_to(m)

# Add amenities to map
for a in amenities:
    icon_color = 'green' if a['type'] == 'Grocery' else 'purple' if a['type'] == 'Library' else 'darkred' if a['type'] == 'Gym' else 'gray'
    folium.Marker(
        location=[a['lat'], a['lon']],
        popup=f"{a['name']} ({a['type']})",
        icon=folium.Icon(color=icon_color, icon='info-sign')
    ).add_to(m)

# Add Divvy bike stations
for _, station in divvy_df.iterrows():
    station_name = station['Station Name']
    lat = station['Latitude']
    lon = station['Longitude']
    docks = station['Total Docks']
    folium.Marker(
        location=[lat, lon],
        popup=f"🚲 {station_name}<br>Total Docks: {docks}",
        icon=folium.Icon(color='cadetblue', icon='bicycle', prefix='fa')
    ).add_to(m)

# Add listings within 3.0 miles of UIC only
for _, row in df.iterrows():
    address = row['address']
    price = row['price']
    lat = row['latitude']
    lon = row['longitude']
    sqft = row.get('livingArea', 0) or 0
    furnished = 'Yes' if 'furnished' in address.lower() else 'No'
    pets = 'Yes' if 'pet' in address.lower() else 'Unknown'

    distance_to_uic = geodesic((lat, lon), uic_location).miles
    if distance_to_uic > 3.0:
        continue

    if price < 1000:
        color = 'green'
        score = "Great Deal 💸"
    elif price < 1800:
        color = 'orange'
        score = "Fair Value ✅"
    else:
        color = 'red'
        score = "Pricey 🚨"

    diff = price - avg_price
    percent_diff = (diff / avg_price) * 100

    if percent_diff < -10:
        comparison = f"{abs(percent_diff):.1f}% below city average 📉"
    elif percent_diff > 10:
        comparison = f"{abs(percent_diff):.1f}% above city average 📈"
    else:
        comparison = "Near city average ⚖️"

    street_view_url = f"https://www.google.com/maps?q=&layer=c&cbll={lat},{lon}"
    distance_str = f"{distance_to_uic:.2f} miles from UIC 📍"
    cost_per_sqft = f"${(price / sqft):.2f}/sqft" if sqft > 0 else "N/A"
    affordability = (price / 1400) * 100
    budget_msg = f"{affordability:.0f}% of $1400 budget"
    budget_flag = "✅ Affordable" if affordability <= 100 else "🚨 Over Budget"

    nearest_divvy = divvy_df.loc[divvy_df.apply(lambda x: geodesic((lat, lon), (x['Latitude'], x['Longitude'])).miles, axis=1).idxmin()]
    nearest_amenity = min(amenities, key=lambda x: geodesic((lat, lon), (x['lat'], x['lon'])).miles)

    popup_text = f"""
    <div style='width: 260px; font-family: Arial, sans-serif;'>
        <img src="{row['imgSrc']}" style="width:100%; height:auto; border-radius:5px; margin-bottom:8px;" />
        <b>Address:</b> {address}<br>
        <b>Price:</b> ${price:,.0f}<br>
        <b>Score:</b> {score}<br>
        <b>Comparison:</b> {comparison}<br>
        <b>Distance:</b> {distance_str}<br>
        <b>Sq Ft Price:</b> {cost_per_sqft}<br>
        <b>Furnished:</b> {furnished}<br>
        <b>Pet-Friendly:</b> {pets}<br>
        <b>Budget Fit:</b> {budget_msg} - {budget_flag}<br>
        <b>Nearest Divvy:</b> {nearest_divvy['Station Name']}<br>
        <b>Nearest Amenity:</b> {nearest_amenity['name']} ({nearest_amenity['type']})<br>
        <a href="{street_view_url}" target="_blank" style="color:blue; font-weight:bold;">🏙️ View Street</a>
    </div>
    """

    folium.CircleMarker(
        location=[lat, lon],
        radius=7,
        color=color,
        fill=True,
        fill_opacity=0.8,
        popup=folium.Popup(popup_text, max_width=280)
    ).add_to(m)

    folium.PolyLine(
        locations=[[lat, lon], uic_location],
        color="blue",
        dash_array="5, 10",
        weight=1.5,
        opacity=0.7
    ).add_to(m)

    folium.PolyLine(
        locations=[[lat, lon], [nearest_divvy['Latitude'], nearest_divvy['Longitude']]],
        color="cadetblue",
        dash_array="1, 6",
        weight=1,
        opacity=0.5
    ).add_to(m)

    folium.PolyLine(
        locations=[[lat, lon], [nearest_amenity['lat'], nearest_amenity['lon']]],
        color="gray",
        dash_array="2, 6",
        weight=1,
        opacity=0.5
    ).add_to(m)

legend_html = f'''
<div style="
    position: fixed;
    bottom: 30px;
    left: 30px;
    width: 320px;
    background-color: rgba(255, 255, 255, 0.95);
    border: 2px solid #444;
    z-index: 9999;
    font-size: 14px;
    font-family: Arial, sans-serif;
    padding: 15px;
    border-radius: 10px;
    box-shadow: 3px 3px 10px rgba(0,0,0,0.3);
    line-height: 1.6;
">
<h4 style="margin-top: 0; font-size: 18px;">🗺️ Rental Score + Student View</h4>
<p style="margin: 0;">
    <span style="color:green; font-weight: bold;">● Under $1000:</span> Great Deal 💸<br>
    <span style="color:orange; font-weight: bold;">● $1000–$1799:</span> Fair Value ✅<br>
    <span style="color:red; font-weight: bold;">● $1800+:</span> Pricey 🚨
</p>
<hr style="margin: 10px 0;">
<p style="font-size: 13px; color: #555;">
    📍 UIC Proximity: only listings within 3.0 miles shown.<br>
    🛍️ Amenities nearby include grocery stores, libraries, gyms, CTA, and Divvy Bike Stations.<br>
    💰 Budget benchmark = $1400/mo for affordability estimate.<br>
    🔷 Blue line = to UIC, 🟦 Light Blue = to Divvy, 🔘 Gray = to nearest amenity.
</p>
</div>
'''
m.get_root().html.add_child(folium.Element(legend_html))

m.save("real_estate_map.html")
print("✅ Map updated with interactive proximity lines to UIC, Divvy, and nearest amenities!")
