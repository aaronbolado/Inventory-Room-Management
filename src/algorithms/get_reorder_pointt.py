def get_reorder_point(demand, lead_time, last_restock):
    avg_demand = demand / last_restock
    return (avg_demand * lead_time) + (avg_demand/2)