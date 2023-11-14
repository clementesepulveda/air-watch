<script>
    // @ts-nocheck
    
    import { onMount } from 'svelte';
    import * as echarts from 'echarts';
    import { PUBLIC_BASE_URL } from '$env/static/public'

    let data = []
    let year = "";
    let characteristics = "distance";
    let chars_Titles = {
        "distance": "Total Distance Traveled per Month",
        "weight": "Total Weight Transported per Month",
        "height": "Average Passenger Height per Month"
    }
    let chars_units = {
        "distance": "km",
        "weight": "kg",
        "height": "cm"
    }

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
            xAxis: {
                type: 'category',
                nameLocation: 'center',
                nameGap: 60,
                name: 'month',
                data: data.map( item => item.month),
                axisLabel: {
                    show: true,
                    interval: 0,
                    rotate: 45,
                },
            },
            yAxis: {
                type: 'value',
                nameLocation: 'center',
                nameGap: 50,
                name: `${characteristics} (${chars_units[characteristics]})`,
            },
            series: [{
                data: data.map( item => item.value),
                type: 'bar'
            }],
            grid: {containLabel: true, left: 25, bottom: 30},
            tooltip: {
                trigger: 'axis',
                confine: true,
                axisPointer: {
                    type: 'shadow'
                },
                formatter: function (params) {
                    const data = params[0]
                    return `month: ${data.axisValue}<br>${characteristics}: ${Math.round(data.data * 100) / 100} (${chars_units[characteristics]})`
                }
            },
        };
        option && myChart.setOption(option);
    }

    async function fetchData() {
        loading = true;

        let url = PUBLIC_BASE_URL + "/temporal_data?"
        if (year) {
            url += `&year=${year}`
        }
        if (characteristics) {
            url += `&characteristics=${characteristics}`
        }
        const response = await fetch(url);
        data = await response.json();

        loading = false;
        showGraph();
    }
</script>

<main>
    <div id="graph-container">
        <div id="title">{chars_Titles[characteristics]}</div>
        <div id="options-container">
            <div id="options">
                <label for="option">Year</label>
                <select name="year" id="year" bind:value={year} on:change={fetchData}>
                    <option value="">-</option>
                    {#each Array.from({length: 9}, (_,index)=> 2015+index) as i}
                        <option value={i}>{i}</option>
                    {/each}
                </select>
                
                <label for="option">Characteristic</label>
                <select name="characteristic" id="characteristic" bind:value={characteristics} on:change={fetchData}>
                    <option value="distance">Total Distance</option>
                    <option value="weight">Total Weight</option>
                    <option value="height">Average Height</option>
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