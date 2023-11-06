<script>
// @ts-nocheck

	import Navbar from "../../components/Navbar.svelte";
    import { onMount } from 'svelte';
    import * as echarts from 'echarts';
    import { PUBLIC_BASE_URL } from '$env/static/public'
	import FlightsTable from "../../components/FlightsTable.svelte";

    let data = []

    onMount( async () => {
        const response = await fetch(PUBLIC_BASE_URL+"/vuelos");
        const vuelos = await response.json();

        const airlines = {}
        vuelos.forEach(flight => {
            if (flight.airline in airlines) {
                airlines[flight.airline] += 1;
            } else {
                airlines[flight.airline] = 0
            }
        });

        data = []
        for (const [key, value] of Object.entries(airlines)) {
            data.push({
                name: key,
                value: value,
            })
        }

        console.log(vuelos)
        showGraph();
    });

    function showGraph() {
        var chartDom = document.getElementById('graph');
        var myChart = echarts.init(chartDom);
        window.onresize = function() {
            myChart.resize();
        };

        const option = {
            // title: {
            //     text: 'Referer of a Website',
            //     subtext: 'Fake Data',
            //     left: 'center'
            // },
            tooltip: {
                trigger: 'item'
            },
            legend: {
                orient: 'vertical',
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
</script>

<Navbar />

<h1>Insights</h1>
<div id="graph-container">
    <div id="title">Cantidad de Vuelos por Aereolínea</div>
    <div id="options">
        <select name="year" id="year">
            <option value="2019">2019</option>
        </select>
        <select name="characteristic" id="characteristic">
            <option value="all">-</option>
            <option value="first-class">first class</option>
            <option value="economy-class">economy</option>
            <option value="business-class">business</option>
        </select>
    </div>
    <div id="graph"></div>
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
    }

    #graph {
        height: 100%;
    }

    #title {
        /* background-color: green; */
        padding: 1rem;
    }
</style>