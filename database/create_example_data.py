from requests import post

ADMIN_KEY = "bar"
API_URL = API_URL + ""

# Register users ######################################################################################
# Register Administrator
result = post(
    url=API_URL + "api/auth/register/",
    data={
        "username": "admin",
        "email": "admin@iis.czleteron.net",
        "first_name": "IIS",
        "last_name": "Admin",
        "city": "Brno",
        "street": "Bozetechova 1/2",
        "zip_code": "61200",
        "country": "Czechia",
        "password": "iis_admin"
    }
)
print(str(result.status_code) + " Register Administrator [" + result.text + "] ")
# Register Distributor
result = post(
    url=API_URL + "api/auth/register/",
    data={
        "username": "distributor",
        "email": "distributor@iis.czleteron.net",
        "first_name": "IIS",
        "last_name": "Distributor",
        "city": "Brno",
        "street": "Bozetechova 1/2",
        "zip_code": "61200",
        "country": "Czechia",
        "password": "iis_distributor"
    }
)
print(str(result.status_code) + " Register Distributor [" + result.text + "] ")
# Register Registered
result = post(
    url=API_URL + "api/auth/register/",
    data={
        "username": "registred",
        "email": "registred@iis.czleteron.net",
        "first_name": "IIS",
        "last_name": "Registred",
        "city": "Brno",
        "street": "Bozetechova 1/2",
        "zip_code": "61200",
        "country": "Czechia",
        "password": "iis_registred"
    }
)
print(str(result.status_code) + " Register Registered [" + result.text + "] ")
# Register Librarian 1
result = post(
    url=API_URL + "api/auth/register/",
    data={
        "username": "librarian",
        "email": "librarian@iis.czleteron.net",
        "first_name": "IIS",
        "last_name": "Librarian",
        "city": "Brno",
        "street": "Bozetechova 1/2",
        "zip_code": "61200",
        "country": "Czechia",
        "password": "iis_librarian"
    }
)
print(str(result.status_code) + " Register Librarian 1 [" + result.text + "] ")
# Register Librarian 2
result = post(
    url=API_URL + "api/auth/register/",
    data={
        "username": "librarian2",
        "email": "librarian2@iis.czleteron.net",
        "first_name": "IIS",
        "last_name": "Librarian2",
        "city": "Brno",
        "street": "Palackeho 12/1",
        "zip_code": "61201",
        "country": "Czechia",
        "password": "iis_librarian2"
    }
)
print(str(result.status_code) + " Register Librarian 2 [" + result.text + "] ")
# Register Librarian 3
result = post(
    url=API_URL + "api/auth/register/",
    data={
        "username": "librarian3",
        "email": "librarian3@iis.czleteron.net",
        "first_name": "IIS",
        "last_name": "Librarian3",
        "city": "Breclav",
        "street": "Sady 28. rijna 27/21",
        "zip_code": "69002",
        "country": "Czechia",
        "password": "iis_librarian3"
    }
)
print(str(result.status_code) + " Register Librarian 3 [" + result.text + "] ")
#######################################################################################################

# Role setup ##########################################################################################
# Login Administrator
result = post(
    url=API_URL + "api/auth/login/",
    json={
        "username": "admin@iis.czleteron.net",
        "password": "iis_admin"
    },
    headers={
        'Content-Type': 'application/json'
    }
)
token = 'Token ' + result.json()['token']
print(str(result.status_code) + " Login Administrator [" + result.text + "] ")
# Make Administrator
result = post(
    url=API_URL + "api/admin/setrole/administrator/",
    json={
        "key": ADMIN_KEY
    },
    headers={
        'Content-Type': 'application/json',
        'Authorization': token
    }
)
print(str(result.status_code) + " Make Administrator [" + result.text + "] ")
# Make Librarian
result = post(
    url=API_URL + "api/admin/setrole/4/librarian/",
    headers={
        'Content-Type': 'application/json',
        'Authorization': token
    }
)
print(str(result.status_code) + " Make Librarian [" + result.text + "] ")
# Make Librarian 2
result = post(
    url=API_URL + "api/admin/setrole/5/librarian/",
    headers={
        'Content-Type': 'application/json',
        'Authorization': token
    }
)
print(str(result.status_code) + " Make Librarian 2 [" + result.text + "] ")
# Make Librarian 3
result = post(
    url=API_URL + "api/admin/setrole/6/librarian/",
    headers={
        'Content-Type': 'application/json',
        'Authorization': token
    }
)
print(str(result.status_code) + " Make Librarian 3 [" + result.text + "] ")
# Make Distributor
result = post(
    url=API_URL + "api/admin/setrole/3/distributor/",
    headers={
        'Content-Type': 'application/json',
        'Authorization': token
    }
)
print(str(result.status_code) + " Make Distributor [" + result.text + "] ")
#######################################################################################################

