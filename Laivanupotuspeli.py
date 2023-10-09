from random import randint 

class Pelilauta: 
    def __init__(self): 
        self.lauta = [[' '] * 8 for i in range(8)] 

    def tulosta(self): 
        print('   A B C D E F G H') 
        print(' ******************') 
        for i in range(len(self.lauta)): 
            if i == 9: 
                print(str(i+1) + '|' + '|'.join(self.lauta[i]) + '|') 
            else: 
                print(' ' + str(i+1) + '|' + '|'.join(self.lauta[i]) + '|') 

class Laiva: 
    def __init__(self, rivi, sarake): 
        self.rivi = rivi 
        self.sarake = sarake 

class LaivanupotusPeli: 

    def __init__(self): 
        self.piilotettu_lauta = Pelilauta() 
        self.pelaajan_lauta = Pelilauta() 
        self.laivat = [] 
 
    def lue_peliohjeet(self): 
        try: 
            with open("peliohjeet.txt") as tiedosto: 
                ohjeet = tiedosto.read() 
                print(ohjeet) 
        except FileNotFoundError: 
            print("Peliohjeita ei löydy.")

    def on_vierekkain(self, laiva1, laiva2): 
        return abs(laiva1.rivi - laiva2.rivi) <= 1 and abs(laiva1.sarake - laiva2.sarake) <= 1 

    def anna_sijainti(self): #tehty virheenkäsittely, että toimii myös tyhjällä syötteellä 
        while True: 
            try: 
                rivi = input("Anna rivinumero 1-8 ").upper() 
                if not rivi: # tarkistaa, onko syöte tyhjä 
                    raise ValueError("Et antanut mitään") 
                if rivi not in '1, 2, 3, 4, 5, 6, 7, 8': # tarkistaa onko syöte sopiva 
                    raise ValueError("Annoit väärän rivinumeron") 
                rivi = int(rivi) - 1  
                break 
            except ValueError as e:  
                print(e) 
                print('Anna rivinumero väliltä 1-8 ') 

        while True: 
            try: 
                sarake = input('Anna sarake A-H ').upper()  
                if not sarake: # tarkistaa, onko syöte tyhjä 
                    raise ValueError("Et antanut mitään") 
                if sarake not in ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'): # tarkistaa onko syöte sopiva 
                    raise ValueError("Annoit väärän sarakkeen")
                sarake = ord(sarake) - ord('A')  
                break  
            except ValueError as e: # käsittelee virheet 
                print(e) 
                print('Anna sarake väliltä A-H ') 
        return rivi, sarake 

    def luo_yksi_laiva(self): 
        rivi = randint(0, 7) 
        sarake = randint(0, 7) 
        return Laiva(rivi, sarake) 
 
    def luo_laivat(self, lauta): 
        for i in range(5): 
            uusi_laiva = self.luo_yksi_laiva() 
            while any(self.on_vierekkain(uusi_laiva, olemassaoleva) for olemassaoleva in self.laivat): 
                uusi_laiva = self.luo_yksi_laiva() 
            lauta.lauta[uusi_laiva.rivi][uusi_laiva.sarake] = 'X' 
            self.laivat.append(uusi_laiva) 
    
    def osuman_viereinen(self, lauta, rivi, sarake):
        if lauta.lauta[rivi][sarake] == 'X':
            for i in range(max(0, rivi - 1), min(rivi + 2, 8)):
                for j in range(max(0, sarake - 1), min(sarake + 2, 8)):
                    if lauta.lauta[i][j] == ' ':
                        lauta.lauta[i][j] = 'o'

    def pelaa(self):
        
        self.luo_laivat(self.piilotettu_lauta)
        
        yritykset = 10
        while yritykset > 0:
            self.pelaajan_lauta.tulosta()
            #voi testata kaikki osumat
            #self.piilotettu_lauta.tulosta()
            rivi, sarake = self.anna_sijainti()
            if self.pelaajan_lauta.lauta[rivi][sarake] == '-':
                print('Olet jo ampunut tähän ruutuun')
            elif self.pelaajan_lauta.lauta[rivi][sarake] == 'o':
                print('Tässä ruudussa ei voi olla laivaa.')
                print('Ammu uudestaan.')
            elif self.piilotettu_lauta.lauta[rivi][sarake] == 'X':
                print('Onnittelut! Osuit laivaan.')
                self.pelaajan_lauta.lauta[rivi][sarake] = 'X'
                self.osuman_viereinen(self.pelaajan_lauta, rivi, sarake)  # Merkitsee osuman ympärillä olevat koordinaatit
                yritykset -= 1
            else:
                print('Et osunut. Ammu uudestaan.')
                self.pelaajan_lauta.lauta[rivi][sarake] = '-'
                self.osuman_viereinen(self.pelaajan_lauta, rivi, sarake)
                yritykset -= 1
            if self.laske_osumat(self.pelaajan_lauta) == 5:
                print("Onnittelut! Sait upotettua kaikki laivat")
                break
            print('Sinulla on ' + str(yritykset) + ' yritystä jäljellä')
            if yritykset == 0:
                self.peliloppu()

    def laske_osumat(self, lauta):
        return sum(1 for rivi in lauta.lauta for sarake in rivi if sarake == 'X')

    def peliloppu(self):
        #tulostetaan laivojen sijainnit
        print('Peli päättyi - Yritykset loppuivat')
        print("Laivojen sijainnit olivat:")
        for laiva in self.laivat:
            self.pelaajan_lauta.lauta[laiva.rivi][laiva.sarake] = 'X'
        self.pelaajan_lauta.tulosta()

def tulosta_valikko():
    print("")
    print("Laivanupotuspeli")
    print("")
    print("1. Aloita peli")
    print("2. Peliohjeet")
    print("3. Lopeta")
    print("4. Koodarit")


if __name__ == "__main__":


    peli = LaivanupotusPeli()
    
    while True:
        tulosta_valikko()
        print("")
        valinta = input("Valitse toiminto: ")
        if valinta == '1':
            print("")
            peli = LaivanupotusPeli()
            peli.pelaa()
        elif valinta == '2':
            print("")
            peli.lue_peliohjeet()
        elif valinta == '3':
            print("")
            print("Peli päättyi. Tulethan pian uudestaan pelailemaan!")
            break
        elif valinta == '4':
            print("")
            print("Jarno Kiimala | Ilkka Lohilahti | Terttu Toivonen")
        else:
            print("Virheellinen valinta. Valitse uudelleen.")