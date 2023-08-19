import { select, scaleLinear, line, curveLinear, axisBottom, axisLeft, max, selectAll } from "d3";
import graph from "./input.json";

export function setupNumCells(element: string) {

    const data = graph.num_cells
 
    // SVG dimensions
    const width = 600;
    const height = 400;
    const margin = { top: 50, right: 30, bottom: 30, left: 40 };
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    const maxValue = data.reduce((max, item) => Math.max(max, item.value), -Infinity);
    const minValue = data.reduce((min, item) => Math.min(min, item.value), Infinity);


    const svg = select(element)
        .append("svg")
        .attr("height", height)
        .attr("width", width);

    // Create scales
    const xScale = scaleLinear()
        .domain([0, data.length - 1])
        .range([0, innerWidth]);

    const yScale = scaleLinear()
        .domain([.9*minValue, 1.1*maxValue])
        .range([innerHeight, 0]);

    // Create line generator
    const lineGenerator1 = line<{ time: number; value: number }>()
        .x(d => xScale(d.time))
        .y(d => yScale(d.value))
        .curve(curveLinear);

    // Create graph area
    const graphGenerator = svg.selectAll(".numCellsGroup")
        .data([0])
        .join("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);



    // Create line path
    graphGenerator.selectAll(".numCellsTimeline")
        .data([data])
        .join("path")
        .attr("class", "numCellsTimeline")
        .attr("d", d => lineGenerator1(d))
        .attr("stroke", "red") 
        .attr("fill", "none")
        .attr("opacity", .1);

    graphGenerator.selectAll(".numCells")
        .data([data.slice(0,1)])
        .join("path")
        .attr("class", "numCells")
        .attr("d", d => lineGenerator1(d))
        .attr("stroke", "red") 
        .attr("fill", "none")
        .attr("opacity", 1);

    // Add x-axis
    graphGenerator.append("g")
        .attr("transform", `translate(0,${innerHeight})`)
        .call(axisBottom(xScale));

    // Add y-axis
    graphGenerator.append("g")
        .call(axisLeft(yScale));

    svg.append("text")
        .attr("x", width / 2)
        .attr("y", margin.top / 2) // Positioned above the graph
        .attr("text-anchor", "middle")
        .attr("font-size", "16px")
        .text("Number of Cells");
}

export function animateNumCells(element: string, timestamp: number) {

    const data = graph.num_cells
 
    // SVG dimensions
    const width = 600;
    const height = 400;
    const margin = { top: 50, right: 30, bottom: 30, left: 40 };
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    const maxValue = data.reduce((max, item) => Math.max(max, item.value), -Infinity);
    const minValue = data.reduce((min, item) => Math.min(min, item.value), Infinity);

    // Create scales
    const xScale = scaleLinear()
        .domain([0, data.length - 1])
        .range([0, innerWidth]);

    const yScale = scaleLinear()
        .domain([.9*minValue, 1.1*maxValue])
        .range([innerHeight, 0]);

    // Create line generator
    const lineGenerator1 = line<{ time: number; value: number }>()
        .x(d => xScale(d.time))
        .y(d => yScale(d.value))
        .curve(curveLinear);

        select(element)
        .selectAll(".numCells")
        .data([data.slice(0,timestamp)])
        .join("path")
        .attr("class", "numCells")
        .attr("d", d => lineGenerator1(d))
        .attr("stroke", "red") 
        .attr("fill", "none")
        .attr("opacity", 1);

}