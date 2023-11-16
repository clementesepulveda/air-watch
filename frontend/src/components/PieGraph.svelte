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
        myChart = echarts.init(chartDom, 'dark');
        fetchData();
    });

    function showGraph() {
        window.onresize = function() {
            myChart.resize();
        };

        const option = {
            tooltip: {
                confine: true,
                trigger: 'item'
            },
            legend: {
                orient: 'vertical',
                type: 'scroll',
                left: 'left'
            },
            series: [{
                type: 'pie',
                radius: '50%',
                center: ['50%', '60%'], // Adjust the y-coordinate to align to the bottom
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

<main>
    <div id="graph-container">
        <div id="title">Number of Flights per Airline</div>
        <div id="options-container">
            <div id="options">
                <label for="option">Year</label>
                <select name="year" id="year" bind:value={year} on:change={fetchData}>
                    <option value="">-</option>
                    {#each Array.from({length: 9}, (_,index)=> 2015+index) as i}
                        <option value={i}>{i}</option>
                    {/each}
                </select>
                
                <label for="option">Type of Seats</label>
                <select name="characteristic" id="characteristic" bind:value={flight_class} on:change={fetchData}>
                    <option value="">-</option>
                    <option value="first class">first class</option>
                    <option value="economy">economy</option>
                    <option value="bussines">business</option>
                </select>
            </div>
        </div>
        <div id="graph" bind:this={chartDom}></div>
    </div>
</main>

<style>
    main {
        padding: 1rem;
        display: flex;
        justify-content: center;
    }

    #graph-container {
        background-color: #303138; 
        box-shadow: 0px 0px 25px #151518;
        text-align: center;
        font-size: 20pt;

        border-radius: 10px;
        padding: 0rem 1rem 1rem 1rem;
        height: 40rem;
        width: 90%;

        display: flex;
        flex-direction: column;
    }

    #graph {
        flex-grow: 1;
    }

    #title {
        padding: 1rem;
    }

    label {
        font-size: 1rem;
    }

    #options {
        padding-bottom: 1rem;
    }

    div#options {
        display:grid;
        justify-content: center;
        grid-template-columns: max-content max-content;
        grid-gap:5px;
    }
    div#options label       { text-align:right; }
    div#options label:after { content: ":"; }
</style>