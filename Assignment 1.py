import requests
import pandas as pd
import matplotlib.pyplot as plt

# Fetch Mars temperature data
API_KEY = "Bs6r5hTZvhBuwhgWELgaCyHzpBW5nen1NuwhO6EZ"
mars_url = f"https://api.nasa.gov/insight_weather/?api_key={API_KEY}&feedtype=json&ver=1.0"
mars_data = requests.get(mars_url).json()

# Process Mars temperatures
mars_temps = [
    (int(sol), 
     mars_data[sol]["AT"]["mn"], 
     mars_data[sol]["AT"]["mx"]
     )
    for sol in mars_data["sol_keys"] if "AT" in mars_data[sol]
]
mars_df = pd.DataFrame(mars_temps, columns=["Sol", "Min_Temp", "Max_Temp"])
mars_df["Day"] = range(1, len(mars_df) + 1)

# Fetch Earth temperature data (Los Angeles)
earth_url = "https://api.open-meteo.com/v1/forecast?latitude=34.05&longitude=-118.25&daily=temperature_2m_min,temperature_2m_max&timezone=auto"
earth_data = requests.get(earth_url).json()

# Process Earth temperatures
earth_df = pd.DataFrame({
    "Day": range(1, len(earth_data["daily"]["temperature_2m_min"]) + 1),
    "Min_Temp": earth_data["daily"]["temperature_2m_min"],
    "Max_Temp": earth_data["daily"]["temperature_2m_max"]
})

# Match data lengths
earth_df = earth_df.iloc[:len(mars_df)]

# Plot Mars and Earth temperatures
plt.plot(mars_df["Day"], mars_df["Min_Temp"], label = "Mars Min", color = 'blue', marker = 'o')
plt.plot(mars_df["Day"], mars_df["Max_Temp"], label = "Mars Max", color = 'red', marker = 'o')
plt.plot(earth_df["Day"], earth_df["Min_Temp"], label = "Earth Min", color = 'green', marker = 's')
plt.plot(earth_df["Day"], earth_df["Max_Temp"], label = "Earth Max", color = 'orange', marker = 's')

# Customize plot
plt.xlabel("Day")
plt.ylabel("Temperature (°C)")
plt.title("Mars vs. Earth Temperature Comparison")
plt.legend()
plt.grid(True, linestyle="--")
plt.show()
