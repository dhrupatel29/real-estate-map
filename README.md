# 🏠 Real Estate Price Heatmap (UIC)

An interactive browser-based map that visualizes Chicago rental prices, trend scores, and proximity to Divvy bike stations. It helps users explore affordable neighborhoods, evaluate investment potential, and understand how access to transport relates to real estate value.

---

<details>
<summary><strong>🌟 Features</strong></summary>

- **Interactive Heatmap**  
  Color-coded regions based on average rental prices — warmer colors = more expensive.

- **Click-to-Reveal Insights**  
  Clicking a region or point reveals:
  - 📍 Neighborhood or zip code
  - 💰 Average monthly rent
  - 📈 1-year rental price trend
  - 🧠 Investment score (e.g. "Good Investment", "Hot Market")

- **Divvy Station Overlay**  
  Visualizes proximity to Divvy bike stations using point markers.

- **CSV & GeoJSON Support**  
  Data loaded from:
  - `Zillow_Chicago_Rental_Data.csv`
  - `Divvy_Bicycle_Stations_20250512.csv`

- **No Backend Required**  
  Fully static project — just open `index.html`.

- **GitHub Pages Ready**  
  Easy to deploy and share live.

</details>

---

<details>
<summary><strong>📊 Scoring Formula</strong></summary>

Each region receives a score based on the following logic:

```plaintext
If (price < city_avg) and (trend > 0)
    → "Good Investment"
Else if (price > city_avg) and (trend > 5%)
    → "Overpriced but Rising"
Else if (trend < 0)
    → "Declining Market"
Else
    → "Stable"
```

You can adjust this logic in your JavaScript based on your target audience or dataset specifics.

</details>

---

<details>
<summary><strong>📂 Data Sources</strong></summary>

- **Zillow Chicago Rental Data**  
  File: `Zillow_Chicago_Rental_Data.csv`  
  Source: [Zillow Research](https://www.zillow.com/research/data/)

- **Divvy Bicycle Station Data**  
  File: `Divvy_Bicycle_Stations_20250512.csv`  
  Source: [City of Chicago Open Data](https://data.cityofchicago.org)

</details>

---

## 🛠 How to Run

```bash
git clone https://github.com/dhrupatel29/real-estate-map.git
cd real-estate-map
```

1. Open `index.html` in your browser  
2. Ensure the CSV files are in the same directory  
3. Customize data or visuals as needed  
4. Deploy to GitHub Pages (Settings → Pages → main branch → `/root`)

---

## 📷 Screenshot

![UIC Real Estate Heatmap](uicrealestate.png)

---

## 🙌 Author

Built by [Dhru Patel](https://github.com/dhrupatel29)  
Data-driven visualizations made simple.

---

