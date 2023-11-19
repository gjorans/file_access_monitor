import time
import picod
import pyinotify


# Define pin
GPIO_PIN = 7
pico = picod.pico()

pico.reset()  # Put Pico into a clean state

# Define the path to the file you want to monitor
file_path = "/home/user/harddrive.img"

# Set up inotify
wm = pyinotify.WatchManager()
mask = pyinotify.IN_ACCESS


class EventHandler(pyinotify.ProcessEvent):
    def process_default(self, event):
        if event.pathname == file_path and event.mask & pyinotify.IN_ACCESS:
            pico.gpio_write(GPIO_PIN, 1)
            # print(1) #enable for visual output of current status
            time.sleep(0.7)
            pico.gpio_write(GPIO_PIN, 0)
            # print(0) #enable for visual output of current status


# Initialize the inotify watcher
notifier = pyinotify.Notifier(wm, EventHandler())

# Add the file to the watch list
wm.add_watch(file_path, mask)

try:
    while True:
        notifier.process_events()
        notifier.check_events()
        notifier.read_events()
        time.sleep(0.05)  # wait in seconds
except KeyboardInterrupt:
    pass
finally:
    # Stop the notifier
    notifier.stop()
