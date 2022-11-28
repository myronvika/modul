from datetime import datetime
from typing import List, Any
from dataclasses import dataclass
from abc import ABC, abstractmethod
import random
from collections import defaultdict
import json
import requests
import mysql.connector as connection

mydb = connection.connect(host="localhost", user="root", passwd="GBMgbm2200!", use_pure=True)


class InfoStation:

    def __init__(self, id: int, title: str, x, y):
        self.id = id
        self.title = title
        self.x = x
        self.y = y

    @abstractmethod
    def personal_manage(self):
        pass


class Station(InfoStation):
    def __init__(self, id: int, title: str, x, y):
        self.id = id
        self.title = title
        self.x = x
        self.y = y
        self.transports = []


class Depo(InfoStation):
    def __init__(self, id: int, title: str, x, y):
        self.id = id
        self.title = title
        self.x = x
        self.y = y

    def route_manage(self, town_a, town_b, distance, truck):
        pass

    def personal_manage(self, passengers, staff):
        pass


class Transport:
    def __init__(self, title, max_size_of_passengers):
        self.title = title
        self.passengers = []


class Train(Transport):
    None


class Bus(Transport):
    None


class Truck(Transport):
    None


class Schedule:
    def __init__(self, title):
        self.title = title
        self.grafik = defaultdict(list)

    def print_schedule(self):
        print(self.grafik)


class Route:
    def __init__(self, schedule: Schedule):
        self.route_dict = defaultdict(list)
        self.schedule = schedule

    def route_create(self, transport, station_a, station_b):
        self.url_info = requests.get(
            f"https://api.tomtom.com/routing/1/calculateRoute/{station_a.x},{station_a.y}:{station_b.x},{station_b.y}/json?key=lxQBgFn2k02GNm9w5XBmGcrQhZaQmzBQ").text
        self.route_info = json.loads(self.url_info)

        self.route_dict[transport.title].append(station_a.title)
        self.route_dict[transport.title].append(station_b.title)

        self.schedule.grafik[transport.title].append(station_a.title)
        self.schedule.grafik[transport.title].append(self.route_info['routes'][0]['summary']['departureTime'])
        self.schedule.grafik[transport.title].append(station_b.title)
        self.schedule.grafik[transport.title].append(self.route_info['routes'][0]['summary']['arrivalTime'])


class Casa:
    def __init__(self):
        self.lisst = defaultdict(list)

    def buy_ticket(self, client, station_a, station_b):
        self.lisst[client].append(station_a)
        transport = station_a.transports[0]
        transport.passengers.append(client)


class Person:
    def __init__(self, name):
        self.surname = name
        self.lisst = []

    def buy_ticket(self, station_a, station_b, transport):
        transport.passengers.append(self.surname)
        self.lisst.append(transport.title)


class DatabaseConnect:
    def connect(self, person, station_a, station_b, transport, time_departure, time_arrive):
        con = connection.connect(host="localhost", user="root", password="GBMgbm2200!", use_pure=True)
        query = f"use module;"
        cursor = con.cursor()
        cursor.execute(query)
        print(cursor.fetchall())
        query1 = f"insert into schedule values ('{person.surname}','{station_a.title}','{station_b.title}','{transport.title}','{time_departure}','{time_arrive}'); "
        cursor = con.cursor()
        cursor.execute(query1)
        print(cursor.fetchall())
        con.commit()


sch = Schedule('damn')
station_1 = Station(1, 'Ternopil', 49.5535, 25.5948)
station_2 = Depo(2, 'lviv', 49.8397, 24.0297)
bogdan = Bus('bus', 19)
station_4 = Station(1, 'darn', 49.5535, 25.5948)
station_3 = Depo(2, 'dnipro', 49.8397, 24.0297)
bogdan2 = Train('express', 15)
chel_1 = Person('NONAME')

route1 = Route(sch)
route1.route_create(vika, station_1, station_2)
route1.route_create(vika1, station_3, station_4)

chel_1.buy_ticket(station_1, station_2, vika1)

DatabaseConnect()



