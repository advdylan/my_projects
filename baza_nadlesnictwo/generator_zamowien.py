import random
def generator(n):

    miasta = ["Warszawa", "Lesko", "Mikolow", "Tychy", "Brzesko"]
    lokalizacja = ["Las_Krymski", "Las_Poniatowski", "Las_Kosobudy"]
    drewno = ["sosna", "buk", "modrzew", "grab", "jesion"]

    zamowienia = []
    for i in range(n):
        metry = random.randint(1,50)
        rand_miasto = random.choice(miasta)
        rand_lokalizacja = random.choice(lokalizacja)
        rand_drewno = random.choice(drewno)
        zamowienia.append((i, rand_drewno, metry, rand_miasto, rand_lokalizacja))
    return zamowienia






