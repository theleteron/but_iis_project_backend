from requests import post

# Register Administrator
result = post(
    url="https://iis.czleteron.net/api/auth/register/",
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
print(result)
# Register Librarian
result = post(
    url="https://iis.czleteron.net/api/auth/register/",
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
print(result)
# Register Distributor
result = post(
    url="https://iis.czleteron.net/api/auth/register/",
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
print(result)
# Register Registred
result = post(
    url="https://iis.czleteron.net/api/auth/register/",
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
print(result)
# Login Administrator
result = post(
    url="https://iis.czleteron.net/api/auth/login/",
    json={
        "username": "admin@iis.czleteron.net",
        "password": "iis_admin"
    },
    headers={
        'Content-Type': 'application/json'
    }
)
token = 'Token ' + result.json()['token']
print(result)
# Make Administrator
result = post(
    url="https://iis.czleteron.net/api/admin/setrole/administrator/",
    json={
        "key": "4Xb3cKF0JQL5R8BOqv9vqSGo5MEWIVQPlrTsqMKtin3RK7G6I1BG6mYT4kky6G0R62E15G7TQi4qR3w09oJZBA8co8Om714a3pGGWZhCRSB5A673EHP0BG4v6U42jO00"
    },
    headers={
        'Content-Type': 'application/json',
        'Authorization': token
    }
)
print(result)
# Make Librarian
result = post(
    url="https://iis.czleteron.net/api/admin/setrole/2/librarian/",
    headers={
        'Content-Type': 'application/json',
        'Authorization': token
    }
)
print(result)
# Make Distributor
result = post(
    url="https://iis.czleteron.net/api/admin/setrole/3/distributor/",
    headers={
        'Content-Type': 'application/json',
        'Authorization': token
    }
)
print(result)
# Create Library
result = post(
    url="https://iis.czleteron.net/api/library/create/",
    json={
        "name": "Městská knihovna v Praze",
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
print(result)
result = post(
    url="https://iis.czleteron.net/api/library/create/",
    json={
        "name": "Městská knihovna Břeclav",
        "description": "MkB",
        "city": "Břeclav",
        "street": "Národních hrdinů 9",
        "zip_code": "69002"
    },
    headers={
        'Content-Type': 'application/json',
        'Authorization': token
    }
)
print(result)
result = post(
    url="https://iis.czleteron.net/api/library/create/",
    json={
        "name": "Městská knihovna Znojmo",
        "description": "Městská knihovna ve Znojmě",
        "city": "Znojmo",
        "street": "Zámečnická 288/9",
        "zip_code": "66926"
    },
    headers={
        'Content-Type': 'application/json',
        'Authorization': token
    }
)
print(result)
# Create Publication
result = post(
    url="https://iis.czleteron.net/api/publication/create/",
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
print(result)
result = post(
    url="https://iis.czleteron.net/api/publication/create/",
    json={
        "name": "The Return of the King",
        "series": "The Lord of the Rings",
        "synopsis": "The Lord of the Rings', 'The awesome conclusion to The Lord of the Rings—the greatest fantasy epic of all time—which began in The Fellowship of the Ring and The Two Towers.",
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
print(result)
result = post(
    url="https://iis.czleteron.net/api/publication/create/",
    json={
        "name": "Karanténa s moderním fotrem",
        "series": "-",
        "synopsis": "Moderní fotr, Čeněk a Nataša v karanténě! To si takhle jednoho prosluněného odpoledne dá někdo v Číně na stojáka u stánku netopýra na loupačku a za pár měsíců, na opačné straně zeměkoule, jste vy zavření doma, protože venku číhá smrt, šijete roušky a krotíte vášně hyperaktivního školáka, jehož vzdělání částečně padlo na vás – školy jsou totiž zavřené. A vy postupně začnete nenávidět všechny členy domácnosti, což je praktické, protože se s nikým jiným nestýkáte (ostatně ani nemůžete) a den za dnem, respektive měsíc za měsícem v televizi sledujete stále nového a nového ministra zdravotnictví, kterak se stále stejným premiérem v zádech národ informuje, že následující tři týdny budou klíčové. A tak začnete nenávidět i všechny ostatní… Mezitím samozřejmě sem tam krátká a matoucí okénka rozvolnění a optimismu. Best in Covid – Made in Česko!",
        "authors": "Dominik Landsman",
        "language": "CZ",
        "ISBN": "9788024945798",
        "date_of_publication": "2021-04-20T17:25:28.629000Z",
        "publisher": "Ikar(ČR)",
        "genre": "humor",
        "pages": 208,
        "tags": "karanténa best covid"
    },
    headers={
        'Content-Type': 'application/json',
        'Authorization': token
    }
)
print(result)
# Associate Publication with Library
result = post(
    url="https://iis.czleteron.net/api/publication/1/associate/1",
    headers={
        'Content-Type': 'application/json',
        'Authorization': token
    }
)
print(result)
result = post(
    url="https://iis.czleteron.net/api/publication/1/associate/2",
    headers={
        'Content-Type': 'application/json',
        'Authorization': token
    }
)
print(result)
result = post(
    url="https://iis.czleteron.net/api/publication/2/associate/1",
    headers={
        'Content-Type': 'application/json',
        'Authorization': token
    }
)
print(result)
result = post(
    url="https://iis.czleteron.net/api/publication/3/associate/1",
    headers={
        'Content-Type': 'application/json',
        'Authorization': token
    }
)
print(result)
# Order publications
result = post(
    url="https://iis.czleteron.net/api/order/create/",
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
print(result)
result = post(
    url="https://iis.czleteron.net/api/order/create/",
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
print(result)
result = post(
    url="https://iis.czleteron.net/api/order/create/",
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
print(result)
result = post(
    url="https://iis.czleteron.net/api/order/create/",
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
print(result)
# Deliver orders
result = post(
    url="https://iis.czleteron.net/api/order/1/deliver/",
    headers={
        'Content-Type': 'application/json',
        'Authorization': token
    }
)
print(result)
result = post(
    url="https://iis.czleteron.net/api/order/2/deliver/",
    headers={
        'Content-Type': 'application/json',
        'Authorization': token
    }
)
print(result)
result = post(
    url="https://iis.czleteron.net/api/order/4/deliver/",
    headers={
        'Content-Type': 'application/json',
        'Authorization': token
    }
)
print(result)
# Bookloan