# Create of libraries #################################################################################
result = post(
    url=API_URL + "api/library/create/",
    json={
        "name": "M??stsk?? knihovna v Praze",
        "description": "Barrandov",
        "city": "Praha",
        "street": "Wassermannova 926/16",
        "zip_code": "14300"
    },
    headers={
        'Content-Type': 'application/json',
        'Authorization': token
    }
)
print(str(result.status_code) + " Create library 1 [" + result.text + "] ")
result = post(
    url=API_URL + "api/library/create/",
    json={
        "name": "M??stsk?? knihovna B??eclav",
        "description": "MkB",
        "city": "B??eclav",
        "street": "N??rodn??ch hrdin?? 9",
        "zip_code": "69002"
    },
    headers={
        'Content-Type': 'application/json',
        'Authorization': token
    }
)
print(str(result.status_code) + " Create library 2 [" + result.text + "] ")
result = post(
    url=API_URL + "api/library/create/",
    json={
        "name": "M??stsk?? knihovna Znojmo",
        "description": "M??stsk?? knihovna ve Znojm??",
        "city": "Znojmo",
        "street": "Z??me??nick?? 288/9",
        "zip_code": "66926"
    },
    headers={
        'Content-Type': 'application/json',
        'Authorization': token
    }
)
print(str(result.status_code) + " Create library 3 [" + result.text + "] ")
#######################################################################################################

# Associate librarians with libraries #################################################################
result = post(
    url=API_URL + "api/library/1/associate/4/",
    headers={
        'Content-Type': 'application/json',
        'Authorization': token
    }
)
print(str(result.status_code) + " Associate librarian 1 with library 1 [" + result.text + "] ")

result = post(
    url=API_URL + "api/library/2/associate/5/",
    headers={
        'Content-Type': 'application/json',
        'Authorization': token
    }
)
print(str(result.status_code) + " Associate librarian 2 with library 2 [" + result.text + "] ")

result = post(
    url=API_URL + "api/library/3/associate/6/",
    headers={
        'Content-Type': 'application/json',
        'Authorization': token
    }
)
print(str(result.status_code) + " Associate librarian 3 with library 3 [" + result.text + "] ")
#######################################################################################################

# Create publications & add them to libraries #########################################################
result = post(
    url=API_URL + "api/publication/create/",
    json={
        "name": "The Fellowship of the Ring",
        "series": "The Lord of the Rings",
        "synopsis": "The first volume in J.R.R. Tolkien's epic adventure THE LORD OF THE RINGS One Ring to rule them all, One Ring to find them, One Ring to bring them all and in the darkness bind them.",
        "authors": "J.R.R. Tolkien",
        "language": "EN",
        "ISBN": "9780547928210",
        "date_of_publication": "2009-04-20T17:25:28.629000Z",
        "publisher": "HarperCollins",
        "genre": "Fantasy",
        "pages": 433,
        "tags": "lotr middleearth thehobbit jrrtolkien hobbit gandalf aragorn legolas sauron frodo elves elf gondor gimli gollum mordor mirkwood"
    },
    headers={
        'Content-Type': 'application/json',
        'Authorization': token
    }
)
print(str(result.status_code) + " Create publication 1 [" + result.text + "] ")
result = post(
    url=API_URL + "api/publication/create/",
    json={
        "name": "The Return of the King",
        "series": "The Lord of the Rings",
        "synopsis": "The Lord of the Rings', 'The awesome conclusion to The Lord of the Rings???the greatest fantasy epic of all time???which began in The Fellowship of the Ring and The Two Towers.",
        "authors": "J.R.R. Tolkien",
        "language": "EN",
        "ISBN": "9780547952024",
        "date_of_publication": "2009-04-20T17:25:28.629000Z",
        "publisher": "HarperCollins",
        "genre": "Fantasy",
        "pages": 352,
        "tags": "lotr middleearth thehobbit jrrtolkien hobbit gandalf aragorn legolas sauron frodo elves elf gondor gimli gollum mordor mirkwood"
    },
    headers={
        'Content-Type': 'application/json',
        'Authorization': token
    }
)
print(str(result.status_code) + " Create publication 2 [" + result.text + "] ")

