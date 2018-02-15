## MBE - Notatki do zadań ##

**Lab 2C**

Flaga:  `1m_all_ab0ut_d4t_b33f`

----

**Lab 7A**

Flaga:  `1m_all_ab0ut_d4t_b33f`

* Binarka statycznie skompilowana z ASLR, Partial RELRO, kanarkiem i NX
* Wiadomości przechowuje struktura zdefiniowana poniżej (kierunek ułożenia w heapie jest odwrotny do tego co na stosie):
```
struct msg {
    void (* print_msg)(struct msg *);
    unsigned int xor_pad[MAX_BLOCKS];
    unsigned int message[MAX_BLOCKS];
    unsigned int msg_len;
};
```
* Użytkownik podaje wiadomość oraz *jej rozmiar* - pod spodem następuje xorowanie z jakimiś wartościami, które są dla nas bez znaczenia
* Błąd pozwalający na nadpisanie zmiennej `msg_len` występuje w snippecie poniżej (problemem jest wykorzystanie int i dzielenie z "ucięciem" ułamka - dzięki temu możemy zapisać o `BLOCK_SIZE - 1` bajtów poza buforem):
```
/* make sure the message length is no bigger than the xor pad */
    if((new_msg->msg_len / BLOCK_SIZE) > MAX_BLOCKS)
        new_msg->msg_len = BLOCK_SIZE * MAX_BLOCKS;

    /* read in the message to encrypt with the xor pad */
    printf("-Enter data to encrypt: ");
    read(0, &new_msg->message, new_msg->msg_len);
```
----
