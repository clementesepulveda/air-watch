<script>
    // @ts-nocheck
    
    import { onMount } from 'svelte';
    import * as echarts from 'echarts';
    import { PUBLIC_BASE_URL } from '$env/static/public'

    let data = []
    let year = "";
    let flight_class = "";

    let loading = false;
    let chartDom;
    let myChart;

    onMount( async () => {
        myChart = echarts.init(chartDom);
        console.log(chartDom)
        fetchData();
    });

    function showGraph() {
        // var chartDom = document.getElementById('graph');
        console.log(chartDom)

        window.onresize = function() {
            myChart.resize();
        };

        const option = {
            tooltip: {
                trigger: 'item'
            },
            legend: {
                orient: 'vertical',
                // type: 'scroll',
                left: 'left'
            },
            series: [{
                type: 'pie',
                radius: '50%',
                data: data,
                emphasis: {
                    itemStyle: {
                    shadowBlur: 10,
                    shadowOffsetX: 0,
                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }]
        };
        option && myChart.setOption(option);
    }

    async function fetchData() {
        loading = true;

        let url = PUBLIC_BASE_URL + "/vuelos_cantidad_data?"
        if (year) {
            url += `&year=${year}`
        }
        if (flight_class) {
            url += `&flight_class=${flight_class}`
        }

        console.log(url)

        const response = await fetch(url);
        const flights = await response.json();

        data = []
        flights.forEach(flight => {
            data.push({
                name: flight['airline'],
                value: flight['total_passengers']
            })
        });

        loading = false;
        showGraph();
    }
</script>

<div id="graph-container">
    <div id="title">Cantidad de Vuelos por Aereolínea</div>
    <div id="options">
        <select name="year" id="year" bind:value={year} on:change={fetchData}>
            <option value="">-</option>
            {#each Array.from({length: 9}, (_,index)=> 2015+index) as i}
                <option value={i}>{i}</option>
            {/each}
        </select>
        <select name="characteristic" id="characteristic" bind:value={flight_class} on:change={fetchData}>
            <option value="">-</option>
            <option value="first class">first class</option>
            <option value="economy">economy</option>
            <option value="bussines">business</option>
        </select>
    </div>
    <div id="graph" bind:this={chartDom}></div>
</div>

<style>
    h1 {
        font-size: 50pt;
        text-align: center;
        margin: 0rem 0rem 1rem 0rem;
    }

    #graph-container {
        background-color: red;
        text-align: center;
        font-size: 20pt;

        border-radius: 10px;
        padding: 0rem 2rem 2rem 2rem;
        height: 25rem;
        width: 80%;

        display: flex;
        flex-direction: column;
    }

    #graph {
        height: 34rem;
        /* background-color: purple; */
    }

    #title {
        padding: 1rem;
    }
</style>