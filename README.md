# e-Teretana


E-teretana je web servis razvijen za upravljanje i pregledavanje termina u teretani. Aplikacija pruža korisniku mogućnost da dodaje, uređuje, briše termine te prati njihovu popunjenost, čime se olakšava organizacija treninga i povećava preglednost dostupnih termina. Glavna svrha aplikacije je omogućiti pregled termina treninga i osnovne informacije poput vrste treninga, datuma, vremena održavanja, kapaciteta i trenutne popunjenosti. Dostupne su funkcionalnosti i uređivanja i brisanja podataka ili samih termina ukoliko je potrebno ili kad su odrađeni. Vizualizacija prati broj termina po danu kroz stupičasti dijagram. 

Pokretanje lokalno
- bez Dockera
  - u terminalu prvo provjeriti verziju Pythona (python --version) jer verzija mora biti ista kao što je u okruženju, u ovom projektu je to 3.10
  - prijedlog je napraviti novi direktorij za projekt, kloniramo putanju iz Githuba s git clone https://github.com/korisnik/eteretana.git
  - ako se uspješno prenijelo, uđemo u direktorij gdje su skinuti svi potrebni dokumenti i preuzmemo potrebne verzije paketa s pip install -r reqs.txt
  - aplikaciju pokrenemo s python main.py i pritisnemo na vezu
- s Dockerom
  - isti koraci do preuzimanja requirementsa, nakon toga docker build --tag termin10:1.0 .  (proizvoljan naziv)
  - otvorimo Images u Dockeru i pokrenemo


Usecase dijagram:


![image](https://github.com/user-attachments/assets/df9b0ba3-7991-4c4c-90dd-3f403d276c90)