result = post(
    url=API_URL + "api/publication/create/",
    json={
        "name": "Karant??na s modern??m fotrem",
        "series": "-",
        "synopsis": "Modern?? fotr, ??en??k a Nata??a v karant??n??! To si takhle jednoho proslun??n??ho odpoledne d?? n??kdo v ????n?? na stoj??ka u st??nku netop??ra na loupa??ku a za p??r m??s??c??, na opa??n?? stran?? zem??koule, jste vy zav??en?? doma, proto??e venku ????h?? smrt, ??ijete rou??ky a krot??te v????n?? hyperaktivn??ho ??kol??ka, jeho?? vzd??l??n?? ????ste??n?? padlo na v??s ??? ??koly jsou toti?? zav??en??. A vy postupn?? za??nete nen??vid??t v??echny ??leny dom??cnosti, co?? je praktick??, proto??e se s nik??m jin??m nest??k??te (ostatn?? ani nem????ete) a den za dnem, respektive m??s??c za m??s??cem v televizi sledujete st??le nov??ho a nov??ho ministra zdravotnictv??, kterak se st??le stejn??m premi??rem v z??dech n??rod informuje, ??e n??sleduj??c?? t??i t??dny budou kl????ov??. A tak za??nete nen??vid??t i v??echny ostatn????? Mezit??m samoz??ejm?? sem tam kr??tk?? a matouc?? ok??nka rozvoln??n?? a optimismu. Best in Covid ??? Made in ??esko!",
        "authors": "Dominik Landsman",
        "language": "CZ",
        "ISBN": "9788024945798",
        "date_of_publication": "2021-04-20T17:25:28.629000Z",
        "publisher": "Ikar(??R)",
        "genre": "Humor",
        "pages": 208,
        "tags": "karant??na best covid"
    },
    headers={
        'Content-Type': 'application/json',
        'Authorization': token
    }
)
print(str(result.status_code) + " Create publication 3 [" + result.text + "] ")

result = post(
    url=API_URL + "api/publication/create/",
    json={
        "name": " Tenkr??t o V??noc??ch",
        "series": "-",
        "synopsis": "V??noce jsou tradi??n?? naz??v??ny sv??tky klidu a m??ru, pro hrdiny pov??dek dev??ti soudob??ch ??esk??ch autor?? je to ov??em sp????e obdob?? pln?? nejistot, pochyb a ??asto tak?? t????iv?? samoty. Ale kdy jindy v????it ve ????astn?? konce ne?? pr??v?? o V??noc??ch?",
        "authors": "Petra Soukupov??, Petra Dvo????kov??, Anna Bolav??, Nellis Alice, Alena Morn??tajnov??, Marek Epstein",
        "language": "CZ",
        "ISBN": "9788024277677",
        "date_of_publication": "2021-01-11T17:25:28.629000Z",
        "publisher": "Listen",
        "genre": "Pr??za",
        "pages": 168,
        "tags": "christmas x-max loneliness"
    },
    headers={
        'Content-Type': 'application/json',
        'Authorization': token
    }
)
print(str(result.status_code) + " Create publication 4 [" + result.text + "] ")

