<script>
    // @ts-nocheck

    import { onMount } from 'svelte';
    import * as echarts from 'echarts';
    import { PUBLIC_BASE_URL } from '$env/static/public'
	import { SyncLoader } from 'svelte-loading-spinners';

    let yAxis = Array.from({length: 99}, (_,index)=> 99-index)
    let maleData = []
    let femaleData = []
    let year = "";

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
                show: true,
                axisPointer: {
                type: 'shadow'
                },
                formatter: function (params) {
                    return `${params.seriesName} <br>Age: ${params.name} <br>Quantity: ${Math.abs(params.value)}`
                }
            },
            legend: {
                data: ['Female', 'Male']
            },
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            label: {
                show: true,
                formatter: function (params) {
                    if (typeof(params.value) === 'number') {
                        return Math.abs(params.value);
                    }
                }
            },
            xAxis: [{
                type: 'value',
                name: 'Total of Passengers',
                nameLocation: 'center',
                nameTextStyle: {
                    padding: [5, 0, 0, 0],
                },
                axisLabel: {
                    formatter: function (params) {
                        return Math.abs(params);
                    }
                }
            }],
            yAxis: [{
                type: 'category',
                name: 'Age of Passengers',
                nameTextStyle: {
                    padding: [0, 0, 15, 0],
                },
                nameLocation: 'center',
                axisTick: {
                    show: false
                },
                data: yAxis
            }],
            series: [{
                name: 'Female',
                type: 'bar',
                stack: 'Total',
                label: {
                    show: true
                },
                // emphasis: {
                //     focus: 'series'
                // },
                data: femaleData,
                barCategoryGap: '-1%',
            },{
                name: 'Male',
                type: 'bar',
                stack: 'Total',
                label: {
                    show: true,
                },
                // emphasis: {
                //     focus: 'series'
                // },
                data: maleData
            }],
            dataZoom: [
                {
                    type: 'slider',
                    yAxisIndex: [0],
                    start: 0,
                    end: 100
                },
            ],
            grid: {containLabel: true, left: 25, bottom: 15},
            
        };
        option && myChart.setOption(option);
    }

    async function fetchData() {
        loading = true;

        let url = PUBLIC_BASE_URL + "/population_data?"
        if (year) {
            url += `&year=${year}`
        }

        const response = await fetch(url);
        const data = await response.json();

        maleData = []
        femaleData = []
        yAxis.forEach(age => {
            maleData.push(data['males'][age.toString()])
            femaleData.push(-data['females'][age.toString()])
        });

        loading = false;
        showGraph();
    }
</script>

<main>
    <div id="graph-container">
        <div id="title">Number of Passengers by Age</div>
        <div id="options">
                <label for="options">Year</label>
                <select name="year" id="year" bind:value={year} on:change={fetchData}>
                    <option value="">-</option>
                    {#each Array.from({length: 9}, (_,index)=> 2015+index) as i}
                        <option value={i}>{i}</option>
                    {/each}
                </select>
        </div>

        {#if loading}
            <div class="spinner">
                <SyncLoader color="#F8F8F8"/>
            </div>
        {/if}
        <div id="graph" bind:this={chartDom} class:show={!loading}></div>
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
        height: 45rem;
        width:90%;

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
    
    .spinner {
        display: grid;
        place-items: center;
        height: 100vh;
        background-color: #100C2A;
    }

    #graph {
        display: none; /* Initially hide the graph */
    }

    .show {
        display: block !important; /* Show when the class is present */
    }
</style>