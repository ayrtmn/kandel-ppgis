# PPGIS Kandel Game

An interactive negotiation game about solar panels, farmland, and the future of energy in Kandel, Germany.

Based on: **Rösch & Fakharizadehshirazi (2025)** — *Public Participation GIS Scenarios for Decision-Making on Land-Use Requirements for Renewable Energy Systems*

---

## 📁 Files

| File | Description |
|------|-------------|
| `kandel-game.html` | Interactive scoring tool (50 hexes, 4 stakeholder groups) |
| `kandel-game-data.csv` | QGIS-compatible voting data |
| `kandel-hex-map.png` | Hex map image |
| `kandel-a4-web.jpg` | A4 web version of map |
| `rosch-fakharizadehshirazi-2025-ppgis-scenarios-renewable-energy.pdf` | Original research paper |

---

## 🎮 Play the Game

**Live:** https://ayrtmn.github.io/kandel-ppgis/kandel-game.html

### How to Play

1. **Background** — Read the story and land types
2. **Configuration** — Adjust scoring values (optional)
3. **Game Board** — Vote on 50 hexes:
   - **Restrict** = Protect from PV
   - **Prefer** = Build PV there
4. **Results** — View consensus and conflicts

### Stakeholder Groups

| Group | Focus |
|-------|-------|
| 🌾 **Farmer** | Protect agricultural land |
| 🏠 **Citizen** | Protect residential areas |
| 🏭 **Industry** | Maximize PV efficiency (road access) |
| 🌳 **Environment** | Protect forests and ecology |

---

## 🗺️ Land Types

| Land Type | Hexes | Value |
|-----------|-------|-------|
| Forest | 12 | High ecology, visual |
| Arable Land | 10 | Food production |
| Productive Agriculture | 8 | Premium soil |
| Settlement | 8 | Residential |
| Grassland | 7 | Moderate ecology |
| Sealed | 5 | Already paved |

---

## 📊 CSV Format (QGIS-compatible)

```csv
hex_id,land_use,road,farmer_suitable,farmer_restricted,citizen_suitable,citizen_restricted,industry_suitable,industry_restricted,env_suitable,env_restricted
A6,arrable_land,false,false,false,false,false,false,false,false,false
B6,arrable_land,false,false,true,false,false,false,false,false,false
```

---

## 📚 Source

**Rösch, C. & Fakharizadehshirazi, E. (2025).** Public participation GIS scenarios for decision-making on land-use requirements for renewable energy systems. *Energy, Sustainability and Society*, 15:18.

DOI: [10.1186/s13705-025-00518-y](https://doi.org/10.1186/s13705-025-00518-y)

---

## License

Educational use only.
