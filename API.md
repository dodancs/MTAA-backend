# ČiliCat API

## Endpointy

- [Autentifikácia](#route-auth)
  - [Prihlásenie](#route-auth-login)
  - [Odhlásenie](#route-auth-logout)
  - [Registrácia](#route-auth-register)
  - [Aktivácia účtu](#route-auth-activate)
  - [Obnovenie relácie](#route-auth-refresh)
  - [Zobrazenie všetkých používateľov](#route-auth-getUsers)
  - [Zobrazenie informácií o špecifickom používateľovi](#route-auth-getUser)
  - [Úprava používateľa](#route-auth-updateUser)
  - [Zmazanie používateľa](#route-auth-deleteUser)
- [Správa mačiek](#route-cats)
  - [Zorbazenie mačiek](#route-cats-get)
  - [Pridanie mačky](#route-cats-add)
  - [Úprava mačky](#route-cats-update)
  - [Zmazanie mačky](#route-cats-delete)
  - [Adoptácia mačky](#route-cats-adopt)
  - [Pridanie do obľúbených](#route-cats-like)
  - [Odobratie z obľúbených](#route-cats-unlike)
- [Správa obrázkov](#route-pictures)
  - [Zobrazenie obrázku](#route-pictures-get)
  - [Pridanie obrázku](#route-pictures-add)
  - [Zmazanie obrázku](#route-pictures-delete)
- [Správa komentárov](#route-comments)
  - [Zobrazenie komentárov pre mačku](#route-comments-get)
  - [Pridanie komentára](#route-comments-add)
  - [Zmazanie komentára](#route-comments-delete)
- [Správa potrieb útulku](#route-shelterneeds)
  - [Zobrazit všetky potreby](#route-shelterneeds-get)
  - [Pridať potrebu](#route-shelterneeds-add)
  - [Zobraziť / skryť potrebu](#route-shelterneeds-toggle)
  - [Zmazať potrebu](#route-shelterneeds-delete)
- [Peňažné príspevky](#route-donations)
  - [Zaznamenanie príspevku](#route-donations-add)
- [Nastavenia systému](#route-settings)
  - [Zobrazenie farieb](#route-settings-colours-get)
  - [Pridanie farby](#route-settings-colours-add)
  - [Odstránenie farby](#route-settings-colours-delete)
  - [Zobrazenie plemien](#route-settings-breeds-get)
  - [Pridanie plemena](#route-settings-breeds-add)
  - [Odstránenie plemena](#route-settings-breeds-delete)
  - [Zobrazenie zdravotných stavov](#route-settings-healthstatus-get)
  - [Pridanie zdravotného stavu](#route-settings-healthstatus-add)
  - [Odstránenie zdravotného stavu](#route-settings-healthstatus-delete) 

### <a name="route-auth"></a>Autentifikácia
- [Prihlásenie](#route-auth-login)
- [Odhlásenie](#route-auth-logout)
- [Registrácia](#route-auth-register)
- [Aktivácia účtu](#route-auth-activate)
- [Obnovenie relácie](#route-auth-refresh)
- [Zobrazenie všetkých používateľov](#route-auth-getUsers)
- [Zobrazenie informácií o špecifickom používateľovi](#route-auth-getUser)
- [Úprava používateľa](#route-auth-updateUser)
- [Zmazanie používateľa](#route-auth-deleteUser)

#### <a name="route-auth-login"></a>/auth/login : POST
- popis: Autentifikovanie používateľa pomocou prihlasovacích údajov
- požiadavka:
  - telo požiadavky:
    ```json
    {
      "email": "janko@mrkvicka.sk", 
      "password": "hesielko"
    }
    ```

- odpoveď:
  - HTTP kód: 200
  - telo odpovede:
    ```json
    {
      "token": "JWT_ACCESSTOKEN", 
      "token_type": "bearer", 
      "expires": 3600,
      "uuid": "uuidstring"
    }
    ```
  
- odpoveď:
  - HTTP kód: 400
  - telo odpovede: 
    ```json
    {
      "error": "Zlé prihlasovacie údaje..."
    }
    ```
  
-----------

#### <a name="route-auth-logout"></a>/auth/logout : GET
- popis: Odhlásenie používateľa
- požiadavka:
  - HTTP hlavičky: 
    - `Authentication: "bearer JWT_ACCESSTOKEN"`


- odpoveď:
  - HTTP kód: 200

-----------

#### <a name="route-auth-register"></a>/auth/register : POST
- popis: Registrácia nového používateľa
- správanie: V prípade, že nie je špecifikovaný obrázok je používateľovi nastavený všeobecný predvolený obrázok.
- požiadavka:
  - telo požiadavky:
    ```json
    {
      "email": "janko@mrkvicka.sk", 
      "password": "hesielko",
      "firstname": "Jano",
      "lastname": "Mrkvička",
      "picture": "pictureuuidstring"
    }
    ```

- odpoveď:
  - HTTP kód: 200
  
- odpoveď:
  - HTTP kód: 400
  - telo odpovede: 
    ```json
    {
      "error": "E-mailová adresa už bola použitá..."
    }
    ```

-----------

#### <a name="route-auth-activate"></a>/auth/activate/{seed} : GET
- popis: Aktivácia používateľského účtu
- odpoveď:
  - HTTP kód: 200

-----------

#### <a name="route-auth-refresh"></a>/auth/refresh_token : GET
- popis: Obnovenie používateľskej relácie
- požiadavka:
  - HTTP hlavičky: 
    - `Authentication: "bearer JWT_ACCESSTOKEN"`

- odpoveď:
  - HTTP kód: 200
  - telo odpovede:
    ```json
    {
      "token": "JWT_ACCESSTOKEN", 
      "token_type": "bearer", 
      "expires": 3600,
      "uuid": "uuidstring"
    }
    ```

- odpoveď:
  - HTTP kód: 401
  - telo odpovede: 
    ```json
    {
      "error": "Prístup zamietnutý..."
    }
    ```
  
-----------

#### <a name="route-auth-getUsers"></a>/auth/users : GET
- popis: Zobrazenie všetkých používateľov
- požiadavka:
  - HTTP hlavičky: 
    - `Authentication: "bearer JWT_ACCESSTOKEN"`

- odpoveď:
  - HTTP kód: 200
  - telo odpovede:
    ```json
    {
      "count": 231,
      "users": [
        {
          "uuid": "uuidstring",
          "email": "janko@mrkvicka.sk",
          "firstname": "Jano",
          "lastname": "Mrkvička",
          "activated": true,
          "admin": false,
          "created_at": "2020-02-19 08:46:28",
          "updated_at": "2020-02-19 08:46:28"
        }
      ]
    }
    ```
  
- odpoveď:
  - HTTP kód: 401
  - telo odpovede: 
    ```json
    {
      "error": "Prístup zamietnutý..."
    }
    ```

-----------

#### <a name="route-auth-getUser"></a>/auth/users/{uuid} : GET
- popis: Zobrazenie detailu používateľa
- požiadavka:
  - HTTP hlavičky: 
    - `Authentication: "bearer JWT_ACCESSTOKEN"`
  - parametre:
    - __{uuid}__: Unikátny identifikačný reťazec používateľa

- odpoveď:
  - HTTP kód: 200
  - telo odpovede:
    ```json
    {
      "uuid": "uuidstring",
      "email": "janko@mrkvicka.sk",
      "firstname": "Jano",
      "lastname": "Mrkvička",
      "activated": true,
      "admin": false,
      "donations": 0,
      "picture": "uuidstring",
      "favourites": ["cat1uuid", "cat2uuid"],
      "created_at": "2020-02-19 08:46:28",
      "updated_at": "2020-02-19 08:46:28"
    }
    ```
  
- odpoveď:
  - HTTP kód: 401
  - telo odpovede: 
    ```json
    {
      "error": "Prístup zamietnutý..."
    }
    ```
  
- odpoveď:
  - HTTP kód: 400
  - telo odpovede: 
    ```json
    {
      "error": "Neplatný identifikátor..."
    }
    ```

-----------

#### <a name="route-auth-updateUser"></a>/auth/users/{uuid} : PUT
- popis: Úprava používateľa
- požiadavka:
  - HTTP hlavičky: 
    - `Authentication: "bearer JWT_ACCESSTOKEN"`
  - parametre:
    - __{uuid}__: Unikátny identifikačný reťazec používateľa
  - telo požiadavky:
    ```json
    {
      "password": "novehesielko"
    }
    ```
  
- odpoveď:
  - HTTP kód: 200
  
- odpoveď:
  - HTTP kód: 401
  - telo odpovede: 
    ```json
    {
      "error": "Prístup zamietnutý..."
    }
    ```
  
- odpoveď:
  - HTTP kód: 400
  - telo odpovede: 
    ```json
    {
      "error": "Neplatný identifikátor..."
    }
    ```

-----------

#### <a name="route-auth-updateUser"></a>/auth/users/{uuid} : DELETE
- popis: Odstránenie používateľa
- požiadavka:
  - HTTP hlavičky: 
    - `Authentication: "bearer JWT_ACCESSTOKEN"`
  - parametre:
    - __{uuid}__: Unikátny identifikačný reťazec používateľa

- odpoveď:
  - HTTP kód: 200
  
- odpoveď:
  - HTTP kód: 401
  - telo odpovede: 
    ```json
    {
      "error": "Prístup zamietnutý..."
    }
    ```
  
- odpoveď:
  - HTTP kód: 400
  - telo odpovede: 
    ```json
    {
      "error": "Neplatný identifikátor..."
    }
    ```

-----------
-----------

### <a name="route-cats"></a>Správa mačiek
- [Zorbazenie mačiek](#route-cats-get)
- [Pridanie mačky](#route-cats-add)
- [Úprava mačky](#route-cats-update)
- [Zmazanie mačky](#route-cats-delete)
- [Adoptácia mačky](#route-cats-adopt)
- [Pridanie do obľúbených](#route-cats-like)
- [Odobratie z obľúbených](#route-cats-unlike)

#### <a name="route-cats-get"></a>/cats : GET
- popis: Zobrazenie všetkých mačiek
- požiadavka:
  - HTTP hlavičky: 
    - `Authentication: "bearer JWT_ACCESSTOKEN"`
  - GET parametre (voliteľné):
    - Limitácia počtu výsledkov: `limit=10`
    - Aktuálna stránka: `page=3`
    - Filter: adoptovateľná: `adoptive=true`
    - Filter: pohlavie: `sex=true`
    - Filter: plemeno: `breed=1`
    - Filter: zdravotný stav: `health_statu=1`
    - Filter: maximálny vek: `age_up=30`
    - Filter: minimálny vek: `age_down=10`
    - Filter: farba srsti: `colour=7`
    - Filter: kastrovaná: `castrated=false`
    - Filter: očkovaná: `vaccinated=true`
    - Filter: odčervená: `dewormed=true`

- odpoveď:
  - HTTP kód: 200
  - telo odpovede:
    ```json
    {
      "total": 3421,
      "page": 3,
      "count": 10,
      "cats": [
        {
          "uuid": "uuidstring",
          "name": "Micka", 
          "age": 3,
          "sex": true,
          "breed": 1,
          "health_status": 3,
          "castrated": false,
          "vaccinated": true,
          "dewormed": true,
          "colour": 7,
          "desctiption": "Toto je moje zlaticko..",
          "health_log": "Problemy u veterinara nikdy neboli...",
          "adoptive": true,
          "pictures": [
            "uuidstring1",
            "uuidstring2"
          ]
        }
      ]
    }
    ```

- odpoveď:
  - HTTP kód: 401
  - telo odpovede: 
    ```json
    {
      "error": "Prístup zamietnutý..."
    }
    ```

-----------

#### <a name="route-cats-add"></a>/cats : POST
- popis: Pridanie novej mačky
- požiadavka:
  - HTTP hlavičky: 
    - `Authentication: "bearer JWT_ACCESSTOKEN"`
  - telo požiadavky:
    ```json
    {
      "name": "Micka", 
      "age": 3,
      "sex": true,
      "breed": 1,
      "health_status": 3,
      "castrated": false,
      "vaccinated": true,
      "dewormed": true,
      "colour": 7,
      "desctiption": "Toto je moje zlaticko..",
      "health_log": "Problemy u veterinara nikdy neboli...",
      "adoptive": true,
      "pictures": [
        "uuidstring1",
        "uuidstring2"
      ]
    }
    ```
  
- odpoveď:
  - HTTP kód: 200
  - telo odpovede:
    ```json
    {
      "uuid": "uuidnovejmacky"
    }
    ```
  
- odpoveď:
  - HTTP kód: 400
  - telo odpovede: 
    ```json
    {
      "error": "Nesprávne zadané údaje..."
    }
    ```

-----------

#### <a name="route-cats-update"></a>/cats/{uuid} : PUT
- popis: Úprava existujúcej mačky
- požiadavka:
  - HTTP hlavičky: 
    - `Authentication: "bearer JWT_ACCESSTOKEN"`
  - parametre:
    - __{uuid}__: Unikátny identifikačný reťazec používateľa
  - telo požiadavky:
    ```json
    {
      "age": 4,
      "health_status": 1,
      "castrated": true,
      "pictures": [
        "uuidstring1",
        "uuidstring2"
      ]
    }
    ```
  
- odpoveď:
  - HTTP kód: 200
  
- odpoveď:
  - HTTP kód: 401
  - telo odpovede: 
    ```json
    {
      "error": "Prístup zamietnutý..."
    }
    ```

- odpoveď:
  - HTTP kód: 400
  - telo odpovede: 
    ```json
    {
      "error": "Nesprávne zadané údaje..."
    }
    ```

-----------

#### <a name="route-cats-update"></a>/cats/{uuid} : DELETE
- popis: Odstránenie mačky
- požiadavka:
  - HTTP hlavičky: 
    - `Authentication: "bearer JWT_ACCESSTOKEN"`
  - parametre:
    - __{uuid}__: Unikátny identifikačný reťazec mačky

- odpoveď:
  - HTTP kód: 200
  
- odpoveď:
  - HTTP kód: 401
  - telo odpovede: 
    ```json
    {
      "error": "Prístup zamietnutý..."
    }
    ```
  
- odpoveď:
  - HTTP kód: 400
  - telo odpovede: 
    ```json
    {
      "error": "Neplatný identifikátor..."
    }
    ```

-----------

#### <a name="route-cats-adopt"></a>/cats/{uuid}/adopt : POST
- popis: Adoptovanie mačky
- požiadavka:
  - HTTP hlavičky: 
    - `Authentication: "bearer JWT_ACCESSTOKEN"`
  - parametre:
    - __{uuid}__: Unikátny identifikačný reťazec mačky

- odpoveď:
  - HTTP kód: 200
  
- odpoveď:
  - HTTP kód: 400
  - telo odpovede: 
    ```json
    {
      "error": "Neplatný identifikátor..."
    }
    ```

- odpoveď:
  - HTTP kód: 400
  - telo odpovede: 
    ```json
    {
      "error": "Mačku nie je možné adoptovať..."
    }
    ```

-----------

#### <a name="route-cats-like"></a>/cats/{uuid}/like : POST
- popis: Uloženie mačky do obľúbených
- požiadavka:
  - HTTP hlavičky: 
    - `Authentication: "bearer JWT_ACCESSTOKEN"`
  - parametre:
    - __{uuid}__: Unikátny identifikačný reťazec mačky

- odpoveď:
  - HTTP kód: 200
  
- odpoveď:
  - HTTP kód: 400
  - telo odpovede: 
    ```json
    {
      "error": "Neplatný identifikátor..."
    }
    ```

-----------

#### <a name="route-cats-unlike"></a>/cats/{uuid}/unlike : POST
- popis: Odobratie mačky z obľúbených
- požiadavka:
  - HTTP hlavičky: 
    - `Authentication: "bearer JWT_ACCESSTOKEN"`
  - parametre:
    - __{uuid}__: Unikátny identifikačný reťazec mačky

- odpoveď:
  - HTTP kód: 200
  
- odpoveď:
  - HTTP kód: 400
  - telo odpovede: 
    ```json
    {
      "error": "Neplatný identifikátor..."
    }
    ```

-----------
-----------

### <a name="route-pictures"></a>Správa obrázkov
- [Zobrazenie obrázku](#route-pictures-get)
- [Pridanie obrázku](#route-pictures-add)
- [Zmazanie obrázku](#route-pictures-delete)

#### <a name="route-pictures-get"></a>/pictures/{uuid} : GET
- popis: Zobrazenie obrázku
- požiadavka:
  - HTTP hlavičky: 
    - `Authentication: "bearer JWT_ACCESSTOKEN"`
  - parametre:
    - __{uuid}__: Unikátny identifikačný reťazec obrázku

- odpoveď:
  - HTTP kód: 200
  - HTTP hlavičky: 
    - `Content-type: image/png`
  - telo odpovede: `binarne data`

- odpoveď:
  - HTTP kód: 401
  - telo odpovede: 
    ```json
    {
      "error": "Prístup zamietnutý..."
    }
    ```

- odpoveď:
  - HTTP kód: 400
  - telo odpovede: 
    ```json
    {
      "error": "Neplatný identifikátor..."
    }
    ```

-----------

#### <a name="route-pictures-add"></a>/pictures : POST
- popis: Pridanie nového obrázku
- požiadavka:
  - HTTP hlavičky: 
    - `Authentication: "bearer JWT_ACCESSTOKEN"`
    - `Content-type: image/jpg`
    - `Content-length: 45677834`
  - telo požiadavky: `binarne data`

- odpoveď:
  - HTTP kód: 200
  - telo odpovede:
    ```json
    {
      "uuid": "uuidstring"
    }
    ```

- odpoveď:
  - HTTP kód: 401
  - telo odpovede: 
    ```json
    {
      "error": "Prístup zamietnutý..."
    }
    ```

-----------

#### <a name="route-pictures-delete"></a>/pictures/{uuid} : DELETE
- popis: Zobrazenie obrázku
- požiadavka:
  - HTTP hlavičky: 
    - `Authentication: "bearer JWT_ACCESSTOKEN"`
  - parametre:
    - __{uuid}__: Unikátny identifikačný reťazec obrázku

- odpoveď:
  - HTTP kód: 200
  
- odpoveď:
  - HTTP kód: 401
  - telo odpovede: 
    ```json
    {
      "error": "Prístup zamietnutý..."
    }
    ```

- odpoveď:
  - HTTP kód: 400
  - telo odpovede: 
    ```json
    {
      "error": "Neplatný identifikátor..."
    }
    ```

-----------
-----------

### <a name="route-comments"></a>Správa komentárov
- [Zobrazenie komentárov pre mačku](#route-comments-get)
- [Pridanie komentára](#route-comments-add)
- [Zmazanie komentára](#route-comments-delete)

#### <a name="route-comments-get"></a>/comments/{uuid} : GET
- popis: Zobrazenie komentárov pre danú mačku
- požiadavka:
  - HTTP hlavičky: 
    - `Authentication: "bearer JWT_ACCESSTOKEN"`
  - parametre:
    - __{uuid}__: Unikátny identifikačný reťazec mačky

- odpoveď:
  - HTTP kód: 200
  - telo odpovede:
    ```json
    {
      "count": 3,
      "comments": [
        {
          "uuid": "uuidstring",
          "author": "uuidstring", 
          "cat": "uuidstring", 
          "text": "Tá je úplne krásna! 😍",
          "created_at": "2020-02-19 08:46:28"
        }
      ]
    }
    ```

- odpoveď:
  - HTTP kód: 401
  - telo odpovede: 
    ```json
    {
      "error": "Prístup zamietnutý..."
    }
    ```

- odpoveď:
  - HTTP kód: 400
  - telo odpovede: 
    ```json
    {
      "error": "Neplatný identifikátor..."
    }
    ```

-----------

#### <a name="route-comments-add"></a>/comments/{uuid} : POST
- popis: Pridanie komentára k danej mačke
- požiadavka:
  - HTTP hlavičky: 
    - `Authentication: "bearer JWT_ACCESSTOKEN"`
  - parametre:
    - __{uuid}__: Unikátny identifikačný reťazec mačky
  - telo požiadavky:
    ```json
    {
      "text": "Tá je úplne krásna! 😍"
    }
    ```
  
- odpoveď:
  - HTTP kód: 200
  
- odpoveď:
  - HTTP kód: 401
  - telo odpovede: 
    ```json
    {
      "error": "Prístup zamietnutý..."
    }
    ```

- odpoveď:
  - HTTP kód: 400
  - telo odpovede: 
    ```json
    {
      "error": "Neplatný identifikátor..."
    }
    ```

-----------

#### <a name="route-comments-delete"></a>/comments/{uuid} : DELETE
- popis: Zmazanie komentára
- požiadavka:
  - HTTP hlavičky: 
    - `Authentication: "bearer JWT_ACCESSTOKEN"`
  - parametre:
    - __{uuid}__: Unikátny identifikačný reťazec komentára

- odpoveď:
  - HTTP kód: 200
  
- odpoveď:
  - HTTP kód: 401
  - telo odpovede: 
    ```json
    {
      "error": "Prístup zamietnutý..."
    }
    ```

- odpoveď:
  - HTTP kód: 400
  - telo odpovede: 
    ```json
    {
      "error": "Neplatný identifikátor..."
    }
    ```

-----------
-----------

### <a name="route-shelterneeds"></a>Správa potrieb útulku
- [Zobrazit všetky potreby](#route-shelterneeds-get)
- [Pridať potrebu](#route-shelterneeds-add)
- [Zobraziť / skryť potrebu](#route-shelterneeds-toggle)
- [Zmazať potrebu](#route-shelterneeds-delete)

#### <a name="route-shelterneeds-get"></a>/shelterneeds : GET
- popis: Zobrazenie potrieb útulku
- správanie: V prípade, že je používateľ prihlásený a má rolu administrátora, bude mu zobrazené aj pole "hide". V opačnom prípade budú zobrazené len potreby, ktoré majú tento parameter nastavený na hodnotu `false`.
- požiadavka:
  - HTTP hlavičky (nepovinné): 
    - `Authentication: "bearer JWT_ACCESSTOKEN"`

- odpoveď:
  - HTTP kód: 200
  - telo odpovede:
    ```json
    {
      "count": 7,
      "shelterneeds": [
        {
          "uuid": "uuidstring",
          "category": "Krmivo", 
          "name": "Suché granule", 
          "details": "Granule suchého typu, preferovane od značiek Whiskas.", 
          "hide": false
        }
      ]
    }
    ```

- odpoveď:
  - HTTP kód: 401
  - telo odpovede: 
    ```json
    {
      "error": "Prístup zamietnutý..."
    }
    ```

-----------

#### <a name="route-shelterneeds-add"></a>/shelterneeds : POST
- popis: Pridanie novej potreby útulku
- požiadavka:
  - HTTP hlavičky (nepovinné): 
    - `Authentication: "bearer JWT_ACCESSTOKEN"`
  - telo požiadavky:
    ```json
    {
      "category": "Krmivo",
      "name": "Suché granule",
      "details": "Granule suchého typu, preferovane od značiek Whiskas."
    }
    ```
  
- odpoveď:
  - HTTP kód: 200
  
- odpoveď:
  - HTTP kód: 401
  - telo odpovede: 
    ```json
    {
      "error": "Prístup zamietnutý..."
    }
    ```

- odpoveď:
  - HTTP kód: 400
  - telo odpovede: 
    ```json
    {
      "error": "Nesprávne zadané údaje..."
    }
    ```

-----------

#### <a name="route-shelterneeds-toggle"></a>/shelterneeds/{uuid} : POST
- popis: Zobrazenie / skrytie potreby útulku
- požiadavka:
  - HTTP hlavičky: 
    - `Authentication: "bearer JWT_ACCESSTOKEN"`
  - parametre:
    - __{uuid}__: Unikátny identifikačný reťazec potreby útulku

- odpoveď:
  - HTTP kód: 200
  
- odpoveď:
  - HTTP kód: 401
  - telo odpovede: 
    ```json
    {
      "error": "Prístup zamietnutý..."
    }
    ```

- odpoveď:
  - HTTP kód: 400
  - telo odpovede: 
    ```json
    {
      "error": "Neplatný identifikátor..."
    }
    ```

-----------

#### <a name="route-shelterneeds-delete"></a>/shelterneeds/{uuid} : DELETE
- popis: Zmazanie potreby útulku
- požiadavka:
  - HTTP hlavičky: 
    - `Authentication: "bearer JWT_ACCESSTOKEN"`
  - parametre:
    - __{uuid}__: Unikátny identifikačný reťazec potreby útulku

- odpoveď:
  - HTTP kód: 200
  
- odpoveď:
  - HTTP kód: 401
  - telo odpovede: 
    ```json
    {
      "error": "Prístup zamietnutý..."
    }
    ```

- odpoveď:
  - HTTP kód: 400
  - telo odpovede: 
    ```json
    {
      "error": "Neplatný identifikátor..."
    }
    ```

-----------
-----------

### <a name="route-donations"></a>Peňažné príspevky
- [Zaznamenanie príspevku](#route-donations-add)

#### <a name="route-donations-add"></a>/donation : POST
- popis: Zaznamenanie peňažného príspevku
- správanie: Položka "donator" nie je potrebná - určuje identifikátor prispievateľa, ak nechce byť anonymný.
- požiadavka:
  - HTTP hlavičky: 
    - `Authentication: "bearer JWT_ACCESSTOKEN"`
  - telo požiadavky:
    ```json
    {
      "donator": "uuidstring",
      "amount": 15.25
    }
    ```
  
- odpoveď:
  - HTTP kód: 200
  
- odpoveď:
  - HTTP kód: 400
  - telo odpovede: 
    ```json
    {
      "error": "Nesprávne zadané údaje..."
    }
    ```

-----------
-----------

### <a name="route-settings"></a>Nastavenia systému
- [Zobrazenie farieb](#route-settings-colours-get)
- [Pridanie farby](#route-settings-colours-add)
- [Odstránenie farby](#route-settings-colours-delete)
- [Zobrazenie plemien](#route-settings-breeds-get)
- [Pridanie plemena](#route-settings-breeds-add)
- [Odstránenie plemena](#route-settings-breeds-delete)
- [Zobrazenie zdravotných stavov](#route-settings-healthstatus-get)
- [Pridanie zdravotného stavu](#route-settings-healthstatus-add)
- [Odstránenie zdravotného stavu](#route-settings-healthstatus-delete) 

#### <a name="route-settings-colours-get"></a>/settings/colours : GET
- popis: Zobrazenie dostupných hodnôt pre farbu srsti mačky
- požiadavka:
  - HTTP hlavičky: 
    - `Authentication: "bearer JWT_ACCESSTOKEN"`

- odpoveď:
  - HTTP kód: 200
  - telo odpovede:
    ```json
    {
      "count": 3,
      "colours": [
        {
          "id": 0,
          "name": "čierna"
        },
        {
          "id": 1,
          "name": "šedá"
        },
        {
          "id": 2,
          "name": "hnedá"
        }
      ]
    }
    ```

-----------

#### <a name="route-settings-colours-add"></a>/settings/colours : POST
- popis: Pridanie hodnoty pre farbu srsti

- požiadavka:
  - HTTP hlavičky: 
    - `Authentication: "bearer JWT_ACCESSTOKEN"`
  - telo požiadavky:
    ```json
    {
      "name": "biela"
    }
    ```
  
- odpoveď:
  - HTTP kód: 200
  - telo odpovede:
    ```json
    {
      "id": 3
    }
    ```

- odpoveď:
  - HTTP kód: 401
  - telo odpovede: 
    ```json
    {
      "error": "Prístup zamietnutý..."
    }
    ```

- odpoveď:
  - HTTP kód: 400
  - telo odpovede: 
    ```json
    {
      "error": "Nesprávne zadané údaje..."
    }
    ```

-----------

#### <a name="route-settings-colours-delete"></a>/settings/colours/{id} : DELETE
- popis: Odstránenie hodnoty pre farbu srsti

- požiadavka:
  - HTTP hlavičky: 
    - `Authentication: "bearer JWT_ACCESSTOKEN"`
  - parametre:
    - __{id}__: Unikátny identifikátor farby

- odpoveď:
  - HTTP kód: 200
  
- odpoveď:
  - HTTP kód: 401
  - telo odpovede: 
    ```json
    {
      "error": "Prístup zamietnutý..."
    }
    ```

-----------

#### <a name="route-settings-breeds-get"></a>/settings/breeds : GET
- popis: Zobrazenie dostupných hodnôt pre plemeno mačky
- požiadavka:
  - HTTP hlavičky: 
    - `Authentication: "bearer JWT_ACCESSTOKEN"`

- odpoveď:
  - HTTP kód: 200
  - telo odpovede:
    ```json
    {
      "count": 3,
      "colours": [
        {
          "id": 0,
          "name": "perzská"
        },
        {
          "id": 1,
          "name": "britská modrá"
        },
        {
          "id": 2,
          "name": "egyptská"
        }
      ]
    }
    ```

-----------

#### <a name="route-settings-breeds-add"></a>/settings/breeds : POST
- popis: Pridanie hodnoty pre plemeno

- požiadavka:
  - HTTP hlavičky: 
    - `Authentication: "bearer JWT_ACCESSTOKEN"`
  - telo požiadavky:
    ```json
    {
      "name": "maincoon"
    }
    ```
  
- odpoveď:
  - HTTP kód: 200
  - telo odpovede:
    ```json
    {
      "id": 3
    }
    ```

- odpoveď:
  - HTTP kód: 401
  - telo odpovede: 
    ```json
    {
      "error": "Prístup zamietnutý..."
    }
    ```

- odpoveď:
  - HTTP kód: 400
  - telo odpovede: 
    ```json
    {
      "error": "Nesprávne zadané údaje..."
    }
    ```

-----------

#### <a name="route-settings-breeds-delete"></a>/settings/breeds/{id} : DELETE
- popis: Odstránenie hodnoty pre plemeno

- požiadavka:
  - HTTP hlavičky: 
    - `Authentication: "bearer JWT_ACCESSTOKEN"`
  - parametre:
    - __{id}__: Unikátny identifikátor plemena

- odpoveď:
  - HTTP kód: 200
  
- odpoveď:
  - HTTP kód: 401
  - telo odpovede: 
    ```json
    {
      "error": "Prístup zamietnutý..."
    }
    ```

-----------

#### <a name="route-settings-healthstatus-get"></a>/settings/healthstatus : GET
- popis: Zobrazenie dostupných hodnôt pre zdravotný stav mačky
- požiadavka:
  - HTTP hlavičky: 
    - `Authentication: "bearer JWT_ACCESSTOKEN"`

- odpoveď:
  - HTTP kód: 200
  - telo odpovede:
    ```json
    {
      "count": 3,
      "health_statuses": [
        {
          "id": 0,
          "name": "zdravá"
        },
        {
          "id": 1,
          "name": "začervená"
        },
        {
          "id": 2,
          "name": "chorá"
        }
      ]
    }
    ```

-----------

#### <a name="route-settings-healthstatus-add"></a>/settings/healthstatus : POST
- popis: Pridanie hodnoty pre zdravotný stav

- požiadavka:
  - HTTP hlavičky: 
    - `Authentication: "bearer JWT_ACCESSTOKEN"`
  - telo požiadavky:
    ```json
    {
      "name": "ochrnutá"
    }
    ```
  
- odpoveď:
  - HTTP kód: 200
  - telo odpovede:
    ```json
    {
      "id": 3
    }
    ```

- odpoveď:
  - HTTP kód: 401
  - telo odpovede: 
    ```json
    {
      "error": "Prístup zamietnutý..."
    }
    ```

- odpoveď:
  - HTTP kód: 400
  - telo odpovede: 
    ```json
    {
      "error": "Nesprávne zadané údaje..."
    }
    ```

-----------

#### <a name="route-settings-healthstatus-delete"></a>/settings/healthstatus/{id} : DELETE
- popis: Odstránenie hodnoty pre zdravotný stav

- požiadavka:
  - HTTP hlavičky: 
    - `Authentication: "bearer JWT_ACCESSTOKEN"`
  - parametre:
    - __{id}__: Unikátny identifikátor zdravotného stavu

- odpoveď:
  - HTTP kód: 200
  
- odpoveď:
  - HTTP kód: 401
  - telo odpovede: 
    ```json
    {
      "error": "Prístup zamietnutý..."
    }
    ```
