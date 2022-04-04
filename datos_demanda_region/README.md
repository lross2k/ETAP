# Datos de demanda Ente Operador

Este script aún no está completo, se empezará a documentar el proceso que se ha seguido sobre
el desarrollo del mismo (porque considero que ha sido un caso interesante y no tan común)

Los datos obtenidos de la página web son accesibles de forma pública, por lo tanto este script
sólo facilita la lectura de los mismos y no viola ninguna política explicitamente mencionada 
en el sitio web de origen

# TODO
- Enviar form al servidor de Oracle APEX
- Obtener y leer los datos del form mediante GET
- Solicitar los datos finales al servidor de APEX

# Proceso seguido
- Se intentó enviar un POST a https://www.enteoperador.org:7778/ords/wwv_flow.ajax esperando 
una respuesta con los datos, sin embargo no fue aceptada.
- Analizando mediante las dev tools de Firefox se encontró que el POST request incluye múltiples 
headers entre los cuales van ciertas cookies importantes ORA_WWV_APP_102, ORA_WWV_APP_101 y 
PHPSESSID, se cambia el enfoque para encontrar cómo obtener estas.
- Son encontradas las dos cookies de ORA_*_10* al enviar un GET a 
www.enteoperador.org:7778/ords/f?p=102:1 y www.enteoperador.org:7778/ords/f?p=101:1 según el sitio
en que se tenga interés.
- El PHPSSID es encontrado al enviar el GET inicial para la página, ya sea en 
https://www.enteoperador.org/inicio-2/curva-de-demanda-por-paises/ o bien 
https://www.enteoperador.org/inicio-2/curva-de-demanda-regional/.
- Nuevo intento de conseguir los datos directamente con el POST necesario, sin embargo las cookies
no son suficiente, se encuentra que el payload del POST también tiene unos datos únicos y 
necesarios para la respuesta del servidor.
- Entre los requests observados con las dev tools se encuentra un html que es insertado al sitio 
final de alguna manera, al leer este se encuentra uno de los datos necesarios, y otro se menciona 
pero no tiene su valor, a continuación se muestra un exctracto del formato encontrado.
```html
<form action="wwv_flow.accept" method="post" name="wwv_flow" id="wwvFlowForm" novalidate  autocomplete="off">
  <input type="hidden" name="p_instance" value="10720467546029" id="pInstance" />
  . . .
  <input type="hidden" name="p_request" value="" id="pRequest" />
  . . .
</form>
```
- Se extrae exitosamente el p_instance que debe incluirse con el cuerpo del POST, sin embargo no 
es suficiente para completar el request, hace falta encontrar el p_request de alguna manera.
- Con base en [respuesta de StackOverflow](https://stackoverflow.com/questions/68322689/python-requests-how-to-get-value-of-blank-hidden-input/68350585#68350585) se añade a los pasos 
del script el enviar un GET con el form encontrado previamente.
