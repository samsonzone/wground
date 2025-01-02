
# **Weather Station Observation Script**  

## **Overview**  
This Python script fetches real-time weather data from the Weather Underground API for a specified weather station. It displays the data in a terminal-friendly format with colored outputs to enhance readability.

---

## **Features**  
- Displays temperature, humidity, wind speed, wind gusts, pressure, and precipitation.  
- Dynamically calculates **"Feels Like"** temperature (Wind Chill or Heat Index).  
- Uses **Colorama** for color-coded outputs based on thresholds.  
- Supports automatic dependency installation.  
- Compatible with **Ubuntu 24.04** and other Linux distributions.  

---

## **Requirements**  
- Python 3.x  
- `requests` library  
- `colorama` library  

---

## **Setup Instructions**  

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/your-username/weather-observation-script.git
   cd weather-observation-script
   ```

2. **Install Dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Execute Permissions**  
   ```bash
   chmod +x weather.py
   ```

4. **Run the Script**  
   ```bash
   ./weather.py
   ```

---

## **Configuration**  
- Update the **API Key** and **Station ID** in the script if needed:  
  ```python
  API_KEY = "your-api-key-here"
  STATION_ID = "your-station-id-here"
  ```

---

## **Example Output**  

```
WEATHER STATION OBSERVATION
---------------------------
Observation Time:  2024-01-01 10:30 AM
Location:          New York City, NY (Station ID)
Hardware:          myAcuRite

Temperature:       45.2°F
Feels like:        42.5°F
Dew Point:         39.5°F
Humidity:          85%
Wind:              NW @ 12.0 mph (Gusts @ 15.5 mph)
Highest Gust:      20.5 mph
Pressure:          29.85 inHg
Precip Rate:       0.05 in/hr
Precip Total:      0.25 in
```

---

## **Error Handling**  
- If any API or network errors occur, the script displays an error message and exits gracefully.  

---

## **License**  
This project is licensed under the **MIT License**. See the **LICENSE** file for more details.  

---

## **Contributions**  
Contributions are welcome! Feel free to fork the repository and submit pull requests.  