result = post(
    url=API_URL + "api/publication/create/",
    json={
        "name": "T??tovy holky",
        "series": "Charlotte Staffordov??",
        "synopsis": "P??vodn?? nem??l v ??myslu zab??jet a ohro??ovat star?? lidi. Vyhled??val jen p????le??itosti si s nimi promluvit a zavzpom??nat. Jen??e to by se nesm??l vkr??dat do jejich lo??nic uprost??ed noci a krom?? vzpom??nek a pam??te??n??ch p??edm??t?? je zbavovat i toho nejcenn??j????ho, co jim je??t?? z??st??v?? ??? posledn??ch p??r let ??ivota mezi d??tmi a vnou??aty. V p??t??m d??le p????b??h?? detektivky Charlotte Staffordov?? se do hled????ku jej??ho vy??et??ovac??ho t??mu dost??vaj?? nezvan?? no??n?? host??, ze kter??ch ??ivotn?? okolnosti, zklam??n?? a trag??die u??inily zlo??ince. Charlotte Staffordov?? ??el?? jednomu z nejt????????ch p????pad?? v??bec. Nep??jde v n??m pouze o dopaden?? podez??el??ho d????v, ne?? se vyd?? za svoj?? dal???? ob??t??, ale tak?? o porozum??n?? vlastn?? ??ivotn?? cest??. Tento nev??edn?? detektivn?? rom??n nab??z?? v??c ne?? nap??t?? a vykreslen?? postupu policejn??ho vy??et??ov??n??. Poodhaluje ??ten????i, ??e trpk?? zklam??n?? a smutek ze ztr??ty milovan?? osoby m????e jedince zm??nit natolik, ??e se nezastav?? p??ed ni????m, aby zm??rnil svoje tr??pen??, a to i za cenu nejvy??????. Podle autor??in??ch vlastn??ch slov ji k seps??n?? tohoto rom??nu inspiroval skute??n?? osud pachatele, kter??ho b??hem svoj?? dlouholet?? kari??ry u policie zadr??ela a jeho?? zlo??in nebyl v prv?? ??ad?? veden zl??mi pohnutkami, ale utkv??lou p??edstavou o l??sce a?? za hrob.",
        "authors": "Sarah Flint",
        "language": "CZ",
        "ISBN": "9788027701285",
        "date_of_publication": "2021-11-08T17:25:28.629000Z",
        "publisher": "Vendeta",
        "genre": "Detektivn??",
        "pages": 368,
        "tags": "Beletrie horor thriller daddy"
    },
    headers={
        'Content-Type': 'application/json',
        'Authorization': token
    }
)
print(str(result.status_code) + " Create publication 5 [" + result.text + "] ")
# Associate Publication with Library
result = post(
    url=API_URL + "api/publication/1/associate/1/",
    headers={
        'Content-Type': 'application/json',
        'Authorization': token
    }
)
print(str(result.status_code) + " Associate Publication 1 with Library 1 [" + result.text + "] ")
result = post(
    url=API_URL + "api/publication/1/associate/2/",
    headers={
        'Content-Type': 'application/json',
        'Authorization': token
    }
)
print(str(result.status_code) + " Associate Publication 1 with Library 2 [" + result.text + "] ")
result = post(
    url=API_URL + "api/publication/2/associate/1/",
    headers={
        'Content-Type': 'application/json',
        'Authorization': token
    }
)
print(str(result.status_code) + " Associate Publication 2 with Library 1 [" + result.text + "] ")
result = post(
    url=API_URL + "api/publication/3/associate/1/",
    headers={
        'Content-Type': 'application/json',
        'Authorization': token
    }
)
print(str(result.status_code) + " Associate Publication 3 with Library 1 [" + result.text + "] ")
result = post(
    url=API_URL + "api/publication/4/associate/3/",
    headers={
        'Content-Type': 'application/json',
        'Authorization': token
    }
)
print(str(result.status_code) + " Associate Publication 4 with Library 3 [" + result.text + "] ")
result = post(
    url=API_URL + "api/publication/4/associate/1/",
    headers={
        'Content-Type': 'application/json',
        'Authorization': token
    }
)
print(str(result.status_code) + " Associate Publication 4 with Library 1 [" + result.text + "] ")
#######################################################################################################

