import web
render = web.template.render('templates/')

import graph_explore

urls = (
    '/graph_viz', 'graph_viz',

)
app=web.application(urls, globals())

class graph_viz:        
    def GET(self):
        i=web.input(max_sum_of_digits=19,x_from=-200,y_from=-200,x_to=200,y_to=200)
        print 'graph_explore.init()'
        graph_explore.init()
        print 'graph_explore.challenge()'        
        graph_explore.challenge(int(i.max_sum_of_digits))
        print 'rendering html'
        return render.graph_viz(node_set=graph_explore.explored,x_from=int(i.x_from),y_from=int(i.y_from),x_to=int(i.x_to),y_to=int(i.y_to))

if __name__ == "__main__":
    web.config.debug=True
    app.run()
