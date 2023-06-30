import computervision
import computergraphics

computervision.start()
computergraphics.start()

while computervision.is_window_open() or computergraphics.is_window_open():
    computervision.update()
    computergraphics.update()
    
computervision.end()
computergraphics.end()
