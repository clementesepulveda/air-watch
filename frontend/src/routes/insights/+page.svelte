<script>
// @ts-nocheck

	import Navbar from "../../components/Navbar.svelte";
	import PieGraph from "../../components/PieGraph.svelte";
	import PopulationGraph from "../../components/PopulationGraph.svelte";
	import TemporalGraph from "../../components/TemporalGraph.svelte";
    
    let option = 0;
</script>

<Navbar />

<h1>Insights</h1>

<div class="buttons">
    <button class="button-1"on:click={()=>option=1}>Flights</button>
    <button class="button-1"on:click={()=>option=2}>Airlines</button>
    <button class="button-1"on:click={()=>option=3}>Passengers</button>
</div>
{#if option == 1}
    <TemporalGraph />
{:else if option == 2}
    <PieGraph />
{:else if option == 3}
    <PopulationGraph />
{/if}

<style>
    h1 {
        font-size: 50pt;
        text-align: center;
        margin: 0rem 0rem 1rem 0rem;
    }

    .buttons {
        display: flex;
        justify-content: center;
        /* background-color: green; */
    }

    button {
        margin: 1rem;
        margin-top: 0;
        width: 5.5rem;
        height: 2rem;
    }

    .button-1 {
        background-color: #1C6DDF;
        border-radius: 8px;
        border-style: none;
        box-sizing: border-box;
        color: #FFFFFF;
        cursor: pointer;
        display: inline-block;
        font-size: 14px;
        font-weight: 500;
        height: 40px;
        line-height: 20px;
        list-style: none;
        outline: none;
        position: relative;
        text-align: center;
        text-decoration: none;
        transition: color 100ms;
        vertical-align: baseline;
        user-select: none;
        -webkit-user-select: none;
        touch-action: manipulation;
    }

    .button-1:hover,
        .button-1:focus {
        background-color: #367bdb;
    }

</style>