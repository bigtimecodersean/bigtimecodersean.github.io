---

permalink: "/projects/"
layout: page
---
Solo projects I've done 

--------

# Research / Engineering
### [SigLIP + Qwen2 + Flow Matching on LIBERO](https://github.com/bigtimecodersean/libero-vla)
A 1.5B-parameter Vision-Language-Action model (SigLIP + Qwen2-1.5B with LoRA + flow-matching action head) trained from scratch on the LIBERO manipulation benchmark, deliberately skipping the Open X-Embodiment pretraining that most published VLAs rely on. Reaches 70.5% across the four base suites in ~11 hours on a single H100, and isolates a specific failure mode: the long-horizon suite is bimodal — single-object multi-step tasks succeed at 70–80% while tasks requiring referent tracking across two distinct objects

### [RL for Simulated Humanoids](https://github.com/bigtimecodersean/RL-for-simulated-robotics) 
RL for simulated locomotion, scaling from MuJoCo Reacher on a laptop to Humanoid on an A100 with 4,096 parallel Isaac Gym envs. Quantifies the Bitter Lesson (PPO reward 500 → 6,300+ from compute alone, 9,500+ with bigger nets and LSTM) and documents reward-hacking failures like a HalfCheetah running on its back.

### [Transformer-From-Scratch ](https://github.com/bigtimecodersean/Transformer_From_Scratch)

This project was inspired by Andrej Karpathy's work at: [Let's Build GPT](https://www.youtube.com/watch?v=kCc8FmEb1nY). 

The goal for the project was to:
- Define a decoder-only transformer architecture
- Train on the WikiText V2 dataset
- Generate infinite Wikipedia-like text

### [Vision Transformer-From-Scratch](https://github.com/bigtimecodersean/Vision_Transformer_Replication)

I replicated a Vision Transformer, as developed in: https://arxiv.org/abs/2010.11929 ... and applied it to a classifying food categories. This project was part of Zero-to-Mastery's: Deep Learning with Pytorch

----------

# Miscellaneous  

### [ARC Project Proposal](https://docs.google.com/presentation/d/e/2PACX-1vQKjp7qxEyEPtcXp_PfDWNd3k7BnpISSyDA-DcY-CRSkvCWXVOtR27OIqLkreRNsCXxCk8h9LpPAWIk/pub?start=false&loop=false&delayms=3000) 

An informal presentation I gave to Dartmouth CS Profs on Francois Chollet's Abstraction and Reasoning (ARC) as an important benchmark for few-shot abstract rule learning. I included a few Neurosymbolic approaches that I found most promising.  

### [Numenta Active Dendrite](https://5744f6c2-4ed8-4ec0-a6a4-51909cc8f220.filesusr.com/ugd/e97160_d98a19334c954743adf683cb1df2b919.pdf)

Here is a written companion I wrote to a talk by Numenta's Subutai Ahmad Numenta titled: Active Dendrites Enable Flexible Context Integration. Active dendrites are a more biologically realistic model of individual neurons, enabling better prediction, more flexible learning, and efficient, sparse representations in Artificial Neural Networks.  

### [Investigating Motif Significance in the Drosophilidae Drosophila](https://5744f6c2-4ed8-4ec0-a6a4-51909cc8f220.filesusr.com/ugd/e97160_dcc99d36de424a1fbed10f7f4e635463.pdf)

Investigated recently mapped Drosophila fruit-fly connectome to measure the prevalence of complex structural network motifs, compared to C.elegans and simulated rat somatosensory cortex. Found a decrease in basic motifs, such as basic linked chains; an increase in more complex feedback structures (ie. 3-node structures with bidirectional connections) 

### [Exploring the Phenomenology of Haptic Stimulation](https://www.youtube.com/watch?v=ga88RGOzJwk) 

Designed and built a multi-sensory stimulation device that uses light, sound, and haptic vibration to induce targeted emotional states. In addition to building the device, I spent time mapping out the phenomenology of haptic vibration.

(For NDA purposes, I cannot publish photos of the finished product)

### [Geothermal Energy Drilling](https://5744f6c2-4ed8-4ec0-a6a4-51909cc8f220.filesusr.com/ugd/e97160_0f790d08b3854e9ba95aa4fb85f51c48.pdf) 

Mapping out the landscape of Geothermal Energy drilling technology. I focused in particular on Millimeter Wave drilling, of the type proposed by Quaise Energy I also propose the basic components of what a Geothermal PARPA might look like.

-------- 







