def format_clients(clients):
    return [{
        "id": c.id,
        "client_name": c.client_name,
        "project_name": c.project_name,
        "start_date": c.start_date.isoformat()
    } for c in clients]
