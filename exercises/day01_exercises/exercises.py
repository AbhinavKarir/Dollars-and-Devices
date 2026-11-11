recycling_materials = ("Copper", "Aluminum", "Gold", "Silver", "Titanium","Platic")
print("Recycling Material:", recycling_materials)
for material in recycling_materials:
    print("Recovering: ", material)
tonnes_recovered = {"Copper": 12.5, "Aluminum": 8.3, "Gold": 0.5, "Silver": 1.2, "Titanium": 2.0, "Plastic": 15.0}
for material in tonnes_recovered:
    print(material, "->", tonnes_recovered[material] , "tonnes")
total_tonnes = 0
for tonnes in tonnes_recovered.values():
    total_tonnes = total_tonnes + tonnes
print("Total Tonnes Recovered:", total_tonnes)

    
