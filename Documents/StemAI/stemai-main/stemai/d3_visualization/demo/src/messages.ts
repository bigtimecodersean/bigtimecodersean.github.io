import { select, scaleLinear, line, curveLinear, axisBottom, axisLeft } from "d3";
import graph from "./input.json";


export function setupMessages(element: string) {
  

    const data1 = graph.msgs_from_env
    const data2 = graph.self_msgs

    const maxData1Value = data1.reduce((max, item) => Math.max(max, item.value), -Infinity);
    const maxData2Value = data2.reduce((max, item) => Math.max(max, item.value), -Infinity);
    const maxValue = Math.max(maxData1Value, maxData2Value);

    const minData1Value = data1.reduce((min, item) => Math.min(min, item.value), Infinity);
    const minData2Value = data2.reduce((min, item) => Math.min(min, item.value), Infinity);
    const minValue = Math.min(minData1Value, minData2Value);

    console.log(minValue)
    console.log(data1)
    console.log(data2)

    const legendData = [
        { label: "Replies from Environment", color: "orange" },
        { label: "Self Messages", color: "blue" }
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

    // Create graph area
    // const graphGenerator = svg.append("g")
    //     .attr("transform", `translate(${margin.left},${margin.top})`);


    const graphGenerator = svg.selectAll(".messagesGroup")
        .data([0])
        .join("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);


    // Create line path
    // graphGenerator.append("path")
    //     .datum(data1)
    //     .attr("class", "line")
    //     .attr("d", lineGenerator1)
    //     .attr("stroke", "orange") 
    //     .attr("fill", "none");  


    // Create line path
    graphGenerator.selectAll(".messagesEnvTimeline")
        .data([data1])
        .join("path")
        .attr("class", "messagesEnvTimeline")
        .attr("d", d => lineGenerator1(d))
        .attr("stroke", "orange") 
        .attr("fill", "none")
        .attr("opacity", .2);

    graphGenerator.selectAll(".messagesEnv")
        .data([data1.slice(0,1)])
        .join("path")
        .attr("class", "messagesEnv")
        .attr("d", d => lineGenerator1(d))
        .attr("stroke", "orange") 
        .attr("fill", "none")
        .attr("opacity", 1);


    
    // graphGenerator.append("path")
    //     .datum(data2)
    //     .attr("class", "line")
    //     .attr("d", lineGenerator2)
    //     .attr("stroke", "blue") 
    //     .attr("fill", "none");  
    

    graphGenerator.selectAll(".messagesSelfTimeline")
        .data([data2])
        .join("path")
        .attr("class", "messagesSelfTimeline")
        .attr("d", d => lineGenerator2(d))
        .attr("stroke", "blue") 
        .attr("fill", "none")
        .attr("opacity", .1);

    graphGenerator.selectAll(".messagesSelf")
        .data([data2.slice(0,1)])
        .join("path")
        .attr("class", "messagesSelf")
        .attr("d", d => lineGenerator2(d))
        .attr("stroke", "blue") 
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
        .text("Messages from Environment and from Seed Cell for Seed Cell");
}


export function animateMessages(element: string, timestamp: number) {
  

    const data1 = graph.msgs_from_env
    const data2 = graph.self_msgs

    const maxData1Value = data1.reduce((max, item) => Math.max(max, item.value), -Infinity);
    const maxData2Value = data2.reduce((max, item) => Math.max(max, item.value), -Infinity);
    const maxValue = Math.max(maxData1Value, maxData2Value);

    const minData1Value = data1.reduce((min, item) => Math.min(min, item.value), Infinity);
    const minData2Value = data2.reduce((min, item) => Math.min(min, item.value), Infinity);
    const minValue = Math.min(minData1Value, minData2Value);


    // SVG dimensions
    const width = 600;
    const height = 400;
    const margin = { top: 50, right: 30, bottom: 30, left: 40 };
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    // const svg = select(element)
    //     .append("svg")
    //     .attr("height", height)
    //     .attr("width", width);

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


    select(element)
        .selectAll(".messagesEnv")
        .data([data1.slice(0,timestamp)])
        .join("path")
        .attr("class", "messagesEnv")
        .attr("d", d => lineGenerator1(d))
        .attr("stroke", "orange") 
        .attr("fill", "none")
        .attr("opacity", 1);

    select(element)
        .selectAll(".messagesSelf")
        .data([data2.slice(0,timestamp)])
        .join("path")
        .attr("class", "messagesSelf")
        .attr("d", d => lineGenerator2(d))
        .attr("stroke", "blue") 
        .attr("fill", "none")
        .attr("opacity", 1);

    
}


