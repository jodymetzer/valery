import RPi.GPIO as GPIO
import time
import sys

GPIO.setmode(GPIO.BOARD)   ##je prefere la numerotation BOARD plutot que BCM

Inter1 = 11
Inter2 = 13
Inter3 = 12
Inter4 = 19

Ultra1Trigger = 24
Ultra1Echo = 22
Ultra2Trigger = 23
Ultra2Echo = 21

Moteur1A = 29
Moteur1B = 31
Moteur1E = 32
Moteur2A = 33
Moteur2B = 35
Moteur2E = 36
Moteur3A = 37
Moteur3B = 38
Moteur3E = 40

# Set pins as output and input
GPIO.setup(Ultra1Trigger,GPIO.OUT)  # Trigger
GPIO.setup(Ultra1Echo,GPIO.IN)      # Echo
# Set pins as output and input
GPIO.setup(Ultra2Trigger,GPIO.OUT)  # Trigger
GPIO.setup(Ultra2Echo,GPIO.IN)      # Echo


GPIO.setup(Inter1,GPIO.IN)
GPIO.setup(Inter2,GPIO.IN)
GPIO.setup(Inter3,GPIO.IN)
GPIO.setup(Inter4,GPIO.IN)

GPIO.setup(Moteur1A,GPIO.OUT)
GPIO.setup(Moteur1B,GPIO.OUT)
GPIO.setup(Moteur1E,GPIO.OUT)
GPIO.setup(Moteur2A,GPIO.OUT)
GPIO.setup(Moteur2B,GPIO.OUT)
GPIO.setup(Moteur2E,GPIO.OUT)
GPIO.setup(Moteur3A,GPIO.OUT)
GPIO.setup(Moteur3B,GPIO.OUT)
GPIO.setup(Moteur3E,GPIO.OUT)

pwm1 = GPIO.PWM(Moteur1E,50)
pwm2 = GPIO.PWM(Moteur2E,50)
pwm3 = GPIO.PWM(Moteur3E,50)

#pwm1.start(100)
#pwm2.start(100)
#pwm3.start(100)

distance1=0

##Debut du programe##

print "Debut de la sequence de scan"
print "######################################################"
print "Mesure de la distance objet scanner"
def capteur1():
	# Set trigger to False (Low)
	# Set pins as output and input
	GPIO.setup(Ultra1Trigger,GPIO.OUT)  # Trigger
	GPIO.setup(Ultra1Echo,GPIO.IN)      # Echo
	GPIO.output(Ultra1Trigger, False)
	
	# Allow module to settle
	time.sleep(0.5)
	
	# Send 10us pulse to trigger
	GPIO.output(Ultra1Trigger, True)
	time.sleep(0.00001)
	GPIO.output(Ultra1Trigger, False)
	start = time.time()
	while GPIO.input(Ultra1Echo)==0:
	  start = time.time()
	
	while GPIO.input(Ultra1Echo)==1:
	  stop = time.time()
	
	# Calculate pulse length
	elapsed = stop-start
	
	# Distance pulse travelled in that time is time
	# multiplied by the speed of sound (cm/s)
	global distance1
	distance1 = elapsed * 34000
	
	# That was the distance there and back so halve the value
	distance1 = distance1 / 2
	
	print "Distance : %.1f" % distance1
	
	# Reset GPIO settings
	GPIO.cleanup()
	return

print "Adaptation de la distance scanner-objet"

pwm1.start(100)

while (distance1 < 38):
	capteur1()
	#Rotation sens negatif, pour s'eloigner de l'objet
	
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(Moteur1A,GPIO.OUT)
	GPIO.setup(Moteur1B,GPIO.OUT)
	GPIO.setup(Moteur1E,GPIO.OUT)
	GPIO.output(Moteur1A,GPIO.LOW)
	GPIO.output(Moteur1B,GPIO.HIGH)
	GPIO.output(Moteur1E,GPIO.HIGH)
	
while (distance1 > 42):
        capteur1()
        #Rotation sens positif, pour se rapprocher de l'objet
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(Moteur1A,GPIO.OUT)
        GPIO.setup(Moteur1B,GPIO.OUT)
        GPIO.setup(Moteur1E,GPIO.OUT)
        GPIO.output(Moteur1A,GPIO.HIGH)
        GPIO.output(Moteur1B,GPIO.LOW)
        GPIO.output(Moteur1E,GPIO.HIGH)


pwm1.stop() ##Plus besoin de la pwm1.


# Set trigger to False (Low)
# Set pins as output and input
GPIO.setup(Ultra2Trigger,GPIO.OUT)  # Trigger
GPIO.setup(Ultra2Echo,GPIO.IN)      # Echo
GPIO.output(Ultra2Trigger, False)

# Allow module to settle
time.sleep(0.5)

# Send 10us pulse to trigger
GPIO.output(Ultra2Trigger, True)
time.sleep(0.00001)
GPIO.output(Ultra2Trigger, False)
start2 = time.time()
while GPIO.input(Ultra2Echo)==0:
  start2 = time.time()

while GPIO.input(Ultra2Echo)==1:
  stop2 = time.time()

# Calculate pulse length
elapsed2 = stop2-start2

# Distance pulse travelled in that time is time
# multiplied by the speed of sound (cm/s)
global distance2
distance2 = elapsed2 * 34000

# That was the distance there and back so halve the value
distance2 = distance2 / 2

print "Distance2 : %.1f" % distance2


print "Scan en cours..."

