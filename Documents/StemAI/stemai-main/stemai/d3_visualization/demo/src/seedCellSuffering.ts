import { select, scaleLinear, line, curveLinear, axisBottom, axisLeft, max, min } from "d3";
import graph from "./input.json"

export function setupSeedCellSuffering(element: string) {

    const data1 = graph.min_efes
    const data2 = graph.mean_efes

    const legendData = [
        { label: "Min EFE of Seed Agent", color: "black", dashed: false},
        { label: "Mean EFE of Seed Agent", color: "black", dashed: true}
    ];

    // SVG dimensions
    const width = 600;
    const height = 400;
    const margin = { top: 50, right: 30, bottom: 30, left: 40 };
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    const maxData1Value = data1.reduce((max, item) => Math.max(max, item.value), -Infinity);
    const maxData2Value = data2.reduce((max, item) => Math.max(max, item.value), -Infinity);
    const maxValue = Math.max(maxData1Value, maxData2Value);

    const minData1Value = data1.reduce((min, item) => Math.min(min, item.value), Infinity);
    const minData2Value = data2.reduce((min, item) => Math.min(min, item.value), Infinity);
    const minValue = Math.min(minData1Value, minData2Value);

    const svg = select(element)
        .append("svg")
        .attr("height", height)
        .attr("width", width);

    // Create scales
    const xScale = scaleLinear()
        .domain([0, data1.length - 1])
        .range([0, innerWidth]);

    const yScale = scaleLinear()
        .domain([minValue, maxValue])
        .range([innerHeight, 0]);

    // Create line generator
    const lineGenerator1 = line<{ time: number; value: number }>()
        .x(d => xScale(d.time))
        .y(d => yScale(d.value))
        .curve(curveLinear);

    const lineGenerator2 = line<{ time: number; value: number }>()
        .x(d => xScale(d.time))
        .y(d => yScale(d.value))
        .curve(curveLinear);

    const graphGenerator = svg.selectAll(".sufferingGroup")
        .data([0])
        .join("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);
    
    graphGenerator.selectAll(".minEFETimeline")
        .data([data1])
        .join("path")
        .attr("class", "minEFETimeline")
        .attr("d", d => lineGenerator1(d))
        .attr("stroke", "black") 
        .attr("fill", "none")
        .attr("opacity", .2);

    graphGenerator.selectAll(".minEFE")
        .data([data1.slice(0,1)])
        .join("path")
        .attr("class", "minEFE")
        .attr("d", d => lineGenerator1(d))
        .attr("stroke", "black") 
        .attr("fill", "none")
        .attr("opacity", 1);

    graphGenerator.selectAll(".meanEFETimeline")
        .data([data2])
        .join("path")
        .attr("class", "meanEFETimeline")
        .attr("d", d => lineGenerator2(d))
        .attr("stroke", "blue") 
        .attr("fill", "none")
        .attr("stroke-dasharray", "5,5") // Specify the dash pattern;    
        .attr("opacity", .2);

    graphGenerator.selectAll(".meanEFE")
        .data([data2.slice(0,1)])
        .join("path")
        .attr("class", "meanEFE")
        .attr("d", d => lineGenerator2(d))
        .attr("stroke", "blue") 
        .attr("fill", "none")
        // .attr("stroke-dasharray", "5,5") // Specify the dash pattern;    
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
        .attr("y", margin.top / 2) 
        .attr("text-anchor", "middle")
        .attr("font-size", "16px")
        .text("Expected Suffering of Seed Cell");

    // Add legend
    const legend = svg.append("g")
    .attr("class", "legend")
    .attr("transform", `translate(${ margin.left + 300},${margin.top + 20})`);  

    const legendItems = legend.selectAll(".legend-item")
    .data(legendData)
    .enter().append("g")
    .attr("class", "legend-item")
    .attr("transform", (d, i) => `translate(0, ${i * 20})`); 

    legendItems.append("line")
    .attr("x1", 0) 
    .attr("y1", -5)
    .attr("x2",15) 
    .attr("y2", -5) 
    .style('stroke-dasharray', d => (d.dashed ? "3 3" : "none"))
    .style("stroke", d => d.color); // Set stroke color

    legendItems.append("text")
    .attr("x", 20)
    .attr("y", 0)
    .text(d => d.label);

}


export function animateSeedCellSuffering(element: string, timestamp: number) {
  
    const data1 = graph.min_efes
    const data2 = graph.mean_efes

    // SVG dimensions
    const width = 600;
    const height = 400;
    const margin = { top: 50, right: 30, bottom: 30, left: 40 };
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    const maxData1Value = data1.reduce((max, item) => Math.max(max, item.value), -Infinity);
    const maxData2Value = data2.reduce((max, item) => Math.max(max, item.value), -Infinity);
    const maxValue = Math.max(maxData1Value, maxData2Value);

    const minData1Value = data1.reduce((min, item) => Math.min(min, item.value), Infinity);
    const minData2Value = data2.reduce((min, item) => Math.min(min, item.value), Infinity);
    const minValue = Math.min(minData1Value, minData2Value);

    // Create scales
    const xScale = scaleLinear()
        .domain([0, data1.length - 1])
        .range([0, innerWidth]);

    const yScale = scaleLinear()
        .domain([minValue, maxValue])
        .range([innerHeight, 0]);

    // Create line generator
    const lineGenerator1 = line<{ time: number; value: number }>()
        .x(d => xScale(d.time))
        .y(d => yScale(d.value))
        .curve(curveLinear);

    const lineGenerator2 = line<{ time: number; value: number }>()
        .x(d => xScale(d.time))
        .y(d => yScale(d.value))
        .curve(curveLinear);

    select(element)
        .selectAll(".minEFE")
        .data([data1.slice(0,timestamp)])
        .join("path")
        .attr("class", "minEFE")
        .attr("d", d => lineGenerator1(d))
        .attr("stroke", "black") 
        .attr("fill", "none")
        .attr("opacity", 1);

    select(element)
        .selectAll(".meanEFE")
        .data([data2.slice(0,timestamp)])
        .join("path")
        .attr("class", "meanEFE")
        .attr("d", d => lineGenerator2(d))
        .attr("stroke", "black") 
        .attr("fill", "none")
        .attr("opacity", 1);
     
}