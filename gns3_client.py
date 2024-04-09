import pprint
import requests

class GNS3Client:
    def __init__(self, hostname, port=3080, use_tls=False):
        self.hostname = hostname
        self.port = port
        self.use_tls = use_tls
        self.base_url = f"https://{hostname}:{port}/v2" if use_tls==True else f"http://{hostname}:{port}/v2"

        # Add all projects to self.projects at instantiation         
        self.projects = {}
        for project in self.to_project(self.get_projects()):
            self.add_project(project)

    def _api_call(self, method, endpoint, **kwargs):
        url = f"{self.base_url}/{endpoint}"
        response = requests.request(method, url, **kwargs)
        
        debug = 1
        
        if debug == 0:
            return response.json()
        elif debug == 1:
            try:
                return response.json()
            except requests.exceptions.JSONDecodeError as e:
                print(f"{response.text}, {type(response.text)}")
                print(e)
                return f"{response.text}, {type(response.text)}"
    
    def to_project(self, x):
        """Constructs a Project or a list of Projects from the JSON response of the HTTP API."""
        if type(x) == list:
            projects = []

            for p in x:
                new_project = Project(self._api_call, **p)
                projects.append(new_project)
            return projects
       
        elif type(x) == dict:
            return Project(self, **x)
        
    def add_project(self, project):
        """Adds a Project to the self.projects dict attribute."""
        self.projects[project.name] = project
            
    def create_project(self, name):
        return self._api_call("POST", "projects", json={"name": name})
    
    def delete_project(self, project_id):
        return self._api_call("DELETE", f"projects/{project_id}")

    def get_project(self, project_id):
        return self._api_call("GET", f"projects/{project_id}")

    def get_projects(self):
        return self._api_call("GET", "projects")
    
    def get_computes(self):
        return self._api_call("GET", f"computes")

    def get_version(self):
        return self._api_call("GET", f"version")

    def get_template(self, template_id):
        return self._api_call("GET", f"templates/{template_id}")

    def get_templates(self):
        return self._api_call("GET", "templates")

class Project:
    def __init__(self, api_call, auto_close, auto_open, auto_start, drawing_grid_size, filename, grid_size, name, path, project_id, 
                 scene_height, scene_width, show_grid, show_interface_labels, show_layers, snap_to_grid, status, supplier, variables, zoom):
        self._api_call = api_call

        self.auto_close = auto_close
        self.auto_open = auto_open
        self.auto_start = auto_start
        self.drawing_grid_size = drawing_grid_size
        self.filename = filename
        self.grid_size = grid_size
        self.name = name
        self.path = path
        self.project_id = project_id
        self.scene_height = scene_height
        self.scene_width = scene_width
        self.show_grid = show_grid
        self.show_interface_labels = show_interface_labels
        self.show_layers = show_layers
        self.snap_to_grid = snap_to_grid
        self.status = status
        self.supplier = supplier
        self.variables = variables
        self.zoom = zoom

        # Add all nodes to self.nodes at instantiation     
        self.nodes = {}
        nodes = self.to_node(self.get_nodes())
        for node in nodes:
            self.add_node(node)

    def __repr__(self):
        return f"Project('{self.auto_close}', '{self.auto_open}', '{self.auto_start}', {self.drawing_grid_size}, '{self.filename}', {self.grid_size}, '{self.name}', '{self.path}', '{self.project_id}', {self.scene_height}, {self.scene_width}, '{self.show_grid}', '{self.show_interface_labels}', '{self.show_layers}', '{self.snap_to_grid}', '{self.status}', '{self.supplier}', '{self.variables}', {self.zoom})"
    
    def __str__(self):
        return f"{self.name}"
    
    def to_node(self, x):
        """Contructs a Node or a list of Node from the JSON response of the HTTP API."""
        if type(x) == list:
            nodes = []
            for n in x:
                new_node = Node(self._api_call, **n)
                nodes.append(new_node)
            return nodes

        elif type(x) == dict:
            return Node(self, **n)

    def add_node(self, node):
        self.nodes[node.name] = node

    def open(self):
        """Open this project"""
        return self._api_call("POST", f"projects/{self.project_id}/open")

    def close(self):
        """Close this project"""
        return self._api_call("POST", f"projects/{self.project_id}/close")

    def start_nodes(self, project_id):
        """Start all nodes in a project."""
        return self._api_call("POST", f"projects/{project_id}/start")
    
    def stop_nodes(self, project_id):
        """Stop all nodes in a project."""
        return self._api_call("POST", f"projects/{project_id}/stop")
    
    def get_links(self, project_id):
        return self._api_call("GET", f"projects/{project_id}/links")
    
    def create_node(self, project_id, node_name, node_type, template_id, compute_id="local"):
        return self._api_call("POST", f"projects/{project_id}/nodes", json={"name": f"{node_name}", "node_type": f"{node_type}", "template_id": f"{template_id}", "compute_id": f"{compute_id}"})
    
    def create_template_node(self, project_id, template_id, x, y):
        return self._api_call("POST", f"projects/{project_id}/templates/{template_id}", json={"x": x, "y": y})
    
    def delete_node(self, project_id, node_id):
        return self._api_call("DELETE", f"projects/{project_id}/nodes/{node_id}")

    def get_node(self, node_id):
        return self._api_call("GET", f"projects/{self.project_id}/nodes/{node_id}")
    
    def get_nodes(self):
        x = self._api_call("GET", f"projects/{self.project_id}/nodes")
        pprint.pprint(x[0])
        return x

