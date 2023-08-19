
import Graph from 'graphology';
import {density} from 'graphology-metrics/graph/density';
import {bidirectional} from 'graphology-shortest-path';
import degreeAssortativity from 'graphology-metrics';


// Passing a graph instance


export function setupNetworkStatistics(element: string) {

    // Density 

    const graph = new Graph();


    graph.addNode('A');
    graph.addNode('B');
    graph.addNode('C');
    graph.addNode('D');
    graph.addEdge('A', 'B');
    graph.addEdge('A', 'C');
    graph.addEdge('B', 'C');
    graph.addEdge('C', 'D');

    
    // Displaying useful information about your graph
    console.log('Number of nodes', graph.order);
    console.log('Number of edges', graph.size);
    
    // Iterating over nodes
    graph.forEachNode(node => {
      console.log(node);
    });

    const d = density(graph);
    console.log("density", d)


    // Average Path Length 

    function averagePathLength(graph: any) {
        let totalPathLength = 0;
        let numPairs = 0;
      
        for (const sourceNode of graph.nodes()) {
          for (const targetNode of graph.nodes()) {
            if (sourceNode !== targetNode) {
              const path = bidirectional(graph, sourceNode, targetNode);
              if (path !== null) {
                totalPathLength += path.length - 1;
                numPairs++;
              }
            }
          }
        }
      
        return totalPathLength / numPairs;
      }
      
      const avgPathLength = averagePathLength(graph);
      console.log('Average Path Length:', avgPathLength);


    // Clustering Coefficient (of whole graph)

    // Calculate the clustering coefficient for a specific node
        function nodeClusteringCoefficient(graph: any, node: any) {
        const neighbors = graph.neighbors(node);
        const numNeighbors = neighbors.length;

        if (numNeighbors < 2) {
            return 0;
        }

        let numTriangles = 0;

        for (let i = 0; i < numNeighbors; i++) {
            for (let j = i + 1; j < numNeighbors; j++) {
            if (graph.hasEdge(neighbors[i], neighbors[j])) {
                numTriangles++;
            }
            }
        }

        const possibleTriangles = (numNeighbors * (numNeighbors - 1)) / 2;
        return numTriangles / possibleTriangles;
        }

        // Calculate the global clustering coefficient for the entire graph
        function globalClusteringCoefficient(graph: any) {
        const nodes = graph.nodes();
        const numNodes = nodes.length;
        let totalClusteringCoefficient = 0;

        for (const node of nodes) {
            totalClusteringCoefficient += nodeClusteringCoefficient(graph, node);
        }

        return totalClusteringCoefficient / numNodes;
        }

        const avgClusteringCoefficient = globalClusteringCoefficient(graph);
        console.log('Global clustering coefficient:', avgClusteringCoefficient);



        // Global Efficiency 

        // Calculate the shortest path length between two nodes
        function shortestPathLength(graph: any, sourceNode: any, targetNode: any) {
            const path = bidirectional(graph, sourceNode, targetNode);
            return path ? path.length - 1 : Infinity;
        }
        
        // Calculate the global efficiency of the graph
        function globalEfficiency(graph: any) {
            let totalEfficiency = 0;
            let numPairs = 0;
        
            for (const sourceNode of graph.nodes()) {
            for (const targetNode of graph.nodes()) {
                if (sourceNode !== targetNode) {
                const pathLength = shortestPathLength(graph, sourceNode, targetNode);
                totalEfficiency += 1 / pathLength;
                numPairs++;
                }
            }
            }
        
            return totalEfficiency / numPairs;
        }
        
        const efficiency = globalEfficiency(graph);
        console.log('Global Efficiency:', efficiency);

        // Graph Centralization 


        // Calculate the degree centralization of the graph
        function degreeCentralization(graph: any) {
            const nodes = graph.nodes();
            const maxDegree = nodes.reduce((max: any, node: any) => {
            const degree = graph.degree(node);
            return degree > max ? degree : max;
            }, 0);
        
            let totalDifference = 0;
        
            for (const node of nodes) {
            const degree = graph.degree(node);
            totalDifference += maxDegree - degree;
            }
        
            const normalizedDifference = totalDifference / ((nodes.length - 1) * (nodes.length - 2));
            return normalizedDifference;
        }
        
        const centralization = degreeCentralization(graph);
        console.log('Degree Centralization:', centralization);


        const assortativity = degreeAssortativity(graph);
        console.log('Degree Assortativity Coefficient:', assortativity);


}


