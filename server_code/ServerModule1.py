import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.media
import io
import numpy as np
import matplotlib.pyplot as plt 
import anvil.mpl_util
import plotly.graph_objects as go

#import plotly.graph_objects as go

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#
@anvil.server.callable
#def apply_rp(x, y, m): #alternativo
#  x, y, m = trata_input(x, y, m)
# A = np.vander(x, m + 1)
#  z, *_ = np.linalg.lstsq(A, y, rcond=None)
#  z = z.ravel()
#  return z, x, y, m
def apply_rp(x, y, m):
  x, y, m = trata_input(x, y, m)
  A = np.zeros((m + 1, m + 1))
  b = np.zeros((m+1, 1))
  for i in range(m+1):
     for j in range(m+1):
          A[i, j] = sum(x**(i+j))
     b[i] = sum(x**(i)*y)
  z = np.dot(np.linalg.inv(A), b) #retorna uma array com os coeficientes de x em 2 dimensões
  z = z.ravel() #transforma essa antiga array em uma array unidimensional
  
  return z, x, y, m
@anvil.server.callable
def trata_input(x, y, m):
  #x = x.split(',')
  #y = y.split(',')
  #print(f"x value: {x}; y value: {y}")
  x = [float(number.replace(" ", "")) for number in x.split(',')]
  y = [float(number.replace(" ", "")) for number in y.split(',')]
  x = np.array(x)
  y = np.array(y)
  m = int(m)
  
  
  return x, y, m
@anvil.server.callable
def format_coefs(coefs):
    equation_list = [f"{coef}x^{i}" for i, coef in enumerate(coefs)]
    equation = "$" +  " + ".join(equation_list) + "$"

    replace_map = {"x^0": "", "x^1": "x", '+ -': '- '}
    for old, new in replace_map.items():
        equation = equation.replace(old, new)

    return equation

@anvil.server.callable
def plot(x, y, m):
  z, x, y, m = apply_rp(x, y, m)
  xp = np.linspace(x[0], x[-1], 200) #usamos isso para deixar o grafico "smooth"
  zflip = np.flip(z) #precisamos dar esse "flip" na função, para que o np.poly1d funcione na ordem correta.
  zp = np.poly1d(zflip) #poly1d pega os coeficientes de x e transforma em uma função polinomial
  equation = format_coefs(z.round(5))
  fig = plt.show()
  fig = go.Figure()
  fig.add_scatter(x=x, y=y, mode = "markers", name = "dados")
  fig.add_scatter(x=xp,y=zp(xp), name = f"y={equation}")
  #fig.add_scatter(x=xp,y=np.poly1d(np.flip(z(xp))), name = f"y={equationerrada}")
  
  return fig.data

  
  