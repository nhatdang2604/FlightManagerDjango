from django.views import View
from io import BytesIO

import matplotlib.pyplot as plt
import base64

class GraphPlotting:
    '''Supports graph plotting
    '''

    def __init__(self, x, y, title):
        self.x = x
        self.y = y
        self.title = title

    def get_graph(self):
        buffer = BytesIO()
        plt.savefig(buffer, format = 'png')
        
        buffer.seek(0)
        image_png = buffer.getvalue()
        
        self.graph = base64.b64encode(image_png)
        self.graph = self.graph.decode('utf-8')

        buffer.close()
    
    def get_bar_plot(self, x_label : str, y_label : str):
        plt.switch_backend('AGG')

        plt.figure(figsize = (10, 5))
        plt.title(self.title)
        
        x_int = [i for i in range(len(self.x))]

        plt.bar(x_int, self.y)
        plt.xticks(x_int, self.x)
        plt.xlabel(x_label)
        plt.ylabel(y_label)

        self.get_graph()
        return self.graph

class PaginatedFilterView(View):
    '''A custom Filter View supports Pagination,
    which just parse the querystring back to context.

    This querystring will be parsed to paginator for later results.
    '''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.GET:
            querystring = self.request.GET.copy()
            if self.request.GET.get('page'):
                del querystring['page']
            
            context['querystring'] = querystring.urlencode()
        
        return context