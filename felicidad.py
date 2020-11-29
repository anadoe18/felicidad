#ANALISIS DE LA BASE DE DATOS 2015 Y 2016

# importamos la librería de Pandas
import pandas as pd

# leemos cada uno de los ficheros utilizando pd.read_csv()
df_2015 = pd.read_csv('/content/2015.csv')
df_2016 = pd.read_csv('/content/2016.csv')

# para cada uno de los datasets, creamos una columna que se llame 'year' con el año que representa.
df_2015['year'] = 2015
df_2016['year'] = 2016

# concatenamos los 2 datasets en uno solo
df = pd.concat([df_2015,df_2016])

print(df.shape)

# OBTENEMOS ESTADISTICAS BASICAS
df.info()
df.shape

import plotly.express as px
import seaborn as sns

# representamos un histograma con la distribución de la variable:
fig = px.histogram(df, x="Family",
                   marginal="box",
                   hover_data=df.columns,
                   title='GRADO DE FELICIDAD QUE APORTA LA FAMILIA')
fig.show()

df.Family.describe()

#En este gráfico se analiza si la libertad de un país contribuye a la felicidad del mismo.
#La variable tiene un valor máximo de 0.66 y un mínimo de 0. La media es 0.4.
#Podemos ver en la distribucion y en el boxplot que los valores que se encuentran entre el primer cuartil 
# y el tercero,es decir, entre el 25% y el 75% , son 0.3 y 0.52. 
# Esto es, que el valor de la libertad no tiene tanto peso a la hora de determinar la felicidad de un país.

## DISTRIBUCION DEL SCORE DE FELICIDAD
df['Happiness Score'].describe()

# representamos un histograma con la distribución de la variable:
fig = px.histogram(df, x="Happiness Score",
                   hover_data=df.columns,
                   title='GRADO DE FELICIDAD EN EL MUNDO')
fig.show()

#score medio de felicidad para cada región
happiness_per_region = df.groupby('Region', as_index= False).mean()
happiness_per_region.loc[:,['Region','Happiness Score']]

fig3 = px.bar(x = happiness_per_region['Region'],
              y = happiness_per_region['Happiness Score'])
fig3.show()

# gráfica como ha variado para 2015 y 2016 el índice de felicidad para cada una de las regiones
df.groupby(['Region','year']).mean()['Happiness Score'].plot.bar()

#top5 de los paises más felices y los más infelices en 2016
df = df.sort_values(by='Happiness Score', ascending = False)
df.loc[df['year']==2016,['Happiness Score','Country']].head(5)

df = df.sort_values(by='Happiness Score')
df.loc[df['year']==2016,['Happiness Score','Country']].head(5)

#distribución de este score por región
import plotly.graph_objs as go
from plotly.offline import iplot

data = dict(type = 'choropleth', 
           locations = df['Country'],
           locationmode = 'country names',
           z = df['Happiness Rank'], 
           text = df['Country'],
           colorbar = {'title':'Happiness Rank'})
layout = dict(title = 'Global Happiness Rank', 
             geo = dict(showframe = False, 
                       projection = {'type': 'mercator'}))
choromap3 = go.Figure(data = [data], layout=layout)
iplot(choromap3)

#distribucion de índice de libertad por region
import plotly.graph_objs as go
from plotly.offline import iplot

data = dict(type = 'choropleth', 
           locations = df['Country'],
           locationmode = 'country names',
           z = df['Freedom'], 
           text = df['Country'],
           colorbar = {'title':'Freedom'})
layout = dict(title = 'Global Freedom', 
             geo = dict(showframe = False, 
                       projection = {'type': 'mercator'}))
choromap3 = go.Figure(data = [data], layout=layout)
iplot(choromap3)

#CORRELACION ENTRE VARIABLES
col_corr = ['Happiness Score', 'Economy (GDP per Capita)', 'Family',
       'Health (Life Expectancy)', 'Freedom', 'Trust (Government Corruption)',
       'Generosity']

df[col_corr].corr()

#Las variables que están más correlacionadas con Happiness Score son la economía y y la salud. 
#Esto tiene sentido ya que la salud y tener recursos para vivir hacen que tu calidad de vida sea mejor

#CREAMOS 3 VISUALIZACIONES ENTRE SCORE DE FELICIDAD Y LAS VARIABLES QUE MEJOR CORRELAN CON ELLA
import matplotlib.pyplot as plt
x = df['Economy (GDP per Capita)']
y= df['Happiness Score']
plt.scatter(x,y)
plt.title('CORRELACIÓN ECONOMÍA-FELICIDAD')
plt.xlabel('GDP per capita')
plt.ylabel('Happiness Score')


a = df['Health (Life Expectancy)']
b = df['Happiness Score']
plt.scatter(a,b)
plt.title('CORRELACIÓN SALUD-FELICIDAD')
plt.xlabel('Salud (Life Expectancy)')
plt.ylabel('Happiness Score')


c = df['Family']
d = df['Happiness Score']
plt.scatter(c,d)
plt.title('FCORRELACIÓN FAMILIA-FELICIDAD')
plt.xlabel('Familia')
plt.ylabel('Happiness Score')