GPIO.setup(Inter1,GPIO.IN)
GPIO.setup(Inter2,GPIO.IN)
GPIO.setup(Inter3,GPIO.IN)
GPIO.setup(Inter4,GPIO.IN)
#On lance la sequence de scan, en commencant par le tour de plateau tournant
pwm2.start(100)
print "1"
print "Premier Tour de plateau, en attente de l'interrupteur"
while (GPIO.input(Inter1)==False):
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(Moteur2A,GPIO.OUT)
	GPIO.setup(Moteur2B,GPIO.OUT)
	GPIO.setup(Moteur2E,GPIO.OUT)
	GPIO.output(Moteur2A,GPIO.HIGH)
	GPIO.output(Moteur2B,GPIO.LOW)
	GPIO.output(Moteur2E,GPIO.HIGH)

print "Premier tour termine"
pwm2.stop()
print "Montee du scanner a un tiers"
#Un tour a ete effectue, on monte donc le scanner d'un tiers de la hauteur maximale a parcourir
##Il faudra calculer la vitesse de la montee du scanner, et en fonction de la vitesse, a partir de la relation d=v*t, en deduire le temps necessaire pour parcourir la hauteur totale.

unTiers = 2 #(d/v)/3 ## d/v representant donc le temps de la montee jusqu'en haut.
pwm3.start(100)
GPIO.setup(Moteur3A,GPIO.OUT)
GPIO.setup(Moteur3B,GPIO.OUT)
GPIO.setup(Moteur3E,GPIO.OUT)
GPIO.output(Moteur3A,GPIO.HIGH)
GPIO.output(Moteur3B,GPIO.LOW)
GPIO.output(Moteur3E,GPIO.HIGH) ##On fait monter le scanner
time.sleep(unTiers) 			##On fait monter le scanner d'un tiers de la hauteur maximale
pwm3.stop()  ##On arrete le moteur, le temps de faire un tour de plateau
print "Un tiers. En attente de l'interrupteur"
pwm2.start(100)
while (GPIO.input(Inter1)==False):
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(Moteur2A,GPIO.OUT)
	GPIO.setup(Moteur2B,GPIO.OUT)
	GPIO.setup(Moteur2E,GPIO.OUT)
	GPIO.output(Moteur2A,GPIO.HIGH)
	GPIO.output(Moteur2B,GPIO.LOW)
	GPIO.output(Moteur2E,GPIO.HIGH)
    
pwm2.stop()#Le tour de plateau a ete effectue, arret du moteur
print "2e tour de plateau effectue, montee aux deux tiers"
pwm3.start(100)
#On remonte d'un tiers
GPIO.output(Moteur3A,GPIO.HIGH)
GPIO.output(Moteur3B,GPIO.LOW)
GPIO.output(Moteur3E,GPIO.HIGH) ##On fait monter le scanner
time.sleep(unTiers) 			##On fait monter le scanner d'un tiers de la hauteur maximale
pwm3.stop()  ##On arrete le moteur, le temps de faire un tour de plateau
#Arrivee aux deux tiers
print "Arrivee aux deux tiers, tour de plateau, en attente de l'interrupteur"
pwm2.start(100)
#Tour de plateau
while (GPIO.input(Inter1)==False):
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(Moteur2A,GPIO.OUT)
	GPIO.setup(Moteur2B,GPIO.OUT)
	GPIO.setup(Moteur2E,GPIO.OUT)
	GPIO.output(Moteur2A,GPIO.HIGH)
	GPIO.output(Moteur2B,GPIO.LOW)
	GPIO.output(Moteur2E,GPIO.HIGH)
    
pwm2.stop() #Le tour de plateau a ete effectue, arret du moteur
print "3e tour de plateau effectue, montee a la hauteur max"
pwm3.start(100)
#Montee du scanner jusqu'a la hauteur max
GPIO.output(Moteur3A,GPIO.HIGH)
GPIO.output(Moteur3B,GPIO.LOW)
GPIO.output(Moteur3E,GPIO.HIGH) ##On fait monter le scanner
time.sleep(unTiers) 			##On fait monter le scanner d'un tiers de la hauteur maximale
pwm3.stop()  ##On arrete le moteur, le temps de faire un tour de plateau
#Arrivee hauteur maxi
print "arrivee hauteur max, tour de plateau. En attente de l'interrupteur."
#Dernier tour de plateau
pwm2.start(100)
while (GPIO.input(Inter1)==False):
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(Moteur2A,GPIO.OUT)
	GPIO.setup(Moteur2B,GPIO.OUT)
	GPIO.setup(Moteur2E,GPIO.OUT)
	GPIO.output(Moteur2A,GPIO.HIGH)
	GPIO.output(Moteur2B,GPIO.LOW)
	GPIO.output(Moteur2E,GPIO.HIGH)
    
#Le tour de plateau a ete effectue, arret du moteur
print "Le dernier tour a ete effectue."
pwm2.stop() ##Plus besoin du plateau, arret de la pwm

print "le scanner va donc retourner a la position initiale"
#On redescend le scanner a sa position initiale
print"En attente de l'interrupteur2"
while (GPIO.input(Inter2)==False):
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(Moteur3A,GPIO.OUT)
	GPIO.setup(Moteur3B,GPIO.OUT)
	GPIO.setup(Moteur3E,GPIO.OUT)
	GPIO.output(Moteur3A,GPIO.LOW)		##On le fait  tourner dans le
	GPIO.output(Moteur3B,GPIO.HIGH)		##sens inverse pour redescendre
	GPIO.output(Moteur3E,GPIO.HIGH)
    
pwm3.stop() 					##Arrete du moteur et de la pwm

print "Fin du scan"
print "######################################################"
GPIO.cleanup()