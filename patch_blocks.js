// --------------------------
// Ellipse plot variables

var DISTRICT = (function(d3){

	var dis = { version: '0.0.1' };

	var pathTimeElem = d3.select("#district_path_time");
	var ptime_width = 800;
	var ptime_height = 30;
    
    // NOTE: hard coding length of original ROM for now...
	var ptime_scale = d3.scale.linear().domain([0, 40975]).range([0, ptime_width]);
	
	// Setting up the base SVG element for the district path time bar
	var path_time_canvas = pathTimeElem.append("svg:svg")
				.attr("class", "pathtime")
				.attr("width", ptime_width)
				.attr("height", ptime_height)
				.attr("id", "path_time_canvas")
			.append("g")
				.attr("transform", "translate(0,0)");
				

	// UTILITY private methods
	

	// PUBLIC methods
	
	dis.update_path_time = function(mods_list) {
		var ptimebar = path_time_canvas.selectAll("rect")
			.data(mods_list, function(d){ return d.start; });
					
		ptimebar.enter()
				.append("rect")
			.attr("x", function(d){ return ptime_scale(d.start); })
			.attr("y", 0)
			.attr("width", function(d){ return ptime_scale(d.bytes); })
			.attr("height", ptime_height);
		
		ptimebar.exit()
				.remove();
	};


	// Get data for both the paths and ellipses surrounding a certain district
	// and update visualizations for both
	dis.visgen = function(district_id) {
		
		d3.json('patch.json', function(error_path, mods_list) {
			
			// error will get triggered on null response
			if (error_path) {
				console.warn(error_path);
			}
			if (mods_list) {
			
                // Update the district path time bar
                dis.update_path_time(mods_list);
                
			}
		}); // d3.json(path_data)
	};

	return dis;

}(d3));

// END DISTRICT
// --------------------------
