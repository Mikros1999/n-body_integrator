import math
import time
import random
import sys
from multiprocessing import Process




#pravi klasu tacka koja sadrzi koordinate
class point:
    def __init__(self, x,y,z):
        self.x = x
        self.y = y
        self.z = z



#pravi klasu telo (body) koja ima lokaciju, masu, brzinu, ime
class body:
    def __init__(self, location, mass, velocity, name = ""):
        self.location = location
        self.mass = mass
        self.velocity = velocity
        self.name = name



#Ova funkcija uzima listu tela, i indeks tela koje posmatramo (target_body). 
#Onda prolazimo kroz sva druga tela i dodajemo ubrzanje posmatranom telu (target_body-ju)
def calculate_single_body_acceleration(bodies, body_index):
    G_const = 6.67408e-11 #m3 kg-1 s-2
    acceleration = point(0,0,0)
    target_body = bodies[body_index]
    for index, external_body in enumerate(bodies):
        if index != body_index:
            r = (target_body.location.x - external_body.location.x)**2 + (target_body.location.y - external_body.location.y)**2 + (target_body.location.z - external_body.location.z)**2
            r = math.sqrt(r)
            tmp = G_const * external_body.mass / r**3
            acceleration.x += tmp * (external_body.location.x - target_body.location.x)
            acceleration.y += tmp * (external_body.location.y - target_body.location.y)
            acceleration.z += tmp * (external_body.location.z - target_body.location.z)

    return acceleration



#Kada znamo ubrzanje prelazimo na sledeci korak, a to je racunanje brzine
#Novu brzinu racunamo mnozenjem ubrzanja (acceleration) sa vremenskim korakom (time_step) i dodavanjem toga na trenutnu brzinu
def compute_velocity(bodies, time_step = 1):
    for body_index, target_body in enumerate(bodies):
        acceleration = calculate_single_body_acceleration(bodies, body_index)

        target_body.velocity.x += acceleration.x * time_step
        target_body.velocity.y += acceleration.y * time_step
        target_body.velocity.z += acceleration.z * time_step 



#kad su sve brzine apdejtovane, mozemo promeniti poziciju svih tela 
#to radimo tako sto racunamo duzinu koju su presli u vremenskom koraku (velocity x time) i dodavanjem toga na trenutnu poziciju
def update_location(bodies, time_step = 1):
    for target_body in bodies:
        target_body.location.x += target_body.velocity.x * time_step
        target_body.location.y += target_body.velocity.y * time_step
        target_body.location.z += target_body.velocity.z * time_step




#prethodne dve funkcije mozemo smestiti u jednu
def compute_gravity_step(bodies, time_step = 1):
    compute_velocity(bodies, time_step = time_step)
    update_location(bodies, time_step = time_step)


#Dok traje simulacija jedina neophodna informacija je x,y,z koordinate nasih tela.
#Da bismo pokrenuli simulaciju ponavljati ove gore kalkulacije zeljeni broj puta i sacuvati istoriju lokacija
def run_simulation(bodies, names = None, time_step = 1, number_of_steps = 10000, report_freq = 100):

    body_locations_hist = []
    for current_body in bodies:
        body_locations_hist.append({"x":[], "y":[], "z":[], "name":current_body.name})
        
    for i in range(1,number_of_steps):
        compute_gravity_step(bodies, time_step = 1000)            
        
        if i % report_freq == 0:
            for index, body_location in enumerate(body_locations_hist):
                body_location["x"].append(bodies[index].location.x)
                body_location["y"].append(bodies[index].location.y)           
                body_location["z"].append(bodies[index].location.z)       

    return body_locations_hist



#podaci o planetama (lokacija (m), masa (kg), brzina (m/s)
sun = {"location":point(0,0,0), "mass":2e30, "velocity":point(0,0,0)}
mercury = {"location":point(0,5.7e10,0), "mass":3.285e23, "velocity":point(47000,0,0)}
venus = {"location":point(0,1.1e11,0), "mass":4.8e24, "velocity":point(35000,0,0)}
earth = {"location":point(0,1.5e11,0), "mass":6e24, "velocity":point(30000,0,0)}
mars = {"location":point(0,2.2e11,0), "mass":2.4e24, "velocity":point(24000,0,0)}
jupiter = {"location":point(0,7.7e11,0), "mass":1e28, "velocity":point(13000,0,0)}
saturn = {"location":point(0,1.4e12,0), "mass":5.7e26, "velocity":point(9000,0,0)}
uranus = {"location":point(0,2.8e12,0), "mass":8.7e25, "velocity":point(6835,0,0)}
neptune = {"location":point(0,4.5e12,0), "mass":1e26, "velocity":point(5477,0,0)}
pluto = {"location":point(0,3.7e12,0), "mass":1.3e22, "velocity":point(4748,0,0)}




if __name__ == "__main__":

#lista planeta koje zelimo u simulaciji

    bodies = [ [
        body( location = sun["location"], mass = sun["mass"], velocity = sun["velocity"], name = "sun"),
        body( location = earth["location"], mass = earth["mass"], velocity = earth["velocity"], name = "earth"),
        body( location = mars["location"], mass = mars["mass"], velocity = mars["velocity"], name = "mars"),
        body( location = venus["location"], mass = venus["mass"], velocity = venus["velocity"], name = "venus"),
        body( location = mercury["location"], mass = mercury["mass"], velocity = mercury["velocity"], name = "mercury"),
        body( location = jupiter["location"], mass = jupiter["mass"], velocity = jupiter["velocity"], name = "jupiter"),
        body( location = saturn["location"], mass = saturn["mass"], velocity = saturn["velocity"], name = "saturn"),
        body( location = uranus["location"], mass = uranus["mass"], velocity = uranus["velocity"], name = "uranus"),
        body( location = neptune["location"], mass = neptune["mass"], velocity = neptune["velocity"], name = "neptune"),
        body( location = pluto["location"], mass = pluto["mass"], velocity = pluto["velocity"], name = "pluto"),
        ],
        [
        #body( location = sun["location"], mass = sun["mass"], velocity = sun["velocity"], name = "sun"),
        #body( location = earth["location"], mass = earth["mass"], velocity = earth["velocity"], name = "earth"),
        #body( location = mars["location"], mass = mars["mass"], velocity = mars["velocity"], name = "mars"),
        #body( location = venus["location"], mass = venus["mass"], velocity = venus["velocity"], name = "venus"),
        #body( location = mercury["location"], mass = mercury["mass"], velocity = mercury["velocity"], name = "mercury"),
        #body( location = jupiter["location"], mass = jupiter["mass"], velocity = jupiter["velocity"], name = "jupiter"),
        #body( location = saturn["location"], mass = saturn["mass"], velocity = saturn["velocity"], name = "saturn"),
        #body( location = uranus["location"], mass = uranus["mass"], velocity = uranus["velocity"], name = "uranus"),
        #body( location = neptune["location"], mass = neptune["mass"], velocity = neptune["velocity"], name = "neptune"),
        #body( location = pluto["location"], mass = pluto["mass"], velocity = pluto["velocity"], name = "pluto"),
        ],
	]
         
#normalno pokretanje
    poc = time.time()

    motions = run_simulation(bodies[0], time_step = 100, number_of_steps = 80000, report_freq = 1000)
    
    print('bez paral: ', time.time() - poc, 's')

#paralelizacija
    poc = time.time()

    p = Process(target = run_simulation, args = bodies)
    p.start()
    p.join()
    

    print('sa paral: ', time.time() - poc, 's')
    

