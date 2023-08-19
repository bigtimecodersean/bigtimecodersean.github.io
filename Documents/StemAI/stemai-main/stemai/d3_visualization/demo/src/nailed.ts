import { select, scaleLinear, line, curveLinear, axisBottom, axisLeft } from "d3";
import graph from "./input.json";


const data1 = graph.nailed_it
const data2 = graph.nailed_it_trailing

    
const maxData1Value = data1.reduce((max, item) => Math.max(max, item.value), -Infinity);
const maxData2Value = data2.reduce((max, item) => Math.max(max, item.value), -Infinity);
const maxValue = Math.max(maxData1Value, maxData2Value);

const minData1Value = data1.reduce((min, item) => Math.min(min, item.value), Infinity);
const minData2Value = data2.reduce((min, item) => Math.min(min, item.value), Infinity);
const minValue = Math.min(minData1Value, minData2Value);

export function setupNailed(element: string) {
  
    const data_length = data1.length
    const constantValue = .5


    const constArray = [];
    for (let time = 0; time < data_length; time++) {
        constArray.push({ time, value: constantValue
         });
    }

    const legendData = [
        { label: "Seed Cell sent same signal as env", color: "blue" },
        { label: "Nailed it Trailing", color: "orange" }
    ];

    // SVG dimensions
    const width = 600;
    const height = 400;
    const margin = { top: 50, right: 30, bottom: 30, left: 40 };
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    const svg = select(element)
        .append("svg")
        .attr("height", height)
        .attr("width", width);

    // Create scales
    const xScale = scaleLinear()
        .domain([0, data1.length - 1])
        .range([0, innerWidth]);

    const yScale = scaleLinear()
        .domain([minValue - .1, maxValue])
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

    const lineGeneratorConstant = line<{ time: number; value: number }>()
        .x(d => xScale(d.time))
        .y(d => yScale(constantValue))
        .curve(curveLinear);

    const graphGenerator = svg.selectAll(".nailedGroup")
        .data([0])
        .join("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

    graphGenerator.selectAll(".nailedTimeline")
        .data([data1])
        .join("path")
        .attr("class", "nailedTimeline")
        .attr("d", d => lineGenerator1(d))
        .attr("stroke", "blue") 
        .attr("fill", "none")
        .attr("opacity", .2);

    graphGenerator.selectAll(".nailedIt")        
        .data([data1.slice(0,1)])
        .join("path")
        .attr("class", "nailedIt")
        .attr("d", d => lineGenerator1(d))
        .attr("stroke", "blue") 
        .attr("fill", "none")
        .attr("opacity", 1);

    graphGenerator.selectAll(".nailedTrailingTimeline")
        .data([data2])
        .join("path")
        .attr("class", "nailedTrailingTimeline")
        .attr("d", d => lineGenerator2(d))
        .attr("stroke", "orange") 
        .attr("fill", "none")
        .attr("opacity", .4);

    graphGenerator.selectAll(".nailedItTrailing")
        .data([data2.slice(0,1)])
        .join("path")
        .attr("class", "nailedItTrailing")
        .attr("d", d => lineGenerator2(d))
        .attr("stroke", "orange") 
        .attr("fill", "none")
        .attr("opacity", 1);

    graphGenerator.selectAll(".constantTimeline")
        .data([constArray])
        .join("path")
        .attr("class", "constantTimeline")
        .attr("d", d => lineGeneratorConstant(d))
        .attr("stroke", "green") 
        .attr("fill", "none")
        .attr("opacity", .1);

    graphGenerator.selectAll(".constant")
        .data([constArray.slice(0,1)])
        // .data([constantValue])
        .join("path")
        .attr("class", "constant")
        .attr("d", d => lineGeneratorConstant(d))
        .attr("stroke", "green") 
        .attr("fill", "none")
        .attr("opacity", 1);


    // Add x-axis
    graphGenerator.append("g")
        .attr("transform", `translate(0,${innerHeight})`)
        .call(axisBottom(xScale));

    // Add y-axis
    graphGenerator.append("g")
        .call(axisLeft(yScale));


    // Add legend
    const legend = svg.append("g")
    .attr("class", "legend")
    .attr("transform", `translate(${ margin.left + 300},${margin.top + 100})`); // Position the legend in the top right

    const legendItems = legend.selectAll(".legend-item")
    .data(legendData)
    .enter().append("g")
    .attr("class", "legend-item")
    .attr("transform", (d, i) => `translate(0, ${i * 20})`); // Spacing between legend items

    legendItems.append("circle")
    .attr("cx", 10)
    .attr("cy", -5)
    .attr("r", 5)
    .style("fill", d => d.color);

    legendItems.append("text")
    .attr("x", 20)
    .attr("y", 0)
    .text(d => d.label);

    svg.append("text")
        .attr("x", width / 2)
        .attr("y", margin.top / 2) // Positioned above the graph
        .attr("text-anchor", "middle")
        .attr("font-size", "16px")
        .text("Seed Cell Nailed It?");

}



export function animateNailed(element: string, timestamp: number) {
  
    const data1 = graph.nailed_it
    const data2 = graph.nailed_it_trailing

    const data_length = data1.length
    const constantValue = .5

    // const constArray: number[] = new Array(data_length).fill(constantValue);


    const constArray = [];
    for (let time = 0; time < data_length; time++) {
        constArray.push({ time, value: constantValue
         });
    }

    // SVG dimensions
    const width = 600;
    const height = 400;
    const margin = { top: 50, right: 30, bottom: 30, left: 40 };
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

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

    const lineGeneratorConstant = line<{ time: number; value: number }>()
        .x(d => xScale(d.time))
        .y(d => yScale(constantValue))
        .curve(curveLinear);

    select(element)
        .selectAll(".nailedIt")
        .data([data1.slice(0,timestamp)])
        .join("path")
        .attr("class", "nailedIt")
        .attr("d", d => lineGenerator1(d))
        .attr("stroke", "orange") 
        .attr("fill", "none")
        .attr("opacity", 1);


    select(element)
        .selectAll(".nailedItTrailing")
        .data([data2.slice(0,timestamp)])
        .join("path")
        .attr("class", "nailedItTrailing")
        .attr("d", d => lineGenerator2(d))
        .attr("stroke", "blue") 
        .attr("fill", "none")
        .attr("opacity", 1);

    select(element)
        .selectAll(".constant")
        .data([constArray.slice(0,timestamp)])
        .join("path")
        .attr("class", "constant")
        .attr("d", d => lineGeneratorConstant(d))
        .attr("stroke", "green") 
        .attr("fill", "none")
        .attr("opacity", 1);


 

}