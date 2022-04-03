class MoviePerformanceAnalytics:
    def __init__(self,shows,total_tickets,tickets_sold,housefull_shows,revenue):
        self.shows=shows
        self.total_tickets=total_tickets
        self.tickets_sold=tickets_sold
        self.housefull_shows=housefull_shows
        self.revenue=revenue

    def to_json(self):
        if(self.total_tickets==0):
            self.total_tickets=1
        occupancy=(self.tickets_sold/self.total_tickets)*100
        return{'shows':self.shows,'total_tickets':self.total_tickets,'tickets_sold':self.tickets_sold,'occupancy':occupancy,'housefull_shows':self.housefull_shows,'revenue':self.revenue}

