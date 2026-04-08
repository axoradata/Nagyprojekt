A pythonProject a Raspberry szerver oldali kommunikációjára szolgáló porjekt. Mivel a Raspberry egy single board modell, emiatt nem képes önállóan adatbázis-kapcsolat kapcsolat kialakítására.
A projekt kapcsolatot teremt az adatbázis és az eszköz között, lehetővé teszi, hogy az eszközzel beolvasott adatok megjelenjelenek az adatbázisban. E mellett a program készít a bejelentkezésekről '-txt' fájlokba úgynvezetett belépésilogokat.
A program minden egyes nap egy újabb fájlt készít, amelyben feltünteti a belépési kísérleteket - fontos, hogy a sikeresek mellett a sikertelenek is megjelennek - jegyzi, hogy ki melyik felhasználó mikor kísérelte meg a bejelentkezést, valamint azt hogy ez a próbálkozás sikeres vagy sikertelen volt-e. 

  A projekt struktórája a következőképpen épül fel: 
  .
├── pythonProject/  
│   └── .venv   
├── 2025-11-15.txt   
├── 2025-11-16.txt  
├── 2025-11-17.txt   
├── 2025-11-18.txt   
├── 2025-11-19.txt   
├── 2026-02-06.txt   
├── data.db   
├── log.py  
├── main.py  
├── server.py   
└── External Libraries /  
    └── Scratches and Console  s 
