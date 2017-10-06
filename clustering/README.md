# Practico 1: Clustering

### Introducción

En este trabajo hicimos [clustering](https://es.wikipedia.org/wiki/Algoritmo_de_agrupamiento) sobre un corpus el cual es un conjunto de notas de [la voz del interior](http://www.lavoz.com) (esta en el directorio del repositorio). Para ello tuve que preprocesar las palabras para normalizarlas y poder realizar un análisis morfosintáctico/sintáctico. Luego vectorizar las palabras utilizando algún críterio de reducción de dimensionalidad.
Por una desición propia fui combinando varias formas de normalización junto con vectorización. Más adelante iré explicando los métodos utilizados y como fue mejorando la calidad de los clusters.
Voy a dividir mi trabajo en diferentes intentos explicando el mejoramiento de la calidad del clustering.

### Pre-procesamiento
----------------------------------------------------------------------------------------------------

Utilice varios procedimientos de pre-procesamiento (que los fui combinando). Aquí listaré un par de ellos

#### Normalización y tokenizador

Antes de cualquier procesamiento tuve que normalizar el texto (utilizando una librería de python [re](https://docs.python.org/3/library/re.html)) debido a que tenía muchos cáracteres no necesarios para este problema. Por ejemplo al principio de cada nota aparecía un "&número" donde número es un dígito de 3 decimales.
Luego de esta normalización tokenize el corpus en oraciones y palabras utilizando [nltk](http://www.nltk.org/). Sólo deje las palabras, es decir quite signos de puntuación, puntos, comas, etc. Además transforme todas las ocurrencias de números en la palabra *num* (obviamente después del análisis morfosintactico).

#### Lematización

En algunos casos utlice lemmatización. Para ello utilice [lexiconista](http://www.lexiconista.com/datasets/lemmatization/) debido a que no encontre ninguna librería decente que haga lemmatización en Español.

#### Taggeador y análisis morfosintáctico

Para taggear utilice dos taggeadores para comparar resultados. El primero de ellos fue [standford](https://nlp.stanford.edu/software/tagger.shtml) y luego [spacy](https://spacy.io). Además este último hace un análisis de identidad y triplas de dependencia.

#### Eliminación de stopwords

Luego de tokenizar y hacer el análisis morfosintactico quitamos las stopwords.

### Vecorización
--------------------------------------------------------------------------------------------------------

Para vectorizar utilice diferentes features dependiendo el procesamiento previo. Cuando taggeo solamente:
1) POS tag de palabra anterior, siguiente y actual.
2) Si la palabra, palabra anterior y palabra siguiente es un título.
3) Palabra anterior y siguiente.
4) Si es el tagger de standford quedarme con los primeros dos caracteres (debido a que los primeros cáracteres definen que tipo de POS es). Esto con la palabra, palabra anterior y siguiente.

Por otro lado si hago un árbol de parseo, taggeo y análisis de identidad utilizo los suguientes features:
1) POS de la palabra, palabra anterior y siguiente.
2) Triplas de dependencia.
3) Tags de la anterior palabra en la oración (de spacy, ejemplo: si es singular, femenino, etc). También tags de la palabra en sí.

