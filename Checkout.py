import csv
import os.path
import sys


benutzerdb = "benutzer.csv"
produktdb = "produkte.csv"
gekauft = []


if os.path.exists(benutzerdb) == False:
    with open(benutzerdb, "wb") as f:
        writer = csv.writer(f)
        writer.writerow(["RFID", "Username", "Guthaben"])

if os.path.exists(produktdb) == False:
    with open(produktdb, "wb") as f:
        writer = csv.writer(f)
        writer.writerow(["Barcode", "Produktname", "Preis"])


def rfidcheck(rfid):
    userdata = 0
    with open(benutzerdb, "rb")as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == rfid:
                print("Hallo " + row[1] + ". Dein Kontostand: " + row[2] + " Euro")
                userdata = row

    if userdata == 0:
        print("Karte unbekannt. Neuer Account anlegen")
        newuser = raw_input("Dein Nickname: ")
        newline = [rfid, newuser, "0.00"]
        with open(benutzerdb, "a") as f:
            writer = csv.writer(f)
            writer.writerow(newline)
        sys.exit(0)

rfidcheck(raw_input("Eingabe RFID: "))


def barcodecheck(barcode):
    while weiterartikel == True:

        artikel = ""
        with open(produktdb, "rb") as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] == barcode:
                    print("+ 1x " + row[1] + " fuer " + row[2] + " Euro")
                    artikel = row[1]
                    gekauft.append(row)

        if artikel == "":
            produktname = raw_input("Produkt nicht gefunden. Produktname eingeben: ")
            preis = raw_input("Preis (Punkt benutzen) : ")
            produktdb_newline = [barcode, produktname, preis]
            with open(produktdb, "a") as f:
                writer = csv.writer(f)
                writer.writerow(produktdb_newline)
                gekauft.append(produktdb_newline)
                print("+ 1x " + produktdb_newline[1] + " fuer " + produktdb_newline[2] + " Euro")


barcodecheck(raw_input("Scann das Produkt ein: "))
weiterartikel = True
while weiterartikel:
    if raw_input("weitere Artikel? (ja/nein) ") == "ja":
        barcodecheck(raw_input("Scann das Produkt ein: "))
        weiterartikel = True
    else:
        weiterartikel = False

def abrechnung(gekauft):

    artieknamen = []
    artiekpreise = []

    for x in gekauft:
        artiekpreise.append(x[2])
        artieknamen.append(x[1])

    gesammt = 0
    for x in artiekpreise:
        gesammt = gesammt + float(x)

    print ("Deine Einkauft:")
    for x in gekauft:
        print(x[1] + ".........." + x[2] + " Euro")
    print("Gesammt......." + str(gesammt) + "0 Euro")

    if raw_input("Alles korrekt? (ja/nein) ") == "ja":
        benutzerdb_file = list(csv.reader(open(benutzerdb)))

        for x in benutzerdb_file:
            if x[1] == userdata[1]:                         # check Username
                x[2] = float(x[2]) - float(gesammt)
                print("Dein neuer Kontostand betraegt " + str(x[2]) + " Euro")

        writer = csv.writer(open(benutzerdb, "w"))
        writer.writerows(benutzerdb_file)
    else:
        print ("Abbruch")

abrechnung(gekauft)