# Order publications (& create voting) ################################################################
result = post(
    url=API_URL + "api/order/create/",
    json={
        "publication": 1,
        "library": 1,
        "date_of_order": "2021-11-28T10:19:05.173Z",
        "delivered": False,
        "number_of_books": 10,
        "price_per_book": 500,
        "total_price": 5000
    },
    headers={
        'Content-Type': 'application/json',
        'Authorization': token
    }
)
print(str(result.status_code) + " Create order on Publication 1 for library 1 [" + result.text + "] ")
result = post(
    url=API_URL + "api/order/create/",
    json={
        "publication": 2,
        "library": 1,
        "date_of_order": "2021-11-28T10:19:05.173Z",
        "delivered": False,
        "number_of_books": 10,
        "price_per_book": 500,
        "total_price": 5000
    },
    headers={
        'Content-Type': 'application/json',
        'Authorization': token
    }
)
print(str(result.status_code) + " Create order on Publication 2 for library 1 [" + result.text + "] ")
result = post(
    url=API_URL + "api/order/create/",
    json={
        "publication": 1,
        "library": 2,
        "date_of_order": "2021-11-28T10:19:05.173Z",
        "delivered": False,
        "number_of_books": 5,
        "price_per_book": 500,
        "total_price": 2500
    },
    headers={
        'Content-Type': 'application/json',
        'Authorization': token
    }
)
print(str(result.status_code) + " Create order on Publication 1 for library 2 [" + result.text + "] ")
result = post(
    url=API_URL + "api/order/create/",
    json={
        "publication": 3,
        "library": 3,
        "date_of_order": "2021-11-28T10:19:05.173Z",
        "delivered": False,
        "number_of_books": 1,
        "price_per_book": 200,
        "total_price": 200
    },
    headers={
        'Content-Type': 'application/json',
        'Authorization': token
    }
)
print(str(result.status_code) + " Create order on Publication 3 for library 3 [" + result.text + "] ")
result = post(
    url=API_URL + "api/order/create/",
    json={
        "publication": 4,
        "library": 3,
        "date_of_order": "2021-11-28T10:19:05.173Z",
        "delivered": False,
        "number_of_books": 20,
        "price_per_book": 500,
        "total_price": 10000
    },
    headers={
        'Content-Type': 'application/json',
        'Authorization': token
    }
)
print(str(result.status_code) + " Create order on Publication 4 for library 3 [" + result.text + "] ")
result = post(
    url=API_URL + "api/order/create/",
    json={
        "publication": 4,
        "library": 1,
        "date_of_order": "2021-11-28T10:19:05.173Z",
        "delivered": False,
        "number_of_books": 40,
        "price_per_book": 500,
        "total_price": 20000
    },
    headers={
        'Content-Type': 'application/json',
        'Authorization': token
    }
)
print(str(result.status_code) + " Create order on Publication 4 for library 1 [" + result.text + "] ")
#######################################################################################################

# deliver orders (& create books in libraries) ########################################################
result = post(
    url=API_URL + "api/order/1/deliver/",
    headers={
        'Content-Type': 'application/json',
        'Authorization': token
    }
)
print(str(result.status_code) + " Deliver order 1 [" + result.text + "] ")
result = post(
    url=API_URL + "api/order/2/deliver/",
    headers={
        'Content-Type': 'application/json',
        'Authorization': token
    }
)
print(str(result.status_code) + " Deliver order 2 [" + result.text + "] ")
result = post(
    url=API_URL + "api/order/4/deliver/",
    headers={
        'Content-Type': 'application/json',
        'Authorization': token
    }
)
print(str(result.status_code) + " Deliver order 3 [" + result.text + "] ")
result = post(
    url=API_URL + "api/order/5/deliver/",
    headers={
        'Content-Type': 'application/json',
        'Authorization': token
    }
)
print(str(result.status_code) + " Deliver order 4 [" + result.text + "] ")
result = post(
    url=API_URL + "api/order/6/deliver/",
    headers={
        'Content-Type': 'application/json',
        'Authorization': token
    }
)
print(str(result.status_code) + " Deliver order 5 [" + result.text + "] ")
#######################################################################################################