En el siguiente ejemplo se muestra los features con sus respectivas ocurrencias
> {'word-1.totalmente': 1, 'flat.ricardo': 1, 'word+1.lechoso': 1, 'ADJ__Number-1.Sing': 20, 'conj.bandera': 1, 'nsubj.supermercado': 1, 'word-1.raza': 6, 'word+1.<END>': 96, 'ADJ__Gender-1.Masc': 21, 'obj.definir': 2, 'VERB__Mood-1.Sub': 2, 'fixed.de': 2, 'POS+1.ADP': 15, T__PunctType+1.Dash': 3, 'word-1.polvo': 2, 'csubj.dependencia': 1, 'Tense-1.Pres': 28, 'NUM__Number-1.Plur': 1, 'POS-1.PRON': 3, 'Number.Plur': 112, 'NOUN__Gender.Masc': 157, .....


#### Normalización de los vectores

Debido a que utilice ocurrencias de los features fue muy importante normalizar los vectores. Luego de correr k-means descubrí que muchos clusters tenían un sólo elemento por lo que noté que esas palabras tenían una gran ocurrencia en el corpus. Al tener muchas ocurrencias el conteo de features es muy elevada de modo que esa palabra queda sóla en el espacio. Para ello utilice una herramienta de [sklearn](http://scikit-learn.org/stable/modules/preprocessing.html).

#### Reducción de dimensionalidad

Además de normalizar, también reducí la dimensionalidad de dos maneras: con [truncated svd](http://scikit-learn.org/stable/modules/generated/sklearn.decomposition.TruncatedSVD.html) y dejando solamente las palabras que aparecen más de 150 veces.

### Clusterización
---------------------------------------------------------------------------------------------------

Para cluster utilizamos al famosa técnica [K-means](http://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html). Una incomodidad que me surgio fue como elegir el mejor K, por lo que utilice la *técnica del codo* (feo español) para convencerme de que K utilizar (al final no resulto muy útil).
![elbow metho](Figure_2.png)

Lo que podríamos concluir de este gráfico es que deberíamos usar 20 a 30 clusters (pero no fue así :p).

### Resultados y análisis
-------------------------------------------------------------------------------------------------

#### Primer intento

| Proceso | / |
|:----:|:-:|
| Tokenización | SI  |
| StopWords                       | NO  |
| Lemmatización                   | NO  |
| Tagger                          | Sta |
| Pos                             | SI  |
| Palabras con poca ocurrenciass  | SI  |
| Palabras repetidas              | SI  |
| Triplas de dependencias         | NO  |
| K (K-means)                     | 27  |
| Normalización de matriz         | NO  |
| Reducción de dimensionalidad    | NO  |

En este cluster no teníamos en cuenta ni la concuerrencia de una palabra ni si era repetida.

[CLUSTER](cl1.cl). Se eliminaron las stop words... pero nada cambiaba.

##### Conclusión

Este clustering no sirvio para nada porque los clusters eran sumamente grandes, además de que aparecían las mismas palabras en múltiples clusters. Palabras con ocurrencias pequeñas/grandes arruinaban el cluster.

#### Segundo intento

| Proceso | / |
|:----:|:-:|
| Tokenización | SI  |
| StopWords                       | NO  |
| Lemmatización                   | NO  |
| Tagger                          | Spa |
| Pos                             | SI  |
| Palabras con poca ocurrenciass  | NO  |
| Palabras repetidas              | NO  |
| Triplas de dependencias         | SI  |
| K (K-means)                     | 27  |
| Normalización de matriz         | NO  |
| Reducción de dimensionalidad    | NO  |

Debido a que todavía no quise aumentar el número de cluster probe una segunda alternativa. La primera diferencia es que empecé utilizando triplas de dependencia por lo que va a grupar morfologicamente. Además los features serán contados por número de ocurrencias. Elimine palabras repetidas.

[CLUSTER](cl2.cl)

##### Conclusión

Empezó a tener un poco más de sentido el clustering, sin embargo quería que una palabra en diferente modo sea una sola palabra (caso de cluster 11 y 22). Había avanzado mucho con respecto al primer intento.

###### Ejemplo:

* 2 {'gobierno', 'ley', 'parte', 'vez', 'ciudad', 'provincia'}
* 8 {'si'}
* 11 {'años', 'millones'}
* 17 {'aires', 'argentina', 'villa', 'josé', 'unidos', 'justicia', 'capital', 'federal', 'buenos', 'policía', 'san', 'luis', 'río', 'cámara', 'juan', 'maría', 'carlos', 'cristina', 'nación', 'general', 'daniel', 'fernández', 'schiaretti', 'kirchner'}
* 22 {'año', 'país'}
* 21 {'información', 'seguridad', 'cantidad', 'zona', 'situación', 'salud', 'gestión', 'medida', 'relación', 'sociedad', 'historia', 'decisión', 'personas', 'horas', 'manera', 'agua', 'planta', 'empresas', 'causa', 'producción', 'hora', 'forma', 'gente', 'política', 'campaña', 'familia', 'escuela', 'mayoría', 'construcción', 'empresa', 'vida', 'posibilidad', 'investigación', 'mujer', 'obra', 'semana', 'casa', 'deuda', 'oposición', 'falta', 'reunión', 'educación', 'cuenta', 'crisis', 'presidenta', 'muerte', 'actividad'}

#### Tercer Intento

| Proceso | / |
|:----:|:-:|
| Tokenización | SI  |
| StopWords                       | NO  |
| Lemmatización                   | SI  |
| Tagger                          | Spa |
| Pos                             | SI  |
| Palabras con poca ocurrenciass  | NO  |
| Palabras repetidas              | NO  |
| Triplas de dependencias         | SI  |
| K (K-means)                     | 27  |
| Normalización de matriz         | NO  |
| Reducción de dimensionalidad    | NO  |

Lo importante en este cluster fue que lemmatice. Esto causa que sólo el lemma este en el cluster mejorando la calidad de los clusters.

El [CLUSTER](cl3.cl)

###### Ejemplo:

* 1 {'ser'}
* 2 {'num'}
* 4 {'pesos'}
* 8 {'deber', 'ir'}
* 9 {'defender', 'bajar', 'votar', 'afectar', 'tras', 'cerrar', 'hablar', 'advertir', 'recordar', 'funcionar', 'quedo', 'definir', 'solicitar', 'llamar', 'evitar', 'depender', 'vario', 'aparecer', 'acompañar', 'apoyar', 'declarar', 'aplicar', 'precisar', 'elegir', 'analizar', 'adelantar', 'paso', 'addmitir', 'asistir', 'requerir', 'controlar', 'proponer', 'convertir', 'surgir', 'ubicar', 'aceptar', 'sacar', 'opinar', 'crecer', 'investigar', 'apuntar', 'insistir', 'rechazar', 'ninguno', 'preguntar', 'levantar', 'reclamar', 'estudiar', 'corresponder', 'acusar', 'utilizar', 'calificar', 'coincidir', 'reducir', 'destacar', 'principal', 'ocurrir', 'escuchar', 'confirmar', 'publicar', 'cincar', 'remarcar', 'superar', 'instalar', 'ayudar', 'caer', 'conocer', 'anticipar', 'impulsar', 'estimar', 'subir', 'impedir', 'responder', 'resolver', 'mejorar', 'entregar', 'plantear', 'manifestar', 'ingresar', 'cuestionar', 'creer', 'actuar', 'elevar', 'reconocer', 'detener', 'convocar', 'reunir', 'ratificar', 'perder', 'expresar', 'comprar', 'parecer', 'referir', 'obtener', 'aprobar', 'avanzar', 'sufrir', 'iniciar', 'prever', 'jugar', 'continuar', 'imponer', 'suceder', 'significar', 'sumar', 'destinar', 'distinto', 'participar', 'morir', 'cumplir', 'establecer', 'conseguir', 'ofrecer', 'exigir', 'revelar', 'ocupar', 'trasladar', 'implicar', 'lanzar', 'intentar', 'cubrir', 'integrar', 'cuyo', 'viajar', 'cuatro', 'concluir', 'abrir', 'económico', 'costar', 'ordenar', 'incrementar', 'busccar', 'cobrar', 'provocar', 'mientras', 'crear', 'construir', 'encabezar', 'ganar', 'necesitar', 'decidir', 'sino', 'representar', 'pretender', 'aclarar', 'fijar', 'alcanzar', 'determinar', 'enviar', 'suponer', 'negar', 'obligar', 'disponer', 'incluir', 'figurar', 'privar', 'vender', 'manejar', 'anunciar', 'demostrar', 'empezar', 'aportar', 'entender', 'servir', 'comentar', 'pensar', 'mostrar', 'asumir', 'registrar', 'garantizar'}
* 16 {'mil', 'do', 'tres'}
* 23 {'mismo', 'cada', 'alguno'}

##### Conclusión

Los clusters empezaron a tener más sentido, sin embargo en algunos casos empezaron a quedar singletones y en otros casos clusters extremadamente grandes. Cinco clusters quedaron muy grandes y el resto quedó singletones o muy pequeños.

Después de ver el ejemplo pude ver que las palabras que aparecían muchas veces quedaban solas. La explicación que le pude dar fue que las ocurrencias de features eran muy altas por lo que las palabras quedaban solas en el espacio.
Ejemplo: num aparece 106744 con alrededor de 31700 features.



#### Últimos intentos

Debido a que no quiero hacer eterno el informe voy a contar por arriba un par de intentos.
El problema de los singetones era muy grave. ¿Que alternativas tenía? Normalizar los vectores, cambiar totalmente la ingeniería de features (no era viable debido a la falta de tiempo), intentar con reducción de dimensionalidad (se que no iba a cambiar mucho). Además clusters quedaban sumamente grandes e ileigles por lo que había que aumentar el K en K-means. Después de varios intentos pude establecer que de 120~130 daba bastante bien.
También me di cuenta que si dejaba las palabras con más de 150 ocurrencias los clusters daban mejor.
Probe todas las opciones (salvo lo de cambiar la ingeniera de features), pero el que dio mejor resultado fue normalizar sin reducción de dimensionalidad, es decir cambiar número de clusters, quitar las palabras con menos de 150 ocurrencias y normalizar los vectores de palabras. 

##### Intento con reducción de dimensionalidad

Reducí a 300 dimensiones.

| Proceso | / |
|:----:|:-:|
| Tokenización | SI  |
| StopWords                       | NO  |
| Lemmatización                   | SI  |
| Tagger                          | Spa |
| Pos                             | SI  |
| Palabras con poca ocurrenciass  | NO  |
| Palabras repetidas              | NO  |
| Triplas de dependencias         | SI  |
| K (K-means)                     | 120 |
| Normalización de matriz         | NO  |
| Reducción de dimensionalidad    | SI  |

[CLUSTER](cl4.cl)

###### Ejemplo:

* 0 {'nadie', 'nadar', 'quién', 'alguien', 'cuál'}
* 1 {'ser'}
* 2 {'num'}
* 3 {'parir'}
* 4 {'hacer'}
* 5 {'haber'}
* 6 {'llegar', 'realizar'}
* 22 {'schiaretti', 'policía', 'kirchner', 'argentina', 'justicia', 'nación'}
* 44 {'menos', 'casi'}
* 94 {'comenzar', 'permitir', 'volver', 'parecer', 'seguir', 'venir'}
* 108 {'además', 'luego', 'después'}
* 118 {'ocho', 'siete', 'nueve', 'seis'}


###### Conclusión

Podemos ver que el sentido la calidad de los clusters aumento significativamente. Sin embargo seguimos con el probelema del tercer intento (singletones).


##### Intento con normalización de vectores


| Proceso | / |
|:----:|:-:|
| Tokenización | SI  |
| StopWords                       | NO  |
| Lemmatización                   | SI  |
| Tagger                          | Spa |
| Pos                             | SI  |
| Palabras con poca ocurrenciass  | NO  |
| Palabras repetidas              | NO  |
| Triplas de dependencias         | SI  |
| K (K-means)                     | 120 |
| Normalización de matriz         | SI  |
| Reducción de dimensionalidad    | NO  |


[CLUSTER](cl5.cl)

###### Ejemplo:

* 7 {'partido', 'cristina', 'ramón', 'ministerio', 'luiz', 'néstor', 'olga', 'federación', 'programa', 'barack', 'sebastián', 'unión', 'mesa', 'juzgado', 'the', 'raúl', 'concejo', 'víctor', 'benedicto', 'instituto', 'secretaría', 'mauricio', 'jorge', 'villa', 'fuerzas', 'daniel', 'junta', 'marcelo', 'consejo', 'agencia', 'david', 'defensoría', 'juan', 'ee', 'claudio', 'héctor', 'casa', 'aguas', 'sergio', 'palacio', 'marcos'}
* 20 {'num', 'cincar', 'dos', 'seis', 'ambos', 'numº', 'do', 'cuatro', 'nueve', 'tres', 'ocho', 'siete'}
* 38 {'domingo', 'sábado', 'lunes', 'viernes', 'jueves', 'martes', 'miércoles'}
* 50 {'giacomino', 'morales', 'alfonsín', 'mujica', 'piñera', 'timerman', 'moreno', 'cobos', 'carrió', 'campana', 'sota', 'serra', 'duhalde', 'oyarbide', 'correa', 'rossi', 'boudou', 'caminera', 'castro', 'zapatero', 'sanz', 'mestre', 'menem', 'méndez', 'aguad', 'scioli', 'vido', 'bush', 'silva', 'solanas', 'grahovac', 'menéndez', 'riutort', 'narváez', 'moyano', 'sosa', 'yanicelli', 'accastello', 'caserio', 'binner', 'xvi', 'kirchner'}
* 51 {'posición', 'nene', 'resolución', 'ideo', 'documentación', 'suerte', 'controversia', 'impunidad', 'reunión', 'razón', 'facultar', 'decisión', 'estrategia', 'camioneta', 'comparación', 'tragedia', 'fecho', 'historia', 'investigación', 'incertidumbre', 'sequía', 'cuestión', 'excepción', 'ley', 'auditoría', 'condición', 'gente', 'votación', 'inflación', 'normativo', 'vez', 'ordenanza', 'verdad', 'visión', 'modalidad', 'mamá', 'ceremonia', 'manera', 'distanciar', 'misión', 'versión', 'discusión', 'actualidad', 'licitación', 'frase', 'intención', 'realidad', 'lectura', 'reglamentación', 'reacción', 'ocasión', 'oportunidad', 'solución', 'situación', 'iniciativo', 'información', 'convocatorio', 'etapa', 'noche', 'madrugar', 'oposición', 'tendencia', 'multitud', 'problemático'}
* 86 {'chicago', 'unidos', 'libia', 'innviron', 'crese', 'mercosur', 'irán', 'epec', 'arizona', 'grecia', 'europa', 'botnia', 'k', 'dios', 'g-num', 'tamse', 'pro', 'suoem', 'latinoamérica', 'ejecutivo', 'cuba', 'gualeguaychú', 'suquía', 'wikileaks', 'apross', 'facebook', 'israel', 'unicameral', 'senado'}
* 100 {'gaza', 'china', 'franco', 'unasur', 'rosario', 'uia', 'córdoba', 'egipto', 'justicia', 'ecuador', 'indec', 'dilma', 'américa', 'cta', 'bicentenario', 'washington', 'ong', 'francia', 'nación', 'españa', 'colombia', 'farc', 'argentina', 'anses', 'rusia', 'ucr', 'venezuela', 'bolivia', 'alemania', 'onu', 'brasil', 'toledo', 'ersep', 'jaime', 'pt'}
* 101 {'cubano', 'venezolano', 'uruguayo', 'brasileño', 'argentino', 'griego', 'humanar', 'libio', 'chileno', 'electrónico', 'solidario', 'norteamericano', 'alemán', 'conservador', 'español', 'francés', 'mejicano', 'porteño', 'santafesino', 'ruso', 'colombiano', 'chino', 'inmobiliario', 'británico', 'boliviano', 'egipcio', 'italiano', 'climático', 'europeo'}
* 103 {'punilla', 'colón', 'bogotá', 'malvinas', 'catamarca', 'ganancias', 'roca', 'paraguay', 'videla', 'ríos', 'chile', 'luna', 'unc', 'salta', 'clarín', 'flores', 'méxico', 'japón', 'ferreyra', 'india', 'fmi', 'cosquín', 'tucumán', 'calamuchita', 'madrid', 'alberdi', 'ue', 'pueyrredón', 'garzón', 'italia', 'perón', 'perú', 'rioja', 'belgrano', 'diputados', 'mendoza', 'parís', 'uruguay'}
* 109 {'peso', 'euro', 'dólar'}


###### Conclusión
Gracias a la normalización el problema de los singletones y clusters muy grandes había desaparecido. Claramente aumento en gran medida la calidad del clustering. El único problema sería (a priori) la velocidad de Kmeans.


##### Intento con normalización de vectores y reducción de dimensionalidad

| Proceso | / |
|:----:|:-:|
| Tokenización | SI  |
| StopWords                       | NO  |
| Lemmatización                   | SI  |
| Tagger                          | Spa |
| Pos                             | SI  |
| Palabras con poca ocurrenciass  | NO  |
| Palabras repetidas              | NO  |
| Triplas de dependencias         | SI  |
| K (K-means)                     | 120 |
| Normalización de matriz         | SI  |
| Reducción de dimensionalidad    | SI  |

El [CLUSTER](cl6.cl).

###### Conclusión:
Como no quiero hacerlo tan largo al informe se podría decir que es parecido al anterior pero con menos calidad. Lo positivo de reducir dimensionalidad es que Kmeans corre a mayor velocidad.

------------------------------------------------------------------------------------------------------
# Práctico 2: Continuación

### Método de feature supervisado

El método de feature supervisado que utilice fue eliminar las palabras por el número de ocurrencias. Pero ¿que parámetro iba a utilizar para eliminar concurrencias?, es decir ¿entre cuantas concurrencias era conveniente dejar la palabra?. Para ello me ayude de la librería [panda](http://pandas.pydata.org) para sacar estadísticas acerca del corpus.

A continuación mostraré como tome la desición.

Primero que todo mostraré las ocurrencias de las palabras:

106744 num
78739 ser
47437 parir
31169 haber
22055 tener
19508 comer
18256 año
17889 poder
17412 hacer
13714 córdoba
13098 decir
12253 ciento
11335 entrar
10466 si
10275 partir
9989 sobrar
9375 ayer
9137 pasar
8995 do
8751 deber
8140 millón
8058 nacional
7884 político
7747 país
7740 peso
7581 día
7498 ir
6689 mil
6688 provincia
6644 casar
... ...
2982 san
2979 nación
2960 frente
2946 causar
2937 grupo
2936 ministro
2924 derecho
2915 kirchner
2846 carlos
2819 barrio
2803 propio
2775 aumentar
2773 venir
2771 diario
2771 buenos
2762 federal
2762 considerar
2759 temer
2757 indicar
2752 aires
2710 argentino
2709 momento
2702 resultar
2685 capital
2684 cuatro
2674 fiscal
2669 gran
2653 saber
2646 zona
2631 villa
.....
1 evaristo
1 juliette
1 prolifera
1 paracelso
1 claroscuro
1 recogerse
1 ramin
1 cerradísimo
1 sobresalían
1 observante
1 digiten
1 reanudan
1 estratégicos
1 exigió
1 ediberto
1 sencadenará
1 silajes
1 pierdan
1 copista
1 prodemocráticos
1 alou
1 preadjudicados
1 aríngoli
1 educacionales
1 modernista
1 wilfred
1 escrachados
1 sanofi
1 visionarios
1 yaguaribe
.. ...
1 reformularlos
1 municipaliad
1 jazaro
1 considerada
1 saneamientos
1 ceramista
1 layne
1 maltratándolas
1 coloniales
1 fenomenología
1 uspallata
1 ordovícica
1 vinchina
1 ingelmo
1 multifocal
1 cratón
1 granuja
1 soltaron
1 misilísticas
1 neutralizadas
1 sacnciones
1 remarcan
1 reinventarlos
1 vitta
1 contraponerse
1 litoraleños
1 barreneche
1 rajarlos
1 barilochense
1 guirnalda

150>=x<14000 mean: 753.0651955867603
150>=x<14000: 5.313082867039701
<150 mean: 56.42051691979749
<150: 94.68869348965272
150<=x<1001:4.261479705124789
150<=x<1001 mean: 375.16298457690704


The objective of variable selection is three-fold: improving the prediction performance of the predictors, providing faster and more cost-effective predictors, and providing a better understanding of
the underlying process that generated the data.