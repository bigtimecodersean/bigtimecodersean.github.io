import {select} from 'd3'
import { getURLParameter } from './preRenderNetwork'

const setupSlider = (id: string) => {
    console.log("setting up slider")
    select(id)
        .attr("value", "0") // Set the initial value to the leftmost position (minimum value)        .attr("value", getURLParameter('timestamp'))
        .on("change", (d) => {
            console.log(d.target.value)
            window.location.href = `/?timestamp=${d.target.value}`;

        })
}

export {setupSlider}