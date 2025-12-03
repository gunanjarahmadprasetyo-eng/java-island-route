import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import folium
from streamlit_folium import st_folium
import random
from math import radians, sin, cos, sqrt, atan2
import pandas as pd

# =========================
# CONFIGURATION
# =========================
st.set_page_config(
    page_title="Graph Matrix Pro",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# CUSTOM CSS - PROFESSIONAL DESIGN
# =========================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800&family=Poppins:wght@300;400;500;600&display=swap');
    
    /* Main Background */
    .stApp {
        background-color: #FAF3E1;
        color: #222222;
        font-family: 'Poppins', sans-serif;
    }
    
    /* Headers with Montserrat */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 700 !important;
        color: #222222 !important;
    }
    
    .main-title {
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 800 !important;
        font-size: 3rem !important;
        color: #222222 !important;
        text-align: center;
        margin-bottom: 0.5rem !important;
    }
    
    .section-title {
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 700 !important;
        font-size: 2rem !important;
        color: #222222 !important;
        border-bottom: 3px solid #FF6D1F;
        padding-bottom: 0.5rem;
        margin-bottom: 1.5rem !important;
    }
    
    /* Sidebar Styling */
    .css-1d391kg, .css-1lcbmhc {
        background-color: #F5E7C6 !important;
    }
    
    /* Professional Header */
    .main-header {
        background: linear-gradient(135deg, #FF6D1F, #FF8C42);
        padding: 40px;
        border-radius: 20px;
        margin-bottom: 30px;
        text-align: center;
        color: white;
        box-shadow: 0 8px 25px rgba(255, 109, 31, 0.3);
    }
    
    /* Feature Cards */
    .feature-card {
        background: white;
        padding: 25px;
        border-radius: 15px;
        margin: 15px 0;
        border-left: 5px solid #FF6D1F;
        box-shadow: 0 6px 15px rgba(0,0,0,0.1);
        border: 1px solid #F5E7C6;
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
    }
    
    /* Profile Cards */
    .profile-card {
        background: white;
        padding: 25px;
        border-radius: 15px;
        margin: 15px 0;
        box-shadow: 0 6px 15px rgba(0,0,0,0.1);
        border: 1px solid #F5E7C6;
        text-align: center;
    }
    
    /* Metrics Cards */
    .metric-card {
        background: white;
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        border: 1px solid #F5E7C6;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    /* Graph Container */
    .graph-container {
        background: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 6px 15px rgba(0,0,0,0.1);
        border: 1px solid #F5E7C6;
    }
    
    /* Matrix Container */
    .matrix-container {
        background: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 6px 15px rgba(0,0,0,0.1);
        border: 1px solid #F5E7C6;
    }
    
    /* Map Container */
    .map-container {
        background: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 6px 15px rgba(0,0,0,0.1);
        border: 1px solid #F5E7C6;
    }
    
    /* Route Option Cards */
    .route-option {
        background: white;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        border: 2px solid #F5E7C6;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .route-option:hover {
        border-color: #FF6D1F;
        transform: translateY(-2px);
    }
    
    .route-option.selected {
        border-color: #FF6D1F;
        background: #FFF5EB;
    }
    
    .route-option.recommended {
        border-color: #FF6D1F;
        background: #FFF5EB;
        position: relative;
    }
    
    .route-option.recommended::before {
        content: "⭐ RECOMMENDED";
        position: absolute;
        top: -10px;
        right: 10px;
        background: #FF6D1F;
        color: white;
        padding: 2px 8px;
        border-radius: 10px;
        font-size: 10px;
        font-weight: bold;
    }
    
    /* Button Styling */
    .stButton>button {
        background: linear-gradient(135deg, #FF6D1F, #FF8C42);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 14px 28px;
        font-weight: 600;
        font-family: 'Montserrat', sans-serif;
        transition: all 0.3s ease;
        width: 100%;
        font-size: 1rem;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(255, 109, 31, 0.4);
        background: linear-gradient(135deg, #E55C1A, #FF6D1F);
    }
    
    /* Input Styling */
    .stSelectbox>div>div, .stTextInput>div>div>input, 
    .stNumberInput>div>div>input, .stMultiSelect>div>div {
        background: white;
        border: 2px solid #F5E7C6;
        color: #222222;
        border-radius: 8px;
        font-family: 'Poppins', sans-serif;
    }
    
    /* Sidebar Navigation */
    .sidebar-nav {
        padding: 20px 0;
    }
    
    .nav-item {
        padding: 15px 20px;
        margin: 10px 0;
        border-radius: 10px;
        cursor: pointer;
        transition: all 0.3s ease;
        border-left: 4px solid transparent;
        background: white;
        font-family: 'Montserrat', sans-serif;
        font-weight: 600;
    }
    
    .nav-item:hover {
        background: #FF6D1F;
        color: white;
        border-left: 4px solid #222222;
        transform: translateX(5px);
    }
    
    .nav-item.active {
        background: #FF6D1F;
        color: white;
        border-left: 4px solid #222222;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# SESSION STATE INITIALIZATION
# =========================
if 'graph' not in st.session_state:
    st.session_state.graph = nx.Graph()
if 'node_positions' not in st.session_state:
    st.session_state.node_positions = {}
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Home"
if 'selected_route' not in st.session_state:
    st.session_state.selected_route = None
if 'available_routes' not in st.session_state:
    st.session_state.available_routes = None

# =========================
# GRAPH FUNCTIONS
# =========================
def create_random_graph(num_nodes, num_edges):
    """Create a random graph with specified nodes and edges"""
    G = nx.Graph()
    nodes = list(range(1, num_nodes + 1))
    G.add_nodes_from(nodes)
    
    all_possible_edges = [(i, j) for i in range(1, num_nodes + 1) for j in range(i + 1, num_nodes + 1)]
    
    if num_edges > len(all_possible_edges):
        num_edges = len(all_possible_edges)
    
    selected_edges = random.sample(all_possible_edges, num_edges)
    
    # Add weights to edges
    for edge in selected_edges:
        weight = random.randint(1, 20)
        G.add_edge(edge[0], edge[1], weight=weight)
    
    # Generate circular positions
    positions = {}
    center_x, center_y = 5, 5
    radius = 4
    
    for i, node in enumerate(nodes):
        angle = 2 * np.pi * i / len(nodes)
        x = center_x + radius * np.cos(angle)
        y = center_y + radius * np.sin(angle)
        positions[node] = (x, y)
    
    return G, positions

def calculate_degree(G):
    """Calculate degree of each node"""
    return dict(G.degree())

def get_adjacency_matrix(G):
    """Get adjacency matrix as numpy array"""
    if len(G.nodes()) == 0:
        return np.array([])
    
    nodes = sorted(G.nodes())
    adj_matrix = np.zeros((len(nodes), len(nodes)))
    
    for i, u in enumerate(nodes):
        for j, v in enumerate(nodes):
            if G.has_edge(u, v):
                adj_matrix[i, j] = G[u][v].get('weight', 1)
    
    return adj_matrix

def visualize_graph(G, positions):
    """Visualize graph using matplotlib with high contrast colors"""
    fig, ax = plt.subplots(figsize=(10, 8))
    
    if len(G.nodes()) == 0:
        ax.text(0.5, 0.5, 'No graph to display', 
                horizontalalignment='center', verticalalignment='center',
                transform=ax.transAxes, fontsize=16, color='#222222', fontweight='bold')
        ax.set_facecolor('#FAF3E1')
        fig.patch.set_facecolor('#FAF3E1')
        return fig
    
    # High contrast colors
    node_colors = ['#FF6D1F' for _ in G.nodes()]
    edge_colors = ['#222222' for _ in G.edges()]
    
    # Draw nodes and edges
    nx.draw_networkx_nodes(G, positions, ax=ax, 
                          node_color=node_colors, node_size=1000,
                          edgecolors='#222222', linewidths=2)
    
    nx.draw_networkx_edges(G, positions, ax=ax,
                          edge_color=edge_colors, width=2.5, alpha=0.8)
    
    # Draw labels
    nx.draw_networkx_labels(G, positions, ax=ax, 
                           font_size=14, font_weight='bold', font_color='white',
                           font_family='Montserrat')
    
    # Draw edge labels (weights)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    if edge_labels:
        nx.draw_networkx_edge_labels(G, positions, edge_labels=edge_labels, 
                                   ax=ax, font_size=11, font_color='#222222',
                                   font_family='Montserrat')
    
    ax.set_facecolor('#FAF3E1')
    fig.patch.set_facecolor('#FAF3E1')
    ax.set_title("Graph Visualization", fontsize=20, pad=20, color='#222222', 
                fontweight='bold', fontfamily='Montserrat')
    ax.grid(True, alpha=0.3, color='#F5E7C6')
    ax.axis('on')
    
    return fig

# =========================
# COMPREHENSIVE JAVA CITIES DATABASE
# =========================
java_cities = {
    # Jakarta and Surroundings
    "Jakarta": [-6.2088, 106.8456],
    "Bogor": [-6.5971, 106.8060],
    "Depok": [-6.4025, 106.7942],
    "Tangerang": [-6.1783, 106.6319],
    "Bekasi": [-6.2383, 106.9756],
    
    # West Java
    "Bandung": [-6.9175, 107.6191],
    "Cimahi": [-6.8722, 107.5425],
    "Cirebon": [-6.7320, 108.5523],
    "Tasikmalaya": [-7.3274, 108.2207],
    "Sukabumi": [-6.9277, 106.9300],
    "Garut": [-7.2279, 107.9087],
    "Sumedang": [-6.8586, 107.9194],
    "Majalengka": [-6.8364, 108.2279],
    "Kuningan": [-6.9759, 108.4839],
    "Ciamis": [-7.3331, 108.3494],
    "Banjar": [-7.3708, 108.5346],
    "Purwakarta": [-6.5550, 107.4430],
    "Subang": [-6.5700, 107.7630],
    "Indramayu": [-6.3373, 108.3258],
    "Karawang": [-6.3227, 107.3376],
    
    # Central Java
    "Semarang": [-6.9667, 110.4167],
    "Surakarta (Solo)": [-7.5755, 110.8243],
    "Magelang": [-7.4706, 110.2177],
    "Salatiga": [-7.3307, 110.4922],
    "Pekalongan": [-6.8895, 109.6750],
    "Tegal": [-6.8694, 109.1400],
    "Cilacap": [-7.7255, 109.0244],
    "Purwokerto": [-7.4314, 109.2479],
    "Klaten": [-7.7050, 110.6060],
    "Demak": [-6.8903, 110.6392],
    "Kudus": [-6.8048, 110.8405],
    "Jepara": [-6.5944, 110.6711],
    "Pati": [-6.7550, 111.0380],
    "Blora": [-6.9698, 111.4185],
    "Rembang": [-6.8083, 111.6219],
    
    # Yogyakarta
    "Yogyakarta": [-7.7956, 110.3695],
    "Bantul": [-7.8833, 110.3333],
    "Sleman": [-7.7167, 110.3500],
    "Gunung Kidul": [-7.9833, 110.6167],
    "Kulon Progo": [-7.8667, 110.1500],
    
    # East Java
    "Surabaya": [-7.2575, 112.7521],
    "Malang": [-7.9666, 112.6326],
    "Kediri": [-7.8467, 112.0178],
    "Blitar": [-8.0986, 112.1683],
    "Madiun": [-7.6298, 111.5239],
    "Pasuruan": [-7.6453, 112.9075],
    "Probolinggo": [-7.7543, 113.2159],
    "Mojokerto": [-7.4664, 112.4338],
    "Jember": [-8.1845, 113.7032],
    "Banyuwangi": [-8.2191, 114.3691],
    "Lumajang": [-8.1335, 113.2242],
    "Bondowoso": [-7.9135, 113.8212],
    "Situbondo": [-7.7062, 114.0095],
    "Tulungagung": [-8.0643, 111.9023],
    "Trenggalek": [-8.0500, 111.7167],
    "Ponorogo": [-7.8667, 111.4667],
    "Pacitan": [-8.2067, 111.0933],
    "Ngawi": [-7.4044, 111.4464],
    "Magetan": [-7.6494, 111.3381],
    "Nganjuk": [-7.6050, 111.9036],
    "Bojonegoro": [-7.1500, 111.8833],
    "Tuban": [-6.8976, 112.0649],
    "Lamongan": [-7.1167, 112.4167],
    "Gresik": [-7.1556, 112.6542],
    "Sidoarjo": [-7.4481, 112.7183],
    "Jombang": [-7.5500, 112.2333]
}

# =========================
# REALISTIC ROAD NETWORK FOR JAVA
# =========================
java_highways = {
    "Jakarta": {"Bogor": 45, "Bekasi": 25, "Tangerang": 30, "Depok": 20, "Cirebon": 210},
    "Bogor": {"Jakarta": 45, "Bandung": 150, "Sukabumi": 60},
    "Bandung": {"Bogor": 150, "Cimahi": 15, "Garut": 85, "Sumedang": 45, "Cirebon": 130, "Tasikmalaya": 120},
    "Surabaya": {"Sidoarjo": 25, "Gresik": 20, "Mojokerto": 50, "Malang": 90, "Pasuruan": 65, "Probolinggo": 105},
    "Yogyakarta": {"Sleman": 10, "Bantul": 15, "Magelang": 35, "Solo": 65, "Purwokerto": 120},
    "Semarang": {"Salatiga": 45, "Demak": 25, "Kudus": 80, "Purwokerto": 180},
    "Cirebon": {"Indramayu": 40, "Kuningan": 35, "Majalengka": 50, "Brebes": 85},
    "Tasikmalaya": {"Garut": 40, "Ciamis": 30, "Banjar": 25},
    "Malang": {"Batu": 20, "Blitar": 75, "Lumajang": 90},
    "Purwokerto": {"Cilacap": 60, "Purbalingga": 25, "Banjarnegara": 40},
    "Solo": {"Sragen": 30, "Karanganyar": 15, "Wonogiri": 40, "Madiun": 100},
    "Madiun": {"Magetan": 35, "Ponorogo": 50, "Nganjuk": 45},
    "Kediri": {"Blitar": 45, "Tulungagung": 40, "Jombang": 35},
    "Probolinggo": {"Lumajang": 70, "Jember": 85, "Banyuwangi": 180},
    "Jember": {"Lumajang": 45, "Banyuwangi": 95}
}

def create_java_highway_graph():
    """Create a comprehensive highway graph for Java"""
    G = nx.Graph()
    
    # Add all cities as nodes
    for city, coord in java_cities.items():
        G.add_node(city, pos=coord)
    
    # Add highway connections
    for city, connections in java_highways.items():
        for connected_city, distance in connections.items():
            if connected_city in java_cities:
                G.add_edge(city, connected_city, weight=distance)
    
    # Add additional connections based on proximity
    cities_list = list(java_cities.keys())
    for i, city1 in enumerate(cities_list):
        for j, city2 in enumerate(cities_list):
            if i < j and not G.has_edge(city1, city2):
                distance = calculate_road_distance(java_cities[city1], java_cities[city2])
                if distance <= 100:  # Only add if cities are relatively close
                    G.add_edge(city1, city2, weight=round(distance, 1))
    
    return G

def calculate_road_distance(coord1, coord2):
    """Calculate realistic road distance between two coordinates"""
    R = 6371
    lat1, lon1 = radians(coord1[0]), radians(coord1[1])
    lat2, lon2 = radians(coord2[0]), radians(coord2[1])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    straight_distance = R * 2 * atan2(sqrt(a), sqrt(1-a))
    
    # Realistic road distance factor
    road_factor = 1.3 + (random.random() * 0.3)
    return straight_distance * road_factor

def find_all_routes(start_city, end_city, max_routes=4):
    """Find multiple possible routes between cities"""
    if start_city == end_city:
        return []
    
    G = create_java_highway_graph()
    
    try:
        # Find shortest path (recommended route)
        shortest_path = nx.shortest_path(G, start_city, end_city, weight='weight')
        shortest_distance = calculate_path_distance(G, shortest_path)
        
        routes = [{
            'path': shortest_path,
            'distance': shortest_distance,
            'type': 'shortest',
            'name': 'Shortest Route'
        }]
        
        # Find alternative routes
        try:
            G_temp = G.copy()
            for i in range(len(shortest_path) - 1):
                if G_temp.has_edge(shortest_path[i], shortest_path[i+1]):
                    G_temp.remove_edge(shortest_path[i], shortest_path[i+1])
            
            alt_path = nx.shortest_path(G_temp, start_city, end_city, weight='weight')
            alt_distance = calculate_path_distance(G_temp, alt_path)
            
            if alt_path != shortest_path and len(routes) < max_routes:
                routes.append({
                    'path': alt_path,
                    'distance': alt_distance,
                    'type': 'alternative',
                    'name': 'Alternative Route 1'
                })
        except:
            pass
        
        # Add more alternative routes
        for i in range(2, max_routes):
            try:
                G_alt = G.copy()
                # Randomly adjust some weights to get different paths
                for u, v, data in G_alt.edges(data=True):
                    if random.random() > 0.7:
                        data['weight'] *= random.uniform(0.8, 1.2)
                
                alt_path = nx.shortest_path(G_alt, start_city, end_city, weight='weight')
                alt_distance = calculate_path_distance(G, alt_path)
                
                if (alt_path != shortest_path and 
                    not any(r['path'] == alt_path for r in routes) and 
                    len(routes) < max_routes):
                    routes.append({
                        'path': alt_path,
                        'distance': alt_distance,
                        'type': 'alternative',
                        'name': f'Route Option {i}'
                    })
            except:
                pass
        
        return routes
        
    except nx.NetworkXNoPath:
        return []

def calculate_path_distance(G, path):
    """Calculate total distance for a path"""
    total_distance = 0
    for i in range(len(path) - 1):
        if G.has_edge(path[i], path[i+1]):
            total_distance += G[path[i]][path[i+1]]['weight']
    return round(total_distance, 1)

# =========================
# SIDEBAR NAVIGATION
# =========================
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 20px 0;'>
        <h1 style='color: #222222; margin-bottom: 10px; font-family: "Montserrat", sans-serif; font-weight: 800;'>🌐 GRAPH MATRIX PRO</h1>
        <p style='color: #666; font-size: 14px; font-family: "Poppins", sans-serif;'>Advanced Graph Analysis Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Navigation buttons
    nav_options = {
        "🏠 HOME": "Home",
        "📊 GRAPH VISUALIZATION": "Graph Visualization", 
        "🧮 MATRIX ANALYSIS": "Matrix Analysis",
        "🗺️ JAVA ROUTE FINDER": "Java Route Finder"
    }
    
    for nav_text, page_id in nav_options.items():
        if st.button(nav_text, key=page_id, use_container_width=True):
            st.session_state.current_page = page_id
            st.rerun()
    
    st.markdown("---")
    
    # Quick stats in sidebar
    if len(st.session_state.graph.nodes()) > 0:
        st.markdown("### 📈 CURRENT GRAPH")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Nodes", len(st.session_state.graph.nodes()))
        with col2:
            st.metric("Edges", len(st.session_state.graph.edges()))
    
    st.markdown("---")
    
    # Team information
    st.markdown("### 👥 DEVELOPMENT TEAM")
    st.markdown("""
    <div style='font-family: "Poppins", sans-serif;'>
    - **Jasmiana C. A.** (021202500026)
    - **Angel Margaretha** (021202500007)  
    - **Gunanjar A. P.** (021202500020)
    </div>
    """, unsafe_allow_html=True)

# =========================
# HOME PAGE
# =========================
if st.session_state.current_page == "Home":
    # Header Section
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    st.markdown('<h1 class="main-title">GRAPH MATRIX PRO</h1>', unsafe_allow_html=True)
    st.markdown('<h3 style="font-family: Montserrat, sans-serif; font-weight: 600; color: white; margin-bottom: 0;">Advanced Graph Theory Visualization & Analysis Platform</h3>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick Actions
    st.markdown('<h2 class="section-title">🚀 QUICK ACTIONS</h2>', unsafe_allow_html=True)
    
    quick_col1, quick_col2, quick_col3, quick_col4 = st.columns(4)
    
    with quick_col1:
        if st.button("🔄 CREATE RANDOM GRAPH", use_container_width=True):
            st.session_state.current_page = "Graph Visualization"
            st.rerun()
    
    with quick_col2:
        if st.button("📈 ANALYZE MATRIX", use_container_width=True):
            st.session_state.current_page = "Matrix Analysis"
            st.rerun()
    
    with quick_col3:
        if st.button("🗺️ PLAN ROUTE", use_container_width=True):
            st.session_state.current_page = "Java Route Finder"
            st.rerun()
    
    with quick_col4:
        if st.button("📊 VIEW METRICS", use_container_width=True):
            st.session_state.current_page = "Matrix Analysis"
            st.rerun()
    
    # Features Grid
    st.markdown('<h2 class="section-title">🎯 CORE FEATURES</h2>', unsafe_allow_html=True)
    
    features_col1, features_col2 = st.columns(2)
    
    with features_col1:
        st.markdown("""
        <div class="feature-card">
            <h3 style='color: #FF6D1F;'>📊 GRAPH VISUALIZATION</h3>
            <p style='font-family: Poppins, sans-serif;'>Create and visualize complex graphs with customizable nodes and edges. 
            Support for weighted graphs and various layout algorithms.</p>
            <ul style='font-family: Poppins, sans-serif;'>
                <li>Interactive graph creation</li>
                <li>Multiple layout options</li>
                <li>Weighted edges support</li>
                <li>Real-time visualization</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3 style='color: #FF6D1F;'>🗺️ JAVA ROUTE FINDER</h3>
            <p style='font-family: Poppins, sans-serif;'>Find optimal routes between cities in Java using advanced pathfinding algorithms. 
            Realistic road distances and interactive maps.</p>
            <ul style='font-family: Poppins, sans-serif;'>
                <li>Dijkstra's algorithm</li>
                <li>Real road networks</li>
                <li>Interactive Folium maps</li>
                <li>Distance calculations</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with features_col2:
        st.markdown("""
        <div class="feature-card">
            <h3 style='color: #FF6D1F;'>🧮 MATRIX ANALYSIS</h3>
            <p style='font-family: Poppins, sans-serif;'>Comprehensive matrix operations including adjacency matrices, 
            degree calculations, and graph theory metrics.</p>
            <ul style='font-family: Poppins, sans-serif;'>
                <li>Adjacency matrices</li>
                <li>Node degree analysis</li>
                <li>Graph density</li>
                <li>Connectivity metrics</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3 style='color: #FF6D1F;'>📈 ADVANCED ANALYTICS</h3>
            <p style='font-family: Poppins, sans-serif;'>Deep graph analysis with comprehensive metrics and visualizations 
            for understanding graph properties and relationships.</p>
            <ul style='font-family: Poppins, sans-serif;'>
                <li>Degree distribution</li>
                <li>Path analysis</li>
                <li>Centrality measures</li>
                <li>Cluster analysis</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Team Section
    st.markdown("---")
    st.markdown('<h2 class="section-title">👨‍💻 DEVELOPMENT TEAM</h2>', unsafe_allow_html=True)
    
    team_col1, team_col2, team_col3 = st.columns(3)
    
    with team_col1:
        st.markdown("<div class='profile-card'>", unsafe_allow_html=True)
        st.image("Jasmi.jpg", width=180)
        st.markdown("""
        <div class="profile-card">
            <h3 style='color: #FF6D1F; font-family: Montserrat, sans-serif;'>JASMIANA CELSMIN ARAUJO</h3>
            <p style='font-family: Poppins, sans-serif;'><strong>NIM:</strong> 021202500026</p>
            <div style='background: #FAF3E1; padding: 20px; border-radius: 10px; margin: 15px 0;'>
                <strong style='color: #222222; font-family: Montserrat, sans-serif;'>KEY CONTRIBUTIONS:</strong>
                <ul style='text-align: left; color: #222222; font-family: Poppins, sans-serif;'>
                    <li>Main video creation and compilation</li>
                    <li>Introduction section development</li>
                    <li>Sub-topic material creation</li>
                    <li>Project coordination</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with team_col2:
        st.markdown("<div class='profile-card'>", unsafe_allow_html=True)
        st.image("Angel.jpg", width=180)
        st.markdown("""
        <div class="profile-card">
            <h3 style='color: #FF6D1F; font-family: Montserrat, sans-serif;'>ANGEL MARGARETHA</h3>
            <p style='font-family: Poppins, sans-serif;'><strong>NIM:</strong> 021202500007</p>
            <div style='background: #FAF3E1; padding: 20px; border-radius: 10px; margin: 15px 0;'>
                <strong style='color: #222222; font-family: Montserrat, sans-serif;'>KEY CONTRIBUTIONS:</strong>
                <ul style='text-align: left; color: #222222; font-family: Poppins, sans-serif;'>
                    <li>Presentation slides design</li>
                    <li>Video closing concepts</li>
                    <li>Learning materials development</li>
                    <li>Content quality assurance</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with team_col3:
        st.markdown("<div class='profile-card'>", unsafe_allow_html=True)
        st.image("gunanjar.jpg", width=180)
        st.markdown("""
        <div class="profile-card">
            <h3 style='color: #FF6D1F; font-family: Montserrat, sans-serif;'>GUNANJAR AHMAD PRASETYO</h3>
            <p style='font-family: Poppins, sans-serif;'><strong>NIM:</strong> 021202500020</p>
            <div style='background: #FAF3E1; padding: 20px; border-radius: 10px; margin: 15px 0;'>
                <strong style='color: #222222; font-family: Montserrat, sans-serif;'>KEY CONTRIBUTIONS:</strong>
                <ul style='text-align: left; color: #222222; font-family: Poppins, sans-serif;'>
                    <li>Component synchronization</li>
                    <li>Sub-topic development</li>
                    <li>Content structure design</li>
                    <li>Technical implementation</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

# =========================
# GRAPH VISUALIZATION PAGE
# =========================
elif st.session_state.current_page == "Graph Visualization":
    st.markdown('<h1 class="section-title">📊 GRAPH VISUALIZATION</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown('<div class="graph-container">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #FF6D1F; font-family: Montserrat, sans-serif;">⚙️ GRAPH CONFIGURATION</h3>', unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["🎲 RANDOM GRAPH", "🛠️ CUSTOM GRAPH"])
        
        with tab1:
            st.write("**Quick Random Graph Generation**")
            num_nodes = st.slider("Number of Nodes", 2, 15, 6, key="random_nodes")
            max_edges = num_nodes * (num_nodes - 1) // 2
            num_edges = st.slider("Number of Edges", 1, max_edges, min(8, max_edges), key="random_edges")
            
            if st.button("🎲 GENERATE RANDOM GRAPH", key="generate_random", use_container_width=True):
                G, positions = create_random_graph(num_nodes, num_edges)
                st.session_state.graph = G
                st.session_state.node_positions = positions
                st.success(f"✅ Generated graph with {num_nodes} nodes and {num_edges} edges!")
        
        with tab2:
            st.write("**Build Custom Graph**")
            st.info("💡 Enter edges in format: '1-2' or '1-2,3-4,5-1'")
            edge_input = st.text_area("Edges (comma separated):", "1-2,2-3,3-4,4-1,1-5,5-3", height=100)
            
            weight_option = st.checkbox("Add random weights to edges", value=True)
            
            if st.button("🛠️ BUILD CUSTOM GRAPH", key="build_custom", use_container_width=True):
                edges = []
                for edge in edge_input.split(','):
                    edge = edge.strip()
                    if '-' in edge:
                        nodes = edge.split('-')
                        if len(nodes) == 2:
                            try:
                                u, v = int(nodes[0]), int(nodes[1])
                                edges.append((u, v))
                            except ValueError:
                                st.error("❌ Please enter valid node numbers (e.g., '1-2')")
                
                if edges:
                    G = nx.Graph()
                    
                    # Add edges with optional weights
                    for edge in edges:
                        if weight_option:
                            weight = random.randint(1, 20)
                            G.add_edge(edge[0], edge[1], weight=weight)
                        else:
                            G.add_edge(edge[0], edge[1])
                    
                    # Generate circular layout for better visualization
                    positions = {}
                    nodes = list(G.nodes())
                    center_x, center_y = 5, 5
                    radius = 4
                    
                    for i, node in enumerate(nodes):
                        angle = 2 * np.pi * i / len(nodes)
                        x = center_x + radius * np.cos(angle)
                        y = center_y + radius * np.sin(angle)
                        positions[node] = (x, y)
                    
                    st.session_state.graph = G
                    st.session_state.node_positions = positions
                    st.success(f"✅ Created graph with {len(G.nodes())} nodes and {len(G.edges())} edges!")
        
        # Graph Information
        if len(st.session_state.graph.nodes()) > 0:
            st.markdown("---")
            st.markdown('<h4 style="color: #FF6D1F; font-family: Montserrat, sans-serif;">📈 GRAPH INFORMATION</h4>', unsafe_allow_html=True)
            
            G = st.session_state.graph
            info_col1, info_col2 = st.columns(2)
            
            with info_col1:
                st.metric("Nodes", len(G.nodes()))
                st.metric("Density", f"{nx.density(G):.3f}")
            
            with info_col2:
                st.metric("Edges", len(G.edges()))
                connected = "Yes" if nx.is_connected(G) else "No"
                st.metric("Connected", connected)
            
            # Node degrees
            degrees = calculate_degree(G)
            st.write("**Node Degrees:**")
            degree_text = ", ".join([f"Node {node}: {deg}" for node, deg in degrees.items()])
            st.write(degree_text)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Right side: Graph Visualization and Adjacency Matrix in tabs
        tab_viz, tab_matrix = st.tabs(["👁️ GRAPH VISUALIZATION", "🔢 ADJACENCY MATRIX"])
        
        with tab_viz:
            st.markdown('<div class="graph-container">', unsafe_allow_html=True)
            st.markdown('<h3 style="color: #FF6D1F; font-family: Montserrat, sans-serif;">👁️ GRAPH VISUALIZATION</h3>', unsafe_allow_html=True)
            
            if len(st.session_state.graph.nodes()) > 0:
                fig = visualize_graph(st.session_state.graph, st.session_state.node_positions)
                st.pyplot(fig)
            else:
                st.info("👆 Please generate or create a graph using the controls on the left to see the visualization here.")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab_matrix:
            st.markdown('<div class="matrix-container">', unsafe_allow_html=True)
            st.markdown('<h3 style="color: #FF6D1F; font-family: Montserrat, sans-serif;">🔢 ADJACENCY MATRIX</h3>', unsafe_allow_html=True)
            
            if len(st.session_state.graph.nodes()) > 0:
                adj_matrix = get_adjacency_matrix(st.session_state.graph)
                
                if adj_matrix.size > 0:
                    # Display matrix as styled table
                    nodes = sorted(st.session_state.graph.nodes())
                    adj_df = pd.DataFrame(adj_matrix, index=nodes, columns=nodes)
                    
                    # Custom styling function for the dataframe
                    def style_adj_matrix(val):
                        if val == 0:
                            return 'background-color: #FAF3E1; color: #666;'
                        else:
                            return 'background-color: #FF6D1F; color: white; font-weight: bold;'
                    
                    st.dataframe(adj_df.style.applymap(style_adj_matrix), use_container_width=True)
                    
                    # Matrix statistics
                    st.markdown("---")
                    st.markdown('<h4 style="color: #FF6D1F; font-family: Montserrat, sans-serif;">📊 MATRIX PROPERTIES</h4>', unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Shape:** {adj_matrix.shape}")
                        st.write(f"**Total Elements:** {adj_matrix.size}")
                    with col2:
                        st.write(f"**Non-zero Elements:** {np.count_nonzero(adj_matrix)}")
                        st.write(f"**Matrix Density:** {np.count_nonzero(adj_matrix) / adj_matrix.size:.3f}")
            else:
                st.info("👆 Please generate or create a graph first to see the adjacency matrix.")
            
            st.markdown('</div>', unsafe_allow_html=True)

# =========================
# MATRIX ANALYSIS PAGE
# =========================
elif st.session_state.current_page == "Matrix Analysis":
    st.markdown('<h1 class="section-title">🧮 MATRIX ANALYSIS</h1>', unsafe_allow_html=True)
    
    if len(st.session_state.graph.nodes()) == 0:
        st.warning("⚠️ Please create a graph first in the Graph Visualization page.")
        if st.button("GO TO GRAPH VISUALIZATION"):
            st.session_state.current_page = "Graph Visualization"
            st.rerun()
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="matrix-container">', unsafe_allow_html=True)
            st.markdown('<h3 style="color: #FF6D1F; font-family: Montserrat, sans-serif;">📊 NODE DEGREES ANALYSIS</h3>', unsafe_allow_html=True)
            
            degrees = calculate_degree(st.session_state.graph)
            
            # Create degree distribution visualization
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
            
            # Bar chart for degrees
            nodes = list(degrees.keys())
            degree_values = list(degrees.values())
            
            colors = ['#FF6D1F' if d == max(degree_values) else 
                     '#222222' if d == min(degree_values) else 
                     '#F5E7C6' for d in degree_values]
            
            bars = ax1.bar(nodes, degree_values, color=colors, edgecolor='#222222', linewidth=1.5)
            ax1.set_facecolor('#FAF3E1')
            ax1.set_xlabel('Nodes', color='#222222', fontsize=12, fontweight='bold', fontfamily='Montserrat')
            ax1.set_ylabel('Degree', color='#222222', fontsize=12, fontweight='bold', fontfamily='Montserrat')
            ax1.set_title('Node Degrees Distribution', color='#222222', fontsize=16, fontweight='bold', fontfamily='Montserrat')
            ax1.tick_params(colors='#222222')
            ax1.grid(True, alpha=0.3, color='#F5E7C6')
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height)}', ha='center', va='bottom',
                        color='#222222', fontweight='bold', fontsize=10, fontfamily='Montserrat')
            
            # Pie chart for degree distribution
            degree_counts = {}
            for deg in degree_values:
                degree_counts[deg] = degree_counts.get(deg, 0) + 1
            
            colors_pie = ['#FF6D1F', '#222222', '#F5E7C6', '#4ECDC4', '#45B7D1']
            ax2.pie(degree_counts.values(), labels=degree_counts.keys(), 
                   autopct='%1.1f%%', colors=colors_pie[:len(degree_counts)],
                   textprops={'color': '#222222', 'fontweight': 'bold', 'fontfamily': 'Montserrat'})
            ax2.set_title('Degree Distribution', color='#222222', fontsize=16, fontweight='bold', fontfamily='Montserrat')
            
            fig.patch.set_facecolor('#FAF3E1')
            st.pyplot(fig)
            
            # Degree statistics
            st.markdown('<h4 style="color: #FF6D1F; font-family: Montserrat, sans-serif;">📈 DEGREE STATISTICS</h4>', unsafe_allow_html=True)
            stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
            
            with stats_col1:
                st.metric("Maximum Degree", max(degrees.values()))
            with stats_col2:
                st.metric("Minimum Degree", min(degrees.values()))
            with stats_col3:
                st.metric("Average Degree", f"{sum(degrees.values()) / len(degrees):.2f}")
            with stats_col4:
                st.metric("Total Degree", sum(degrees.values()))
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="matrix-container">', unsafe_allow_html=True)
            st.markdown('<h3 style="color: #FF6D1F; font-family: Montserrat, sans-serif;">🔢 ADJACENCY MATRIX HEATMAP</h3>', unsafe_allow_html=True)
            
            adj_matrix = get_adjacency_matrix(st.session_state.graph)
            
            if adj_matrix.size > 0:
                # Matrix heatmap
                fig, ax = plt.subplots(figsize=(10, 8))
                nodes = sorted(st.session_state.graph.nodes())
                
                im = ax.imshow(adj_matrix, cmap='Oranges', interpolation='nearest')
                
                # Set ticks and labels
                ax.set_xticks(range(len(nodes)))
                ax.set_yticks(range(len(nodes)))
                ax.set_xticklabels(nodes, color='#222222', fontweight='bold', fontfamily='Montserrat')
                ax.set_yticklabels(nodes, color='#222222', fontweight='bold', fontfamily='Montserrat')
                
                # Add values to cells
                for i in range(len(nodes)):
                    for j in range(len(nodes)):
                        text = ax.text(j, i, f'{int(adj_matrix[i, j])}', 
                                     ha='center', va='center', 
                                     color='white' if adj_matrix[i, j] > 0 else '#666',
                                     fontweight='bold', fontfamily='Montserrat')
                
                ax.set_title('Adjacency Matrix Heatmap', color='#222222', fontsize=18, fontweight='bold', fontfamily='Montserrat', pad=20)
                ax.set_facecolor('#FAF3E1')
                fig.patch.set_facecolor('#FAF3E1')
                
                # Add colorbar
                cbar = plt.colorbar(im, ax=ax)
                cbar.ax.tick_params(colors='#222222')
                cbar.set_label('Edge Weight', color='#222222', fontfamily='Montserrat')
                
                st.pyplot(fig)
            
            # Advanced matrix properties
            st.markdown('<h4 style="color: #FF6D1F; font-family: Montserrat, sans-serif;">📋 ADVANCED MATRIX PROPERTIES</h4>', unsafe_allow_html=True)
            
            if adj_matrix.size > 0:
                adv_col1, adv_col2 = st.columns(2)
                
                with adv_col1:
                    st.write(f"**Shape:** {adj_matrix.shape}")
                    st.write(f"**Total Elements:** {adj_matrix.size}")
                    st.write(f"**Non-zero Elements:** {np.count_nonzero(adj_matrix)}")
                
                with adv_col2:
                    st.write(f"**Matrix Density:** {np.count_nonzero(adj_matrix) / adj_matrix.size:.3f}")
                    st.write(f"**Symmetric:** {np.array_equal(adj_matrix, adj_matrix.T)}")
                    st.write(f"**Trace:** {np.trace(adj_matrix)}")
            
            st.markdown('</div>', unsafe_allow_html=True)

# =========================
# JAVA ROUTE FINDER PAGE
# =========================
elif st.session_state.current_page == "Java Route Finder":
    st.markdown('<h1 class="section-title">🗺️ JAVA ISLAND ROUTE PLANNER</h1>', unsafe_allow_html=True)
    
    # Initialize Java highway graph
    if 'java_graph' not in st.session_state:
        st.session_state.java_graph = create_java_highway_graph()
    
    # Main layout
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        st.markdown('<div class="map-container">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #FF6D1F; font-family: Montserrat, sans-serif;">📍 SELECT YOUR ROUTE</h3>', unsafe_allow_html=True)
        
        # City selection
        city_list = sorted(java_cities.keys())
        
        start_city = st.selectbox(
            "🚗 Start City:",
            city_list,
            index=city_list.index("Jakarta") if "Jakarta" in city_list else 0
        )
        
        end_city = st.selectbox(
            "🎯 Destination City:",
            [city for city in city_list if city != start_city],
            index=city_list.index("Surabaya") if "Surabaya" in city_list and "Surabaya" != start_city else 0
        )
        
        if st.button("🔍 FIND ROUTES", use_container_width=True):
            with st.spinner("Finding optimal routes..."):
                routes = find_all_routes(start_city, end_city, max_routes=4)
                
                if routes:
                    st.session_state.available_routes = routes
                    st.session_state.selected_route = routes[0]  # Default to shortest route
                    st.success(f"Found {len(routes)} route options!")
                else:
                    st.error("No routes found between selected cities. Please try different cities.")
                    st.session_state.available_routes = None
                    st.session_state.selected_route = None
        
        # Display route options if available
        if 'available_routes' in st.session_state and st.session_state.available_routes:
            st.markdown("---")
            st.markdown('<h4 style="color: #FF6D1F; font-family: Montserrat, sans-serif;">🛣️ AVAILABLE ROUTES</h4>', unsafe_allow_html=True)
            
            for i, route in enumerate(st.session_state.available_routes):
                is_selected = st.session_state.selected_route and st.session_state.selected_route['path'] == route['path']
                is_recommended = route['type'] == 'shortest'
                
                route_class = "route-option"
                if is_selected:
                    route_class += " selected"
                if is_recommended:
                    route_class += " recommended"
                
                st.markdown(f'<div class="{route_class}">', unsafe_allow_html=True)
                
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    st.write(f"**{route['name']}**")
                    st.write(f"📍 {' → '.join(route['path'])}")
                with col_b:
                    st.write(f"**{route['distance']} km**")
                
                if st.button(f"Select This Route", key=f"select_route_{i}", use_container_width=True):
                    st.session_state.selected_route = route
                    st.rerun()
                
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Route details for selected route
        if st.session_state.selected_route:
            st.markdown("---")
            st.markdown('<h4 style="color: #FF6D1F; font-family: Montserrat, sans-serif;">📋 ROUTE DETAILS</h4>', unsafe_allow_html=True)
            
            route = st.session_state.selected_route
            st.write(f"**Total Distance:** {route['distance']} km")
            st.write(f"**Number of Stops:** {len(route['path'])}")
            st.write("**Route Breakdown:**")
            
            for i, city in enumerate(route['path']):
                col_a, col_b = st.columns([1, 4])
                with col_a:
                    if i == 0:
                        st.markdown("🚩")
                    elif i == len(route['path']) - 1:
                        st.markdown("🏁")
                    else:
                        st.markdown(f"**{i}.**")
                with col_b:
                    if i == 0:
                        st.markdown(f"**START:** {city}")
                    elif i == len(route['path']) - 1:
                        st.markdown(f"**DESTINATION:** {city}")
                    else:
                        st.markdown(f"**Stop {i}:** {city}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="map-container">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #FF6D1F; font-family: Montserrat, sans-serif;">🗺️ INTERACTIVE JAVA MAP</h3>', unsafe_allow_html=True)
        
        # Create base map centered on Java
        java_center = [-7.5, 110.0]
        m = folium.Map(
            location=java_center,
            zoom_start=7,
            tiles='OpenStreetMap'
        )
        
        # Add all city markers
        for city, coord in java_cities.items():
            # Determine marker color based on selection
            if st.session_state.selected_route and city in st.session_state.selected_route['path']:
                if city == st.session_state.selected_route['path'][0]:
                    icon_color = 'green'
                    icon_type = 'play'
                    popup_text = f"<b>START: {city}</b>"
                elif city == st.session_state.selected_route['path'][-1]:
                    icon_color = 'red'
                    icon_type = 'stop'
                    popup_text = f"<b>END: {city}</b>"
                else:
                    icon_color = 'blue'
                    icon_type = 'info-sign'
                    popup_text = f"<b>{city}</b> (Route Stop)"
            else:
                icon_color = 'gray'
                icon_type = 'info-sign'
                popup_text = f"<b>{city}</b>"
            
            folium.Marker(
                coord,
                popup=popup_text,
                tooltip=city,
                icon=folium.Icon(color=icon_color, icon=icon_type, prefix='fa')
            ).add_to(m)
        
        # Draw selected route if available
        if st.session_state.selected_route:
            route = st.session_state.selected_route
            route_coords = [java_cities[city] for city in route['path']]
            
            # Add the main route line
            folium.PolyLine(
                route_coords,
                color='#FF6D1F',
                weight=6,
                opacity=0.9,
                popup=f"<b>{route['name']}</b><br>Distance: {route['distance']} km<br>{' → '.join(route['path'])}",
                tooltip="Click for route details"
            ).add_to(m)
        
        # Display the map
        st_folium(m, width=700, height=600)
        
        # Map legend
        st.markdown("""
        <div style='background: #FAF3E1; padding: 10px; border-radius: 5px; margin-top: 10px;'>
        <strong>Map Legend:</strong><br>
        🟢 <span style='color: green;'>Start City</span> | 
        🔴 <span style='color: red;'>Destination</span> | 
        🔵 <span style='color: blue;'>Route Stops</span> | 
        ⚫ <span style='color: gray;'>Other Cities</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# =========================
# FOOTER
# =========================
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #222222; padding: 30px; font-family: Poppins, sans-serif;'>"
    "🌐 <b>GRAPH MATRIX PRO</b> - FINAL PROJECT © 2024 | "
    "DEVELOPED WITH STREAMLIT & NETWORKX | "
    "COMPREHENSIVE GRAPH ANALYSIS & JAVA ROUTE PLANNING"
    "</div>",
    unsafe_allow_html=True
)