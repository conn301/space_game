import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivy.properties import NumericProperty, BooleanProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
import math
# import mysql.connecter

kivy.require('1.11.0')


# ===================== CONFIG =======================#

Window.fullscreen = True

# ===================== SCREENS ======================#


class Database():
    isAuthenticated = BooleanProperty(False)
    isError = BooleanProperty(False)
    isWrong = BooleanProperty(False)

    global connection
    # connection = mysql.connector.connect(user='root', password='efsiRu1es',
    #                                      host='127.0.0.1',
    #                                      database='world')

    def connect_to_DB(self, username, password):

        c = connection.cursor()

        if username == "" and password == "":
                            exit()

        try:
            c.execute("SELECT * FROM persons WHERE FirstName = \"{}\"".format(username))

            for column in c:
                pass

            if password == column[3]:
                print("Correct Password")
                self.isAuthenticated = True
            else:
                print("Incorrect Password")
                self.isWrong = True

        except UnboundLocalError:
            self.isError = True
            print("ERROR")

        #connection.close()
        # print("You connected to the database successfully.")

    def user_account(self, first, last, username, password):

        c = connection.cursor()
        c.execute("INSERT INTO persons (PersonId, LastName, FirstName, Address) VALUES (%s, %s, %s, %s)", (first, last, username, password))
        connection.commit()
        print(first)
        print(last)
        print(username)
        print(password)


class LogIn(Screen, Database):
    pass


class Register(Screen, Database):
    pass


class GameMenu(Screen, Database):
    pass


# ===================== DATABASE ======================#
class SpaceArena(Screen):
    ship = ObjectProperty(None)
    bonus_1 = ObjectProperty(None)
    # wall = ObjectProperty(None)

    def setup(self):
        self.ship.fuel = 15

    def update(self, dt):
        self.ship.move()
        # Bonus.gather(self.bonus_1)

        if self.ship.collide_widget(self.bonus_1):
            self.ship.fuel = 15

    def on_touch_up(self, touch):
        # if (touch.x)
        if self.ship.fuel > 0:
            old_x, old_y = self.ship.velocity
            new_x, new_y = (touch.x-self.ship.x)/100, (touch.y-self.ship.y)/100
            self.ship.velocity = Vector(old_x + new_x, old_y + new_y)
            x, y = self.ship.velocity
            theta = math.degrees(math.atan(x / y))
            self.ship.angle = float(theta)
            # self.ship.canvas.ask_()

            print()
            print(self.ship.angle)
            print(theta)
            print(self.ship.angle)

            self.ship.fuel -= ((touch.x-self.ship.x)**2 + (touch.x-self.ship.x)**2)**(1/2) / 400

        if self.ship.fuel < 0:
            self.ship.fuel = 0

    def quit(self):
        exit(1)

    def games(self):
        # game = SpaceArena()
        self.remove_widget(self.play)
        print("test2")
        self.setup()
        Clock.schedule_interval(self.update, 1.0 / 60.0)
        return self


class YouLose(Screen):
    def quit(self):
        exit(1)

# ===================== APP ======================#


class ApolloApp(App):
    pass

# ====================== WIDGETS ========================#


class Ship(Widget):
    fuel = NumericProperty(0)
    vel_x = NumericProperty(0)
    vel_y = NumericProperty(0)
    velocity = ReferenceListProperty(vel_x, vel_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos
        # print("moving")
        # print(self.velocity)


class Bonus(Widget):
    pass


class Wall(Widget):
    pass


# ====================== BUILD =======================#


class ScreenManagement(ScreenManager):
    pass


presentation = Builder.load_file("Apollo.kv")


if __name__ == '__main__':
    ApolloApp().run()