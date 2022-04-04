import http.client, urllib.parse, re

# Regex para extraer distintos datos de los responses
regex_ssid = re.compile(r"=\w*\b")
regex_ora = re.compile(r"ORA_WWV-\S{24}")
regex_loc = re.compile(r"/ords/[\S\s]*")
regex_form_inputs = re.compile(r"name=\"(p_\w*)\" value=\"(\w*)\"")
regex_form_psalt = re.compile(r"value=\"([\d]*)\" id=\"pSalt\"")
regex_form_otros = re.compile(r"id=\"pPageItemsProtected\" value=\"([\S]*)\"")

# GET request para extraer la cookie PHPSSID 
con = http.client.HTTPSConnection("www.enteoperador.org")
con.request("GET", "", "", {})
response = con.getresponse()
con.close()
cookie_ssid = regex_ssid.search(response.getheader('Set-Cookie'))[0]

# GET request para extraer cookie ORA_WWV_APP_102
con = http.client.HTTPSConnection("www.enteoperador.org:7778")
con.request("GET", "/ords/f?p=102:1", "", {})
response = con.getresponse()
con.close()
cookie_ora = regex_ora.search(response.getheader('Set-Cookie'))[0]
location = regex_loc.search(response.getheader('Location'))[0]

# Guardar datos de cookies en el header para requests futuros
headers = {
 'Cookie': 'ORA_WWV_APP_102='+cookie_ora+'; '+
           'PHPSSID'+cookie_ssid
,
}

# GET request para extraer p_instance, p_json y otros inputs del wwv_flow form
con = http.client.HTTPSConnection("www.enteoperador.org:7778")
con.request("GET", location, "", headers)
response = con.getresponse().read().decode('utf-8')
con.close()
params = {} 
p_instance = ""
for match in regex_form_inputs.findall(response):
    params[match[0]] = '102' if match[0] == 'p_request' else match[1]
    p_instance = match[1] if match[0] == 'p_instance' else p_instance
p_salt = regex_form_psalt.search(response).groups()[0]
params['p_debug'] = ''
params['p_json'] = {
    'pageItems': {
        'itemsToSubmit': [],
        'protected': regex_form_otros.findall(response)[0],
        'rowVersion': '',
        'formRegionChecksums': []
    },
    'salt': p_salt
}

# Encontrar p_request mediante un POST al wwv_flow form de APEX
con = http.client.HTTPSConnection("www.enteoperador.org:7778")
con.request("POST", "/ords/wwv_flow.accept", urllib.parse.urlencode(params), headers) # Pareciera que la URL no responde
response = con.getresponse()                                                          # como se espera al POST
con.close()
# TODO: probar otra URL, idk
