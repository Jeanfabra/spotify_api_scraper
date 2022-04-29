import requests
import base64
import pandas as pd

URL_SPOTYFY = 'https://api.spotify.com/v1'
EP_ARTIST = '/artists/{artist_id}'
URL_SPOTYFY_SRCH = 'https://api.spotify.com/v1/search'
TOKEN = 'https://accounts.spotify.com/api/token'


def encoding():
    ''' Function that encodes the client id and client secret into base64'''
    
    client_id = "CLIENT ID HERE : CLIENT SECRET HERE"
    msg_bytes = client_id.encode("UTF-8")
    msg_base64 = base64.b64encode(msg_bytes)
    msg_decode = msg_base64.decode("UTF-8")

    return msg_decode

def get_token():
    ''' Function that updates the token '''

    params = {'grant_type': 'client_credentials'}
    headers = {'Authorization': 'Basic ' + encoding()}
    r_spoty = requests.post(TOKEN, headers=headers, data=params)
    if r_spoty.status_code != 200:
        print('Error en la requests', r_spoty.json())
    return r_spoty.json()["access_token"]
    
def get_artist_id(artist):
    ''' Function that finds the ID for a search artist '''
    token = get_token()
    header = {'Authorization': 'Bearer {}'.format(token)}
    srch_params = {'q' : artist, 'type' : 'artist'}
    get_url = requests.get(URL_SPOTYFY_SRCH, headers=header, params=srch_params)
    df = pd.DataFrame(get_url.json()['artists']['items'])

    artist_id = df.sort_values(by = "popularity", ascending= False).iloc[0]['id']

    return artist_id


def obtener_discografia(artist_id, return_name = False, page_limit = 50, country = None):
    ''' Function that obtains the albums of the desire artist '''
    token = get_token()
    url = f'https://api.spotify.com/v1/artists/{artist_id}/albums'
    header = {'Authorization': 'Bearer {}'.format(token)}
    params = {'limit': page_limit,
              'offset': 0,
              'country': country}
    lista = []
    r = requests.get(url, headers = header, params = params)

    if r.status_code != 200:
        print('Error en la requets')
        return None
    if return_name:

        lista += [(item['id'], item['name'],"Año:{}".format(item['release_date']) ) for item in r.json()['items']]
    else:
        lista += [(item['name'],"Año:{}".format(item['release_date'])) for item in r.json()['items']]


    '''
    
    while r.json()['next']:
        r = requests.get(r.json()['next'], headers = header)
        if return_name:
            lista += [(item['id'], item['name']) for item in r.json()['items']]
        else:
            lista += [item['id'] for item in r.json()['items']]
    
    '''
    return lista

def get_tracks(discografia_id, return_name = False, page_limit = 50, market = None):
    ''' Function that gets all the tracks inside a specific album '''

    album_id = str(input('Please input the album\'s id: '))
    token = get_token()
    url = f'https://api.spotify.com/v1/albums/{album_id}/tracks'
    header = {'Authorization': 'Bearer {}'.format(token)}
    params = {
        'limit': page_limit,
        'offset': 0
    }

    tracks = []
    r = requests.get(url, headers = header, params = params)
    if r.status_code != 200:
        print('Error en la requests')
        return None
    if return_name:
        tracks += [(i['id'], i['name']) for i in r.json()['items']]
    else:
        tracks += [(i['name']) for i in r.json()['items']]
    
    return tracks

def run():

    print('This program will obtain the Discography of a giving artist')
    artist_name = str(input('Please give me a artist name: '))
    artist_id = get_artist_id(artist_name)
    discografia = obtener_discografia(artist_id, return_name = True)
    discografia_id = obtener_discografia(artist_id, return_name = True)
    print('This is the Discography:')
    counter = 1
    for i in discografia:
        print(counter, i)
        counter += 1

    while True:
        choice = str(input("Do you wish to know the songs from any album? y/n: "))
        if choice == "y":
            tracks = get_tracks(discografia_id)
            print('This are the songs of the chosen album:')
            counter = 1
            for i in tracks:
                print(counter, i)
                counter += 1
            break

        elif choice == "n":
            print('Closing the program')
            break
        else:
            print('Please input a valid answer')
        

if __name__ == '__main__':
    run()
