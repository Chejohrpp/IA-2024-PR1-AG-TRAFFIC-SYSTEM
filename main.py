import sys
from views.principal.menu import MyApp

if __name__ == "__main__":
        app = MyApp(application_id="com.hrp.TrafficManagement")
        app.run(sys.argv)
