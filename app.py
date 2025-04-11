from flask import Flask, request, render_template
import heapq

app = Flask(__name__, template_folder='templates')

def dijkstra_with_paths(graph, start):
    """
    Implementación del algoritmo de Dijkstra para calcular
    las distancias y los caminos más óptimos desde el nodo inicial.
    """
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    prev = {node: None for node in graph}
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                prev[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))
    
    paths = {}
    for node in graph:
        paths[node] = reconstruct_path(prev, start, node)
    return distances, paths

def reconstruct_path(prev, start, end):
    """
    Reconstruye el camino óptimo desde el nodo inicial hacia un nodo destino.
    """
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = prev[current]
    path.reverse()
    if path and path[0] == start:
        return path
    return []  # Retorna un camino vacío si no hay ruta hacia el nodo destino.

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/dijkstra', methods=['POST'])
def dijkstra_route():
    try:
        data = request.get_json()
        nodes = data.get("nodes")
        edges = data.get("edges")
        start_node = data.get("start_node")
        
        if not all(['source' in edge and 'target' in edge and 'weight' in edge for edge in edges]):
            return "Formato de aristas incorrecto.", 400

        graph = {str(i): {} for i in range(1, nodes + 1)}
        for edge in edges:
            src = edge['source']
            dest = edge['target']
            weight = edge['weight']
            graph[src][dest] = weight

        distances, paths = dijkstra_with_paths(graph, start_node)

        result_table = "<h3>Distancias</h3><ul>"
        for node, distance in distances.items():
            result_table += f"<li>Distancia al nodo {node}: {distance}</li>"
        result_table += "</ul><h3>Caminos</h3><ul>"
        for node, path in paths.items():
            result_table += f"<li>Camino al nodo {node}: {' → '.join(path)}</li>"
        result_table += "</ul>"

        return result_table
    except Exception as e:
        return f"Error: {str(e)}", 400

if __name__ == "__main__":
    app.run(debug=True, port=5001)
