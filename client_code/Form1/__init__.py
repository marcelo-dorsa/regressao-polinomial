from ._anvil_designer import Form1Template
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Form1(Form1Template):

  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    #self.x_inputs = []
    #self.y_inputs = []

   

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    x = self.x_inputs.text
    y = self.y_inputs.text
    m = self.m_inputs.text
    x_test = [float(number.replace(" ", "")) for number in x.split(',')]
    y_test = [float(number.replace(" ", "")) for number in y.split(',')]
    if len(x_test) == len(y_test):
      fig1 = anvil.server.call('plot', x, y, m)
      self.plot_1.data = fig1
    else:
      alert(f"Vetor x e y possuem tamanhos diferentes.")
      
    #fig1 = anvil.server.call('plot', x, y, m)
    #self.image_1.source = fig1
    #self.plot_1.data = fig1
    #x_test = len(x.replace(" ", ""))
    
    #y_test = len(y.replace(" ", ""))

  

    





