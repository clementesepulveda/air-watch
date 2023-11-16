<script>
	// @ts-nocheck

	import Navbar from "../components/Navbar.svelte";
  </script>
  
  <Navbar />
  
  <h1>Welcome to Air Watch Insights</h1>
  
  <div id="content">
	<div class="container">
	  <p>
		Explore the fascinating world of aviation with Air Watch Insights, your go-to destination for comprehensive and visually engaging airline data. Whether you're an aviation enthusiast, a data analyst, or a curious traveler, our website offers a wealth of information, interactive graphs, and unique perspectives on air travel.
	  </p>
	  <!-- <img src="https://cdn.britannica.com/02/215002-050-513175D0/American-actor-Danny-DeVito-2016.jpg" alt="danny devito" /> -->
	</div>
  </div>


  
  <style>
	#content {
	  padding: 0rem 2rem 2rem 2rem;
	}
  
	h1 {
	  /* background-color: green; */
	  text-align: center;
	  font-size: 50pt;
	}
  
	p {
	  font-size: 25pt;
	}
  
	.container {
		/* width: 100%; */
		/* background-color: red; */
		display: flex;
		flex-wrap: nowrap;
		position: relative; /* Set the position to relative */
	}

	img {
		width: 70%;
		max-height: 90vh;
	}
  </style>
  