class Node:
    def __init__(self, api_call, command_line, compute_id, console, console_auto_start, console_host, console_type, custom_adapters, first_port_name, height, label, locked, name, node_directory,
                node_id, node_type, port_name_format, port_segment_size, ports, project_id, properties, status, symbol, template_id, width, x, y, z):
        self._api_call = api_call
        self.command_line = command_line
        self.compute_id = compute_id
        self.console = console
        self.console_auto_start	= console_auto_start
        self.console_host = console_host
        self.console_type = console_type
        self.custom_adapters = custom_adapters	
        self.first_port_name = first_port_name
        self.height = height
        self.label = label
        self.locked = locked
        self.name = name
        self.node_directory = node_directory
        self.node_id = node_id
        self.node_type = node_type
        self.port_name_format = port_name_format
        self.port_segment_size	= port_segment_size	
        self.ports = ports
        self.project_id = project_id
        self.properties = properties
        self.status = status
        self.symbol = symbol
        self.template_id = template_id
        self.width = width
        self.x = x
        self.y = y
        self.z = z
        
        self.links = {}

    def __str__(self):
        return f"{self.name}"

    def start_node(self, project_id, node_id):
        """Start the specified node."""
        return self._api_call("POST", f"projects/{project_id}/{node_id}/start")
    
    def stop_node(self, project_id, node_id):
        """Stop the specified node."""
        return self._api_call("POST", f"projects/{project_id}/{node_id}/stop")
    
    def create_link(self, project_id, node1_id, node1_adapter, node1_port, node2_id, node2_adapter, node2_port):
        return self._api_call("POST", f"projects/{project_id}/links", json={
            "nodes": [
                {
                    "adapter_number": node1_adapter,
                    "node_id": f"{node1_id}",
                    "port_number": node1_port
                },
                {
                    "adapter_number": node2_adapter,
                    "node_id": f"{node2_id}",
                    "port_number": node2_port
                }
            ]
        })

class Link:
    def __init__(self, api_call, capture_compute_id, capture_file_name, capture_file_path, capturing, filters, link_id, link_style, link_type, nodes, project_id, suspend):
        self._api_call = api_call

        self.capture_compute_id = capture_compute_id
        self.capture_file_name = capture_file_name
        self.capture_file_path = capture_file_path
        self.capturing = capturing
        self.filters = filters
        self.link_id = link_id
        self.link_style = link_style
        self.link_type = link_type
        self.nodes = nodes
        self.project_id = project_id
        self.suspend = suspend