## EXPLICACION
#Ambas variables tienen una fuerte correlacion positiva, 
# es decir que si en un país hay buena salud, buena economía y familias la gente es más feliz.


#CORRELACIÓN ECONOMÍA-FELICIDAD
#Es correlación positiva y muy fuerte (0.78).

#Esto quiere decir que el grado de felicidad de un país está muy correlacionado con el nivel económico del país.

#También podemos ver que los puntos que correlan estas dos variables están un poco más elevados de la linea x=y, 
# es decir, que la felicidad es un poco mayor al nivel económico del país.

#CORRELACIÓN SALUD-FELICIDAD
#Es correlación positiva y muy fuerte (0.73).

#Esto quiere decir que el grado de felicidad de un país está muy correlacionado con la salud.

#También podemos ver que los puntos que correlan estas dos variables están practicamente al nivel de la linea x=y,
#  es decir, que la salud está al mismo nivel que el grado de felicidad de un país.

#CORRELACIÓN FAMILIA-FELICIDAD
#Es correlación positiva y muy fuerte (0.69).

#Esto quiere decir que el grado de felicidad de un país está muy correlacionado con la familia.

#También podemos ver que los puntos que correlan estas dos variables están un poco por debajo de la linea x=y, 
# es decir, la felicidad está un poco por debajo de los niveles de la familia



#CREAMOS VISUALIZACION ENTRE SOCRE FELICIDAD Y EL INDICE DE CORRUPCION TRAMIFICADO
df.loc[:, 'Trust (Government Corruption)'].describe()

#Creamos tramos
df['Corrupción_tr'] = 'Desconocido'
df.loc[df['Trust (Government Corruption)']<=0.061315,'Corrupción_tr']='bad'
df.loc[(df['Trust (Government Corruption)']>0.061315)&(df['Trust (Government Corruption)']<=0.178610),'Corrupción_tr']='medium'
df.loc[df['Trust (Government Corruption)']>0.178610,'Corrupción_tr']='good'


# para generar esta gráfica, hemos usado pivot_table:
df2 = df.loc[:, ['Corrupción_tr', 'Happiness Score','Country', 'year']].pivot_table(index=['Country','year'], columns='Corrupción_tr', values='Happiness Score')
df2.loc[:, ['bad', 'medium', 'good']].plot.box()

df2.loc[:, ['bad', 'medium', 'good']].describe()

#En el boxplot estamos viendo cómo afecta el nivel de corrupción de un país a su 'Happiness Score'.

#En este grafico podemos ver algo que no esperabamos, y es que los paises con más corrupción (bad) 
# tienen una media de 'Happiness Score' mayor que la media de de los paises con corrupcion media. Sin embargo, 
# los paises sin corrupción tienen una 'Happiness Score' muy por encima que los otros dos grupos.

#Por otro lado, aunque el grupo BAD tenga una media mayor de felidicad que el grupo MEDIUM, 
# podemos ver que el valor máximo alcanzado en MEDIUM es mucho mayor al valor máximo de felicidad alcanzado en el grupo BAD.

#Otro indicador del boxplot es el grado de dispersión. En el grupo BAD, 
# las notas de felicidad están mucho más concentradas que en el grupo MEDIUM. De hecho, la diferencia de 'Happiness Score' 
# intercuartilica (del 25% al 75%) son:

#en BAD una diferencia de 1,12 puntos
#en MEDIUM una diferencia de 1,67 puntos
#en GOOD una diferencia de 1,65 puntos
#Por último, otro de los aspectos que nos muestra boxplot, es que el en grupo GOOD hay un outlier, 
# con un 'Happiness Socre' cerca de 3


#MODELO DE PREDICCION DE FELICIDAD

# generamos esta función para calcular las veces que el modelo esta en lo correcto:
def accuracy_score(truth, pred):
    """ Devuelve accuracy score comparando valores predichos (pred) contra reales (truth). """
    
    # Ensure that the number of predictions matches number of outcomes
    if len(truth) == len(pred): 
        
        # Calculate and return the accuracy as a percent
        return "Predicciones tienen un accuracy de {:.2f}%.".format((truth == pred).mean()*100)
    
    else:
        return "El número de predicciones no es igual al numero de valores reales!"


#Genero un dataset para entrenar el modelo.

#Entre las cosas que hago, Happiness Score_y/n genero esta columna binaria donde establezco el criterio:

#1 si Happiness Score > Happiness Score_y/n.mean()
#0 si Happiness Score <= Happiness Score_y/n.mean()
#Respecto a las features del modelo, las reduzco a las que se incluyen en col_corr a excepción de 'Happiness Score', 
# que la excluyo pues la target del modelo la he construido a partir de ella.

# creación del dataset:
data2 = df.copy()
data2['Happiness Score_y/n'] = data2['Happiness Score'].apply(lambda x: 1 if x > data2['Happiness Score'].mean() else 0)
outcomes = data2['Happiness Score_y/n']
data2 = data2.loc[:, [x for x in col_corr if x not in ['Happiness Score', 'Happiness Score_y/n']]]

outcomes.head()



