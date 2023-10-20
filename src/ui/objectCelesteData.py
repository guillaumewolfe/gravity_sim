CELESTIAL_PARAMETERS = [
    {
        "name": "Soleil",
        "type": 1,
        "relation": "Soleil",
        "real_distance": 0,  # Le Soleil est le point de référence
        "real_radius": 696_340e3,  # en mètres
        "weight": 1.989e30,  # en kg
        "velocity": [0, 0, 0],  # Le Soleil est le point de référence
        "accel": [0, 0, 0],
        "inclinaison": 7.25,
        "rotation_siderale_angle": 0,
        "rotation_siderale_vitesse": 1/300,
        "rotation_siderale_direction": [0,1,0],
        "texture_path": "assets/textures/sun.jpg"
    },
    {
        "name": "Terre",
        "type": 2,
        "relation": "Soleil",
        "real_distance": 149_597_870e3,  # en mètres
        "real_radius": 6371e3,  # en mètres
        "weight": 5.972e24,  # en kg
        "velocity": [0, 0, -29.78e3],  # en m/s, supposons que la vitesse soit dans la direction x pour simplifier
        "accel": [0, 0, 0],
        "inclinaison": 0,#23.5
        "rotation_siderale_angle": 0,
        "rotation_siderale_vitesse": 360/86400,
        "rotation_siderale_direction": [0,1,0],
        "texture_path": "assets/textures/earth_real.jpg"
    },
    {
        "name": "Mars",
        "type": 2,
        "relation": "Soleil",
        "real_distance": 225_000_000e3,  # en mètres
        "real_radius": 3390e3,  # en mètres
        "weight": 6.417e23,  # en kg
        "velocity": [0, 0, -24e3],  # en m/s, supposons que la vitesse soit dans la direction x pour simplifier
        "accel": [0, 0, 0],
        "inclinaison": 25.19,
        "rotation_siderale_angle": 0,
        "rotation_siderale_vitesse": 1/246,
        "rotation_siderale_direction": [0,1,0],
        "texture_path": "assets/textures/mars.jpg"
    },
    {
        "name": "Mercure",
        "type": 2,
        "relation": "Soleil",
        "real_distance": 57_909_175e3,
        "real_radius": 2439.7e3,
        "weight": 3.301e23,
        "velocity": [0, 0, -47.87e3],
        "accel": [0, 0, 0],
        "inclinaison": 0.034,
        "rotation_siderale_angle": 0,
        "rotation_siderale_vitesse": 1/5064,
        "rotation_siderale_direction": [0, 1, 0],
        "texture_path": "assets/textures/mercure.jpg"
    },
    {
        "name": "Venus",
        "type": 2,
        "relation": "Soleil",
        "real_distance": 108_208_930e3,
        "real_radius": 6051.8e3,
        "weight": 4.867e24,
        "velocity": [0, 0, -35.02e3],
        "accel": [0, 0, 0],
        "inclinaison": 177.4,
        "rotation_siderale_angle": 0,
        "rotation_siderale_vitesse": 1/5832,
        "rotation_siderale_direction": [0, -1, 0], # Vénus tourne dans le sens opposé
        "texture_path": "assets/textures/venus2.jpg"
    },
    {
        "name": "Jupiter",
        "type": 2,
        "relation": "Soleil",
        "real_distance": 778_340_821e3,
        "real_radius": 69911e3,
        "weight": 1.898e27,
        "velocity": [0, 0, -13.07e3],
        "accel": [0, 0, 0],
        "inclinaison": 3.13,
        "rotation_siderale_angle": 0,
        "rotation_siderale_vitesse": 0.0101,
        "rotation_siderale_direction": [0, 1, 0],
        "texture_path": "assets/textures/jupiter.jpg"
    },
    {
        "name": "Uranus",
        "type": 2,
        "relation": "Soleil",
        "real_distance": 2_870_658_186e3,
        "real_radius": 25362e3,
        "weight": 8.681e25,
        "velocity": [0, 0, -6.8e3],
        "accel": [0, 0, 0],
        "inclinaison": 97.77,
        "rotation_siderale_angle": 0,
        "rotation_siderale_vitesse": 0.0058,
        "rotation_siderale_direction": [0, 1, 0],
        "texture_path": "assets/textures/uranus.jpg"
    },
    {
        "name": "Saturne",
        "type": 2,
        "relation": "Soleil",
        "real_distance": 1_426_666_422e3,
        "real_radius": 58232e3,
        "weight": 5.683e26,
        "velocity": [0, 0, -9.68e3],
        "accel": [0, 0, 0],
        "inclinaison": 26.73,
        "rotation_siderale_angle": 0,
        "rotation_siderale_vitesse": 0.0093,
        "rotation_siderale_direction": [0, 1, 0],
        "texture_path": "assets/textures/saturn.jpg"
    },
    {
        "name": "Neptune",
        "type": 2,
        "relation": "Soleil",
        "real_distance": 4_498_396_441e3, 
        "real_radius": 24622e3,
        "weight": 1.024e26,
        "velocity": [0, 0, -5.43e3],
        "accel": [0, 0, 0],
        "inclinaison": 28.32,
        "rotation_siderale_angle": 0,
        "rotation_siderale_vitesse": 0.0062,
        "rotation_siderale_direction": [0, 1, 0],
        "texture_path": "assets/textures/neptune.jpg"
    },
]