# Create book loans for multiple users ################################################################
result = post(
    url=API_URL + "api/bookloan/create/",
    json={
        "date_from": "2021-11-29T16:10:18.691Z",
        "date_to": "2021-12-29T16:10:18.691Z",
        "books": [
            1, 11, 15
        ]
    },
    headers={
        'Content-Type': 'application/json',
        'Authorization': token
    }
)
print(str(result.status_code) + " Create book loan 1 as admin [" + result.text + "] ")

result = post(
    url=API_URL + "api/bookloan/create/",
    json={
        "date_from": "2021-11-29T16:10:18.691Z",
        "date_to": "2021-12-29T16:10:18.691Z",
        "books": [
            26
        ]
    },
    headers={
        'Content-Type': 'application/json',
        'Authorization': token
    }
)
print(str(result.status_code) + " Create book loan 2 as admin [" + result.text + "] ")
# Log in as distributor and create a book loan
result = post(
    url=API_URL + "api/auth/login/",
    json={
        "username": "distributor@iis.czleteron.net",
        "password": "iis_distributor"
    },
    headers={
        'Content-Type': 'application/json'
    }
)
token2 = 'Token ' + result.json()['token']
print(str(result.status_code) + " Log in as distributor [" + result.text + "] ")

result = post(
    url=API_URL + "api/bookloan/create/",
    json={
        "date_from": "2021-11-29T16:10:18.691Z",
        "date_to": "2021-12-29T16:10:18.691Z",
        "books": [
            2, 14
        ]
    },
    headers={
        'Content-Type': 'application/json',
        'Authorization': token2
    }
)
print(str(result.status_code) + " Create book loan 3 as distributor [" + result.text + "] ")
# Log in as user and create a book loan
result = post(
    url=API_URL + "api/auth/login/",
    json={
        "username": "registred@iis.czleteron.net",
        "password": "iis_registred"
    },
    headers={
        'Content-Type': 'application/json'
    }
)
token3 = 'Token ' + result.json()['token']
print(str(result.status_code) + " Log in as user [" + result.text + "] ")

result = post(
    url=API_URL + "api/bookloan/create/",
    json={
        "date_from": "2021-11-29T16:10:18.691Z",
        "date_to": "2021-12-29T16:10:18.691Z",
        "books": [
            5, 13
        ]
    },
    headers={
        'Content-Type': 'application/json',
        'Authorization': token3
    }
)
print(str(result.status_code) + " Create book loan 4 as user [" + result.text + "] ")
# Log in as librarian 1 and create a book loan
result = post(
    url=API_URL + "api/auth/login/",
    json={
        "username": "librarian@iis.czleteron.net",
        "password": "iis_librarian"
    },
    headers={
        'Content-Type': 'application/json'
    }
)
token4 = 'Token ' + result.json()['token']
print(str(result.status_code) + " Log in as librarian 1 [" + result.text + "] ")

result = post(
    url=API_URL + "api/bookloan/create/",
    json={
        "date_from": "2021-11-29T16:10:18.691Z",
        "date_to": "2021-12-29T16:10:18.691Z",
        "books": [
            8
        ]
    },
    headers={
        'Content-Type': 'application/json',
        'Authorization': token4
    }
)
print(str(result.status_code) + " Create book loan 5 as librarian 1 [" + result.text + "] ")


# Log in as librarian 2 and create a book loan
result = post(
    url=API_URL + "api/auth/login/",
    json={
        "username": "librarian2@iis.czleteron.net",
        "password": "iis_librarian2"
    },
    headers={
        'Content-Type': 'application/json'
    }
)
token5 = 'Token ' + result.json()['token']
print(str(result.status_code) + " Log in as librarian 2 [" + result.text + "] ")

