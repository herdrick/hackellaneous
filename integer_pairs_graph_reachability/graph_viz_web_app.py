import web
render = web.template.render('templates/',globals={'str':str})

import graph_explore

urls = (
    '/', 'default',
    '/graph_viz', 'graph_viz',
)
app=web.application(urls, globals())


class default:
    def GET(self):
        raise web.seeother('/graph_viz')

class graph_viz:        
    def GET(self):
        i=web.input(max_sum_of_digits=19,x_from=-100,y_from=-100,x_to=100,y_to=100)
        if int(i.max_sum_of_digits) > 25:
            raise web.seeother('/graph_viz?max_sum_of_digits=10&x_from=i.x_from&x_to=i.x_to&y_from=i.y_from&y_to=i.y_to')
        print 'graph_explore.init()'
        graph_explore.init()
        print 'graph_explore.challenge()'        
        graph_explore.challenge(int(i.max_sum_of_digits))
        print 'rendering html'
        return render.graph_viz(node_set=graph_explore.explored,max_sum_of_digits=int(i.max_sum_of_digits),x_from=int(i.x_from),y_from=int(i.y_from),x_to=int(i.x_to),y_to=int(i.y_to))

if __name__ == "__main__":
    web.config.debug=True
    app.run()