"""

CELESTIAL_PARAMETERS.extend([
    {
        "name": "Mercure",
        "relation": "Soleil",
        "real_distance": 57_909_175e3,
        "real_radius": 2439.7e3,
        "weight": 3.301e23,
        "velocity": [0, 47.87e3, 0],
        "accel": [0, 0, 0],
        "inclinaison": 0.034,
        "rotation_siderale_angle": 0,
        "rotation_siderale_vitesse": 1/5064,
        "rotation_siderale_direction": [0, 1, 0],
        "texture_path": "assets/textures/mercury.jpg"
    },
    {
        "name": "Vénus",
        "relation": "Soleil",
        "real_distance": 108_208_930e3,
        "real_radius": 6051.8e3,
        "weight": 4.867e24,
        "velocity": [0, 35.02e3, 0],
        "accel": [0, 0, 0],
        "inclinaison": 177.4,
        "rotation_siderale_angle": 0,
        "rotation_siderale_vitesse": 1/5832,
        "rotation_siderale_direction": [0, -1, 0], # Vénus tourne dans le sens opposé
        "texture_path": "assets/textures/venus.jpg"
    },
    {
        "name": "Jupiter",
        "relation": "Soleil",
        "real_distance": 778_340_821e3,
        "real_radius": 69911e3,
        "weight": 1.898e27,
        "velocity": [0, 13.07e3, 0],
        "accel": [0, 0, 0],
        "inclinaison": 3.13,
        "rotation_siderale_angle": 0,
        "rotation_siderale_vitesse": 1/9.93,
        "rotation_siderale_direction": [0, 1, 0],
        "texture_path": "assets/textures/jupiter.jpg"
    },
    {
        "name": "Saturne",
        "relation": "Soleil",
        "real_distance": 1_426_666_422e3,
        "real_radius": 58232e3,
        "weight": 5.683e26,
        "velocity": [0, 9.68e3, 0],
        "accel": [0, 0, 0],
        "inclinaison": 26.73,
        "rotation_siderale_angle": 0,
        "rotation_siderale_vitesse": 1/10.7,
        "rotation_siderale_direction": [0, 1, 0],
        "texture_path": "assets/textures/saturn.jpg"
    },
    {
        "name": "Uranus",
        "relation": "Soleil",
        "real_distance": 2_870_658_186e3,
        "real_radius": 25362e3,
        "weight": 8.681e25,
        "velocity": [0, 6.8e3, 0],
        "accel": [0, 0, 0],
        "inclinaison": 97.77,
        "rotation_siderale_angle": 0,
        "rotation_siderale_vitesse": 1/17.2,
        "rotation_siderale_direction": [0, 1, 0],
        "texture_path": "assets/textures/uranus.jpg"
    },
    {
        "name": "Neptune",
        "relation": "Soleil",
        "real_distance": 4_498_396_441e3,
        "real_radius": 24622e3,
        "weight": 1.024e26,
        "velocity": [0, 5.43e3, 0],
        "accel": [0, 0, 0],
        "inclinaison": 28.32,
        "rotation_siderale_angle": 0,
        "rotation_siderale_vitesse": 1/16,
        "rotation_siderale_direction": [0, 1, 0],
        "texture_path": "assets/textures/neptune.jpg"
    }
])

autre = [
    {
        "name": "Lune",
        "type": 2,
        "relation": "Terre",
        "real_distance": 384400e3,  # en mètres
        "real_radius": 1737.5e3,  # en mètres
        "weight": 7.342e22,  # en kg
        "velocity": [0, -1.022e3, -29.78e3],  # en m/s, supposons que la vitesse soit dans la direction x pour simplifier
        "accel": [0, 0, 0],
        "inclinaison": 0,
        "rotation_siderale_angle": 0,
        "rotation_siderale_vitesse": 0,
        "rotation_siderale_direction": [0,0,0],
        "texture_path": "assets/textures/lunar.jpg"
    }
]"""