result = post(
    url=API_URL + "api/bookloan/create/",
    json={
        "date_from": "2021-11-29T16:10:18.691Z",
        "date_to": "2021-12-29T16:10:18.691Z",
        "books": [
            1
        ]
    },
    headers={
        'Content-Type': 'application/json',
        'Authorization': token5
    }
)
print(str(result.status_code) + " Create book loan 6 as librarian 2 [" + result.text + "] ")
# Log in as librarian 3 and create a book loan
result = post(
    url=API_URL + "api/auth/login/",
    json={
        "username": "librarian3@iis.czleteron.net",
        "password": "iis_librarian3"
    },
    headers={
        'Content-Type': 'application/json'
    }
)
token6 = 'Token ' + result.json()['token']
print(str(result.status_code) + " Log in as librarian 3 [" + result.text + "] ")

result = post(
    url=API_URL + "api/bookloan/create/",
    json={
        "date_from": "2021-11-29T16:10:18.691Z",
        "date_to": "2021-12-29T16:10:18.691Z",
        "books": [
            25
        ]
    },
    headers={
        'Content-Type': 'application/json',
        'Authorization': token6
    }
)
print(str(result.status_code) + " Create book loan 7 as librarian 3 [" + result.text + "] ")
#######################################################################################################

# Loan books as librarians ############################################################################
result = post(
    url=API_URL + "api/bookloan/1/loan/",
    headers={
        'Content-Type': 'application/json',
        'Authorization': token4
    }
)
print(str(result.status_code) + " Loan book loan 1 as librarian 1 [" + result.text + "] ")

result = post(
    url=API_URL + "api/bookloan/2/loan/",
    headers={
        'Content-Type': 'application/json',
        'Authorization': token6
    }
)
print(str(result.status_code) + " Loan book loan 2 as librarian 3 [" + result.text + "] ")

result = post(
    url=API_URL + "api/bookloan/3/loan/",
    headers={
        'Content-Type': 'application/json',
        'Authorization': token4
    }
)
print(str(result.status_code) + " Loan book loan 3 as librarian 1 [" + result.text + "] ")

result = post(
    url=API_URL + "api/bookloan/4/loan/",
    headers={
        'Content-Type': 'application/json',
        'Authorization': token4
    }
)
print(str(result.status_code) + " Loan book loan 4 as librarian 1 [" + result.text + "] ")
#######################################################################################################

# Rating publications #################################################################################
result = post(
    url=API_URL + "api/publication/1/rate/9/",
    headers={
        'Content-Type': 'application/json',
        'Authorization': token3
    }
)
print(str(result.status_code) + " Rate publication 1 as user [" + result.text + "] ")

result = post(
    url=API_URL + "api/publication/1/rate/8/",
    headers={
        'Content-Type': 'application/json',
        'Authorization': token4
    }
)
print(str(result.status_code) + " Rate publication 1 as librarian 1 [" + result.text + "] ")

result = post(
    url=API_URL + "api/publication/3/rate/6/",
    headers={
        'Content-Type': 'application/json',
        'Authorization': token4
    }
)
print(str(result.status_code) + " Rate publication 3 as librarian 1 [" + result.text + "] ")

result = post(
    url=API_URL + "api/publication/3/rate/0/",
    headers={
        'Content-Type': 'application/json',
        'Authorization': token
    }
)
print(str(result.status_code) + " Rate publication 3 as administrator [" + result.text + "] ")

result = post(
    url=API_URL + "api/publication/3/rate/2/",
    headers={
        'Content-Type': 'application/json',
        'Authorization': token2
    }
)
print(str(result.status_code) + " Rate publication 3 as distributor [" + result.text + "] ")
#######################################################################################################
# token - admin (id:1)
# token2 - distributor (id:2)
# token3 - reg. user (id:2)
# token4 - librarian (id:3), token5 - librarian 2 (id:5), token6 - librarian 3 (id:6)
