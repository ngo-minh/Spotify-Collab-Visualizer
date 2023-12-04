import React from 'react';
import Title from './Title';
import Instructions from './Instructions';
import Search from './Search';
import GraphVisualization from './GraphVisualization'; 
import ResetButton from './ResetButton';
import { convertToGraphData } from './GraphDataUtils';
import './App.css';
import TopCollaborators from './TopCollaborators';

// holds the state and functionality of the app
class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            topCollaborators: [],
            graphData: { nodes: [], edges: [] },
            vertexCount: 0,
            edgeCount: 0
        };
    }

// handle the graph data update
    handleGraphUpdate(data) {
        if (data.collaborations && data.artistId) {
            const convertedData = convertToGraphData(data.collaborations, data.artistId);
            this.setState({
                graphData: convertedData,
                vertexCount: data.vertex_count,
                edgeCount: data.edge_count
            });
        } else {
            console.error("Error in API:", data);
            this.setState({
                graphData: { nodes: [], edges: [] },
                vertexCount: 0,
                edgeCount: 0
            });
        }

        if (data.top_collaborators) {
            this.setState({ topCollaborators: data.top_collaborators });
        }
    }

// handle artist search
    handleSearch(artistName) {
        fetch('http://localhost:5000/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ artistName })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Error fetching data: ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            this.handleGraphUpdate(data);
        })
        .catch(error => {
            console.error("API Error:", error);
        });
    }

// reset the graph to its initial state and top collab. chart
    handleReset() {
        this.setState({
            graphData: { nodes: [], edges: [] },
            vertexCount: 0,
            edgeCount: 0,
            topCollaborators: []
        });
    }

   
// display components
    render() {
        return (
            <div className="app-container">
                <div className="visualization-container">
                    <Title />
                    <Instructions />
                    <Search onSearch={this.handleSearch.bind(this)} />
                    <GraphVisualization graphData={this.state.graphData} />
                    <div>Vertices (Unique Artists): {this.state.vertexCount}</div>
                    <div>Edges (Collaborations): {this.state.edgeCount}</div>
                    <ResetButton onReset={this.handleReset.bind(this)} />
                </div>
                <div className="top-collaborators-container">
                    <TopCollaborators collaborators={this.state.topCollaborators} />
                </div>
            </div>
        );
    }
}

export default App;
