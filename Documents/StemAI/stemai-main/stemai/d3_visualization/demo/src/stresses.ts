import { select, scaleLinear, line, curveLinear, axisBottom, axisLeft } from "d3";
import graph from "./input.json";import { groupBy, uniqBy, values } from "lodash";


const cellMap: Record<string,string> = {
    "all": "blue"
}
const colorArray = ['#a6cee3', '#1f78b4','#b2df8a','#33a02c','#fb9a99','#e31a1c','#fdbf6f','#ff7f00', '#cab2d6' ,'#6a3d9a','#ffff99','#b15928']

export function setupStresses(element: string) {

    const data = graph.stresses

    const legendData = [
        { label: "cell 1", color: "blue" },
        { label: "cell 2", color: "orange" }
    ];
 
    // SVG dimensions
    const width = 600;
    const height = 400;
    const margin = { top: 50, right: 30, bottom: 30, left: 40 };
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    const results = Object.keys(data).flatMap(key => {
        const timestamps = Object.keys((data as any)[key])
        const values = Object.values((data as any)[key])
        return timestamps.map((time, index) => {
            return {time: parseInt(time), 
            value: values[index] as number, key}
        })
    })

    console.log(results)

    const maxValue = results.reduce((max, item) => Math.max(max, item.value), -Infinity);
    const minValue = results.reduce((min, item) => Math.max(min, item.value), Infinity);
    const timesteps = uniqBy(results, "time")

    const cells = values(groupBy(results, "key"))
    
    console.log(cells)

    const svg = select(element)
        .append("svg")
        .attr("height", height)
        .attr("width", width);

    // Create scales
    const xScale = scaleLinear()
        .domain([0, timesteps.length - 1])
        .range([0, innerWidth]);

    const yScale = scaleLinear()
        .domain([.9*Math.min(0, minValue) - .1, 1.1*maxValue])
        .range([innerHeight, 0]);

    // Create line generator
    const lineGenerator1 = line<{ time: number; value: number }>()
        .x(d => xScale(d.time))
        .y(d => yScale(d.value))
        .curve(curveLinear);

    // Create graph area
    const graphGenerator = svg.selectAll(".selfEfficaciesGroup")
        .data([0])
        .join("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);


    graphGenerator.selectAll(".selfEfficacies")
        .data(cells) 
        .join("path")
        .attr("class", "selfEfficacies")
        .attr("d", d => lineGenerator1(d))
        .attr("stroke", (d, i) => {
            console.log(d[0].key)
            const isInCellMap = d[0].key in cellMap
            
            if (isInCellMap){
                return cellMap[d[0].key]
            }

            return colorArray[i % colorArray.length]
        }) 
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
        .text("Stresses");

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

    

}



export function animateStresses(element: string, timestamp: number) {


    
}

