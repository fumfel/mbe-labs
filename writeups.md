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

* Binarka statycznie skompilowana z Partial RELRO, kanarkiem i NX - **brak ASLR!**
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
