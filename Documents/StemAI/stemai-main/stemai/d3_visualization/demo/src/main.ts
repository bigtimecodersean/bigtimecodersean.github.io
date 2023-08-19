import './style.css'
import { setupNetwork } from './preRenderNetwork.ts'
import { setupLegend } from './legend.ts'

import { RenderGraph, setupPostRenderNetwork } from './postRenderNetwork.ts'
import data from '../../exports/output.json'
import input_data from './input.json'


import { setupSlider } from './timeslider.ts'
import { setupMessages } from './messages.ts'
import { setupNailed } from './nailed.ts'
import { setupNumCells } from './numCells.ts'
import { setupSeedCellSuffering } from './seedCellSuffering.ts'
import { setupSelfEfficacies } from './selfEfficacies.ts'
import { setupStemnesses } from './stemnesses.ts'
import { setupStresses } from './stresses.ts'
import { setupNetworkStatistics } from './networkStatistics.ts'

// import { setupPlayButton } from './playButton.ts'

const max = input_data.max_timestamps - 1
console.log("max timesteps: " + max)

document.querySelector<HTMLDivElement>('#app')!.innerHTML = `
  <div class="container">
    <h1>StemAI Visualization </h1>
    <div class="charts">
      <div id="prerender_chart"></div>
      <div id="postrender_chart"></div>
      <div id="legend"></div>
      <div id="networkStatistics"></div>
       

    </div>
    
    <input type="range" id="timeslider" name="timeslider" min="0" max=${max}>
    <button id="play">Play</button>
    <p>Current Timestamp <span id="currentTimestampLabel"> 0 </span><p>

    <div class="chartsContainers">

      <div id="messages"></div>
      <div id="nailed"></div>
      <div id="numCells"></div>
      <div id="seedCellSuffering"></div>
      <div id="selfEfficacies"></div>
      <div id="stemnesses"></div>
      <div id="stresses"></div>
    
    </div>

  </div>
`

setupNetwork('#prerender_chart', "#play", max)
// setupPostRenderNetwork('#postrender_chart', data as unknown as RenderGraph) //Add num_timestamps as parameter
setupLegend('#legend')
// setupNetworkStatistics("#networkStatistics")
setupSlider("#timeslider")
setupMessages("#messages")
setupNailed("#nailed")
setupNumCells("#numCells")
setupSeedCellSuffering("#seedCellSuffering")
setupSelfEfficacies("#selfEfficacies")
setupStemnesses("#stemnesses")
setupStresses("#stresses")

// setupPlayButton("#play", max)
