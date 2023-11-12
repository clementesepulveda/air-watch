<script>
// @ts-nocheck

	import Navbar from "../../components/Navbar.svelte";
	import PieGraph from "../../components/PieGraph.svelte";
	import TemporalGraph from "../../components/TemporalGraph.svelte";
    
    let option = 0;
</script>

<Navbar />

<h1>Insights</h1>

<button on:click={()=>option=(option+1)%4}>asdf</button>
{#if option == 1}
    <TemporalGraph />
{:else if option == 2}
    <PieGraph />
{:else if option == 3}
    <div>3rd</div>
{/if}

<style>
    h1 {
        font-size: 50pt;
        text-align: center;
        margin: 0rem 0rem 1rem 0rem;
    }
    
</style>